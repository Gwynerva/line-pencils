"""Zone walk: construct arrangements by inserting and re-inserting one line at a time, in exact arithmetic.

A new line is a point of the dual plane, which is cut by the dual lines of the intersection points of the
current arrangement B.  The type of B + new line depends only on which intersection points the new line
passes through, so it suffices to try one line per class:
    a cell    - through no intersection point,
    an edge   - through exactly one point (its pencil grows by one),
    a vertex  - through >= 2 points (a line through two points; it may contain more of them).
Moves: insert (n-1 -> n lines) into every class, and re-insert (remove any line of an n-line arrangement and
put it back into every class).  For every type we keep up to R realizations for each of up to G
combinatorial classes (profile = multiset over the lines of the multiplicities of the points on them), and
iterate the moves until nothing new is kept.

Arithmetic: integers (d = 0) or Z[sqrt d]; points are identified by their pencils (sets of lines) and lines
through points by the set of points on them, so no projective normal form is needed.  Starting from two lines
the walk only produces rational arrangements; starting from the certificates of N0 lines over Q(sqrt d) it
continues the irrational ones.

Every type found is checked with verifier/verify.py; with --add, certificates of types that have none in
data/certificates/n{n}.json are appended there.

usage: python scripts/zone_walk.py NMAX [--from N0] [--d D] [--R 2] [--G 6] [--add] [--save FILE]
       --save writes every kept realization ({n: {type: [lines]}}, field d) for scripts/targeted.py --stock
"""
import argparse, itertools, json, math, os, random, sys, time
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "verifier")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
from verify import verify, cross as qcross, dot as qdot, is_zero as qzero
from pencils import fmt


