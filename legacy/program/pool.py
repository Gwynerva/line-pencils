# Exact point pools (over Q or Q(sqrt d)) and a fast search for subsets with a given
# pencil signature.  Dual picture: points <-> original lines, lines with k points <-> k-pencils.
from fractions import Fraction as Fr
import random, json, sys, os, time, math

# ---------- arithmetic in Z[sqrt d] (pairs of ints); d=0 means plain integers ----------
D = 0
def mul(x, y):
    return (x[0]*y[0] + D*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def add(x, y): return (x[0]+y[0], x[1]+y[1])
def sub(x, y): return (x[0]-y[0], x[1]-y[1])
def iszero(x): return x[0] == 0 and x[1] == 0
def cross(a, b):
    return (sub(mul(a[1],b[2]), mul(a[2],b[1])), sub(mul(a[2],b[0]), mul(a[0],b[2])), sub(mul(a[0],b[1]), mul(a[1],b[0])))
def dot(a, b): return add(add(mul(a[0],b[0]), mul(a[1],b[1])), mul(a[2],b[2]))
def nz_vec(v): return not all(iszero(c) for c in v)
def same(p, q): return not nz_vec(cross(p, q))

def gcd_reduce(v):
    g = 0
    for c in v:
        g = math.gcd(g, abs(c[0])); g = math.gcd(g, abs(c[1]))
    if g > 1: v = tuple((c[0]//g, c[1]//g) for c in v)
    return v

def from_frac(pt):
    """pt: triple of (Fraction a, Fraction b) meaning a + b sqrt(D). Clear denominators."""
    den = 1
    for a, b in pt:
        den = den * Fr(a).denominator // math.gcd(den, Fr(a).denominator)
        den = den * Fr(b).denominator // math.gcd(den, Fr(b).denominator)
    v = tuple((int(Fr(a)*den), int(Fr(b)*den)) for a, b in pt)
    return gcd_reduce(v)

def rat(x, y, z=1):
    return from_frac(((Fr(x),0),(Fr(y),0),(Fr(z),0)))

class Pool:
    def __init__(self, pts, name, d=0):
        global D
        D = d
        self.d = d; self.name = name
        uniq = []
        for p in pts:
            if not nz_vec(p): continue
            if any(same(p, q) for q in uniq): continue
            uniq.append(p)
        self.pts = uniq
        N = len(uniq)
        cov = [0]*N
        lines = []
        for i in range(N):
            for j in range(i+1, N):
                if cov[i] >> j & 1: continue
                L = cross(uniq[i], uniq[j])
                on = [k for k in range(N) if iszero(dot(L, uniq[k]))]
                m = 0
                for k in on: m |= 1 << k
                for k in on: cov[k] |= m
                lines.append(on)
        self.lines = lines
        self.through = [[] for _ in range(N)]
        for li, L in enumerate(lines):
            for p in L: self.through[p].append(li)
    def rich(self):
        return sorted((len(L) for L in self.lines if len(L) >= 3), reverse=True)

def with_intersections(pts, d, maxadd=200, minrich=3, rng=None):
    """Add intersection points of pairs of rich lines (lines with >= minrich points)."""
    P = Pool(pts, "tmp", d)
    global D
    D = d
    rl = [L for L in P.lines if len(L) >= minrich]
    cand = []
    for i in range(len(rl)):
        for j in range(i+1, len(rl)):
            L1 = cross(P.pts[rl[i][0]], P.pts[rl[i][1]])
            L2 = cross(P.pts[rl[j][0]], P.pts[rl[j][1]])
            X = cross(L1, L2)
            if nz_vec(X): cand.append(gcd_reduce(X))
    if rng: rng.shuffle(cand)
    return P.pts + cand[:maxadd]

# ---------- signature search on a pool ----------
class State:
    def __init__(self, pool, S):
        self.P = pool
        self.inS = [False]*len(pool.pts)
        self.c = [0]*len(pool.lines)
        self.h = {}
        for p in S: self.add(p)
    def _bump(self, k, dlt):
        self.h[k] = self.h.get(k, 0) + dlt
    def add(self, p):
        self.inS[p] = True
        for li in self.P.through[p]:
            k = self.c[li]
            if k >= 2: self._bump(k, -1)
            self.c[li] = k+1
            if k+1 >= 2: self._bump(k+1, +1)
    def remove(self, p):
        self.inS[p] = False
        for li in self.P.through[p]:
            k = self.c[li]
            if k >= 2: self._bump(k, -1)
            self.c[li] = k-1
            if k-1 >= 2: self._bump(k-1, +1)
    def sig(self):
        out = []
        for k, v in self.h.items():
            if k >= 3 and v > 0: out += [k]*v
        return tuple(sorted(out, reverse=True))

def score(h, target):
    s = 0
    keys = set(k for k in h if k >= 3) | set(target)
    for k in keys:
        s += abs(h.get(k, 0) - target.get(k, 0)) * (k-1)
    return s

def anneal(pool, n, target, steps, rng, record=None, T0=2.0):
    N = len(pool.pts)
    if N < n: return None
    S = rng.sample(range(N), n)
    st = State(pool, S)
    tgt = {}
    for k in target: tgt[k] = tgt.get(k, 0) + 1
    cur = score(st.h, tgt)
    inS = set(S); outS = [p for p in range(N) if p not in inS]
    if record is not None: record.setdefault(st.sig(), sorted(S))
    if not outS: return sorted(S) if cur == 0 else None
    for step in range(steps):
        if cur == 0:
            return sorted(p for p in range(N) if st.inS[p])
        T = T0 * (1 - step/steps) + 0.05
        i = rng.randrange(n); j = rng.randrange(len(outS))
        p = S[i]; q = outS[j]
        st.remove(p); st.add(q)
        new = score(st.h, tgt)
        if new <= cur or rng.random() < math.exp((cur-new)/T):
            S[i] = q; outS[j] = p; cur = new
            if record is not None:
                record.setdefault(st.sig(), sorted(S))
        else:
            st.remove(q); st.add(p)
    return None