class Field:
    """exact arithmetic on 3-vectors over Z (d = 0, plain integers) or Z[sqrt d] (pairs of integers)"""

    def __init__(self, d):
        self.d = d

    def cross(self, u, v):
        if self.d == 0:
            return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        return qcross(u, v, self.d)

    def zero_dot(self, u, v):
        if self.d == 0:
            return u[0] * v[0] + u[1] * v[1] + u[2] * v[2] == 0
        return qzero(qdot(u, v, self.d))

    def is_null(self, v):
        return all((c == 0) if self.d == 0 else qzero(c) for c in v)

    def reduce(self, v):
        g = 0
        for c in v:
            for x in ((c,) if self.d == 0 else c):
                g = math.gcd(g, abs(x))
        if g > 1:
            v = tuple(c // g if self.d == 0 else (c[0] // g, c[1] // g) for c in v)
        return v

    def lift(self, x):
        return x if self.d == 0 else (x, 0)

    def height(self, L):
        return max(abs(x) for l in L for c in l for x in ((c,) if self.d == 0 else c))

    def to_cert(self, L):
        return [[[c, 0] if self.d == 0 else [c[0], c[1]] for c in l] for l in L]


def pencils(F, L):
    """dict pencil (frozenset of line indices) -> intersection point"""
    out = {}
    for i, j in itertools.combinations(range(len(L)), 2):
        P = F.cross(L[i], L[j])
        S = frozenset(k for k in range(len(L)) if F.zero_dot(L[k], P))
        out.setdefault(S, P)
    return out


def type_of(pens):
    return tuple(sorted((len(s) for s in pens if len(s) >= 3), reverse=True))


def profile(pens):
    per = defaultdict(list)
    for s in pens:
        for i in s:
            per[i].append(len(s))
    return tuple(sorted(tuple(sorted(v, reverse=True)) for v in per.values()))


def zone_lines(F, B, rng, tries=60):
    """one new line per class of the dual subdivision of B: dict resulting type -> line"""
    P = pencils(F, B)
    pts = list(P.items())
    mult = Counter(len(s) for s in P)
    out = {}

    def result(on):
        c = Counter(mult)
        for s in on:
            c[len(s)] -= 1; c[len(s) + 1] += 1
        return tuple(sorted((k for k, v in c.items() if k >= 3 for _ in range(v)), reverse=True))

    seen = set()
    for (sa, pa), (sb, pb) in itertools.combinations(pts, 2):         # vertices
        if sa & sb:
            continue                                                    # the line of B through both
        ell = F.cross(pa, pb)
        on = frozenset(s for s, p in pts if F.zero_dot(ell, p))
        if on not in seen:
            seen.add(on)
            out.setdefault(result(on), F.reduce(ell))
    small = lambda: tuple(F.lift(rng.randint(lo, 9)) for lo in (-9, -9, 1))
    for s, p in pts:                                                    # edges
        for _ in range(tries):
            ell = F.cross(p, small())
            if F.is_null(ell) or any(F.is_null(F.cross(ell, l)) for l in B):
                continue
            if sum(1 for _, q in pts if F.zero_dot(ell, q)) == 1:
                out.setdefault(result([s]), F.reduce(ell)); break
    for _ in range(tries):                                              # a cell
        ell = tuple(F.lift(rng.randint(-9, 9)) for _ in range(3))
        if not F.is_null(ell) and all(not F.zero_dot(ell, q) for _, q in pts):
            out.setdefault(result([]), ell); break
    return out


def walk(F, start, nmax, R, G, log, seed=0):
    """start: dict n0 -> {type: [arrangements]}; returns dict n -> {type: {profile: [arrangements]}}"""
    rng = random.Random(seed)
    n0 = max(start)
    found = {n0: {t: {None: Ls} for t, Ls in start[n0].items()}}
    for n in range(n0 + 1, nmax + 1):
        new = defaultdict(dict)

        def offer(t, L):
            groups = new[t]
            pr = profile(pencils(F, L))
            if pr not in groups:
                if len(groups) >= G:
                    return False
                groups[pr] = [L]; return True
            lst = groups[pr]
            if any(sorted(M) == sorted(L) for M in lst):
                return False
            if len(lst) < R:
                lst.append(L); return True
            j = max(range(len(lst)), key=lambda i: F.height(lst[i]))
            if F.height(L) < F.height(lst[j]):
                lst[j] = L; return True
            return False

        for groups in found[n - 1].values():
            for Ls in groups.values():
                for B in Ls:
                    for t, ell in zone_lines(F, list(B), rng).items():
                        offer(t, tuple(B) + (ell,))
        queue = [L for g in new.values() for Ls in g.values() for L in Ls]
        while queue:
            A = queue.pop()
            for i in range(n):
                B = list(A[:i] + A[i + 1:])
                for t, ell in zone_lines(F, B, rng).items():
                    L = tuple(B) + (ell,)
                    if offer(t, L):
                        queue.append(L)
        found[n] = dict(new)
        log("n=%d: %d types" % (n, len(new)))
    return found


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("nmax", type=int)
    ap.add_argument("--from", dest="n0", type=int, default=None, help="start from the certificates of N0 lines")
    ap.add_argument("--d", type=int, default=0)
    ap.add_argument("--R", type=int, default=2); ap.add_argument("--G", type=int, default=6)
    ap.add_argument("--add", action="store_true"); ap.add_argument("--save", default=None)
    a = ap.parse_args()
    F = Field(a.d)
    if a.n0 is None:
        start = {2: {(): [(tuple(F.lift(x) for x in (1, 0, 0)), tuple(F.lift(x) for x in (0, 1, 0)))]}}
    else:
        start = {a.n0: defaultdict(list)}
        for c in json.load(open(os.path.join(ROOT, "data", "certificates", "n%d.json" % a.n0))):
            if c["d"] in (0, a.d):
                L = tuple(tuple((x[0] if a.d == 0 else (x[0], x[1])) for x in l) for l in c["lines"])
                start[a.n0][tuple(c["type"])].append(L)
    t0 = time.time()
    found = walk(F, start, a.nmax, a.R, a.G, lambda s: print(s, "%.0fs" % (time.time() - t0), flush=True))
    if a.save:
        with open(a.save, "w") as f:
            json.dump({"d": a.d, "arrangements": {str(n): {",".join(map(str, t)): [F.to_cert(L) for Ls in g.values() for L in Ls]
                                                         for t, g in found[n].items()} for n in found}}, f, separators=(",", ":"))
    from find_examples import add_certificate
    for n in range(min(found) + 1, a.nmax + 1):
        known = set()
        fn = os.path.join(ROOT, "data", "certificates", "n%d.json" % n)
        if os.path.exists(fn):
            known = {tuple(sorted(c["type"], reverse=True)) for c in json.load(open(fn))}
        new = [t for t in found[n] if t not in known]
        print("n=%d: %d types found, %d without a certificate so far" % (n, len(found[n]), len(new)), flush=True)
        for t in new:
            L = min((L for Ls in found[n][t].values() for L in Ls), key=F.height)
            cert = {"n": n, "d": a.d, "type": list(t), "lines": F.to_cert(L),
                    "source": "zone walk (scripts/zone_walk.py), exact arithmetic" + (" over Q(sqrt %d)" % a.d if a.d else "")}
            assert tuple(verify(cert)) == t
            print("   ", fmt(t), "max coefficient", F.height(L))
            if a.add:
                add_certificate(cert)
