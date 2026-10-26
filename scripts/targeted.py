"""Targeted search for a given type: deform a smaller arrangement inside its own type until new lines fit.

For a target type T on n lines, take the certificate A of a type T' on n-k lines (k = 1 or 2) and choose, for
each new line, a set S of intersection points of A that it should pass through (k = 1: the multiplicities of
the points in S are determined by T and T'; k = 2: random sets, preferring points whose multiplicity + 1
occurs in T).  Then solve, by minimum-norm Gauss-Newton starting from A,
        all pencils of A stay concurrent  +  every new line passes through its points,
so A moves as little as possible inside its realization space until the points of S become collinear.  The
coordinates that come out are roots of polynomial equations: quadratic irrationalities such as sqrt 5 appear
by themselves (from rational certificates this finds {5, 3^10}, which needs sqrt 5, and {3^16}, known only over Q(sqrt 5)).  A numerical
solution of exactly type T is turned into an exact certificate by scripts/realize.py (snap_to_rationals,
exactify) and kept only if verifier/verify.py accepts it.

usage: python scripts/targeted.py N "k1,k2,..;k1,.." [--k 1|2] [--tries 300] [--workers 4] [--stock FILE ...] [--add]
  The smaller arrangements are the certificates of n-k lines plus, with --stock, the realizations saved by
  scripts/zone_walk.py --save (several different realizations per type make the search much stronger).
"""
import argparse, itertools, json, math, os, random, sys, time
from collections import Counter, defaultdict
from multiprocessing import Pool
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "verifier"))
from realize import snap_to_rationals, exactify, realize_blocks
from verify import verify, Reject
from pencils import unkey, fmt

TON, TOFF = 1e-10, 1e-6           # incidence / ambiguity thresholds for the numerical type


def pencils(L):
    """numerical pencils {frozenset of lines: point}, or None if some incidence is ambiguous"""
    n = len(L)
    U = L / np.linalg.norm(L, axis=1)[:, None]
    out = {}
    for i, j in itertools.combinations(range(n), 2):
        c = np.cross(U[i], U[j]); s = np.linalg.norm(c)
        if s < 1e-7:
            return None
        p = c / s
        on = [i, j]
        for k in range(n):
            if k not in (i, j):
                v = abs(np.dot(U[k], p))
                if v < TON:
                    on.append(k)
                elif v < TOFF:
                    return None
        out[frozenset(on)] = p
    return out


def type_of(pens):
    return tuple(sorted((len(s) for s in pens if len(s) >= 3), reverse=True))


def increments(n, T, Tp):
    """k = 1: x[m] = number of points of multiplicity m the new line must pass through, or None"""
    def counts(m, t):
        c = Counter(t); c[2] = math.comb(m, 2) - sum(math.comb(q, 2) for q in t); return c
    c, cp = counts(n, T), counts(n - 1, Tp)
    x, xk = {}, 0
    for k in range(n, 2, -1):
        xk1 = c[k] - cp[k] + xk
        if xk1 < 0 or xk1 > cp[k - 1]:
            return None
        x[k - 1] = xk1; xk = xk1
    d0 = (n - 1) - sum(m * v for m, v in x.items())
    if d0 < 0 or c[2] != cp[2] - x[2] + d0 or sum(x.values()) < 2:
        return None
    return {m: v for m, v in x.items() if v}


def gauss_newton(L0, eqs, iters=60):
    """min-norm Gauss-Newton for det(L_a, L_b, L_c) = 0 (eqs) and |L_i| = 1"""
    L = np.array(L0, float); L /= np.linalg.norm(L, axis=1)[:, None]
    n = len(L)
    for _ in range(iters):
        r = np.empty(len(eqs) + n); J = np.zeros((len(eqs) + n, 3 * n))
        for e, (a, b, c) in enumerate(eqs):
            r[e] = np.dot(L[a], np.cross(L[b], L[c]))
            J[e, 3 * a:3 * a + 3] = np.cross(L[b], L[c])
            J[e, 3 * b:3 * b + 3] = np.cross(L[c], L[a])
            J[e, 3 * c:3 * c + 3] = np.cross(L[a], L[b])
        for i in range(n):
            r[len(eqs) + i] = np.dot(L[i], L[i]) - 1; J[len(eqs) + i, 3 * i:3 * i + 3] = 2 * L[i]
        if not np.all(np.isfinite(r)):
            return None
        if np.max(np.abs(r)) < 1e-14:
            return L
        try:
            L = L + np.linalg.lstsq(J, -r, rcond=1e-12)[0].reshape(n, 3)
        except np.linalg.LinAlgError:
            return None
    return L if np.max(np.abs(r)) < 1e-12 else None


def certificate(L, T):
    n = len(L)
    blocks = [sorted(s) for s in pencils(L) if len(s) >= 3]
    Q = snap_to_rationals(n, blocks, L)
    for P in ([Q] if Q is not None else []) + [L]:
        ex = exactify(P, maxden=10 ** 6)
        if ex is None:
            continue
        cert = {"n": n, "d": ex[0], "type": list(T), "lines": ex[1],
                "source": "targeted deformation (scripts/targeted.py) + exact reconstruction"
                          + (" over Q(sqrt %d)" % ex[0] if ex[0] else "")}
        try:
            verify(cert); return cert
        except Reject:
            pass
    c = realize_blocks(n, blocks, seed=1, starts=40, source="linear space found by scripts/targeted.py; numerical realization + exact reconstruction")
    return c if c and tuple(c["type"]) == tuple(T) else None


def attempt(job):
    T, k, A, x, tries, seed = job
    rng = random.Random(seed)
    A = np.array(A, float)
    pens = pencils(A)
    if pens is None:
        return None
    n = len(A) + k
    pts = list(pens.items())
    blocks = [sorted(s) for s in pens if len(s) >= 3]
    base = [(b[0], b[1], c) for b in blocks for c in b[2:]]

    def pick(size, start=(), want=None):
        S = list(start)
        pool = pts[:]
        if want is None and rng.random() < 0.7:
            pool = [q for q in pool if len(q[0]) + 1 in T or len(q[0]) == 2]
        rng.shuffle(pool)
        for q in pool:
            if len(S) == size:
                break
            if want is not None and want[len(q[0])] <= sum(1 for s in S if len(s[0]) == len(q[0])):
                continue
            if all(not (q[0] & s[0]) for s in S):
                S.append(q)
        return S if len(S) == size else None

    for _ in range(tries):
        if k == 1:
            sets = [pick(sum(x.values()), want=Counter(x))]
        else:
            S1 = pick(rng.randint(2, n // 2))
            sets = [S1, pick(rng.randint(2, n // 2), [rng.choice(S1)] if S1 and rng.random() < 0.4 else [])]
        if any(S is None for S in sets):
            continue
        new = [np.linalg.svd(np.array([p for _, p in S]))[2][-1] for S in sets]
        eqs = base + [(min(s), sorted(s)[1], len(A) + j) for j, S in enumerate(sets) for s, _ in S]
        L0 = np.vstack([A] + new) + 1e-4 * np.random.default_rng(rng.randrange(1 << 30)).standard_normal((n, 3))
        L = gauss_newton(L0, eqs)
        if L is None:
            continue
        p2 = pencils(L)
        if p2 is not None and type_of(p2) == T:
            c = certificate(L, T)
            if c:
                return c
    return None


def stock(m, files=()):
    out = []
    for c in json.load(open(os.path.join(ROOT, "data", "certificates", "n%d.json" % m))):
        s = math.sqrt(c["d"])
        out.append((tuple(c["type"]), [[a + b * s for a, b in l] for l in c["lines"]]))
    for fn in files:
        z = json.load(open(fn)); s = math.sqrt(z["d"])
        for t, Ls in z["arrangements"].get(str(m), {}).items():
            T = tuple(int(q) for q in t.split(",")) if t else ()
            out += [(T, [[a + b * s for a, b in l] for l in L]) for L in Ls]
    return out


def below2(T, Tp):
    """k = 2: cheap necessary condition for T to arise from Tp by adding two lines"""
    return (sum(math.comb(q, 2) for q in Tp) <= sum(math.comb(q, 2) for q in T)
            and max(Tp, default=2) <= max(T, default=2) <= max(Tp, default=2) + 2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("types")
    ap.add_argument("--k", type=int, default=1); ap.add_argument("--tries", type=int, default=300)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--add", action="store_true"); ap.add_argument("--stock", nargs="*", default=[])
    a = ap.parse_args()
    targets = [tuple(sorted(unkey(s), reverse=True)) for s in a.types.split(";")]
    st = stock(a.n - a.k, a.stock)
    jobs = []
    for T in targets:
        if a.k == 1:
            jobs += [(T, 1, A, x, a.tries, hash((T, Tp)) & 0xffff) for Tp, A in st for x in [increments(a.n, T, Tp)] if x]
        else:
            cand = sorted([(Tp, A) for Tp, A in st if below2(T, Tp)], key=lambda z: -sum(math.comb(q, 2) for q in z[0]))
            jobs += [(T, 2, A, None, a.tries, hash((T, Tp)) & 0xffff) for Tp, A in cand[:a.top]]
    print("%d targets, %d jobs" % (len(targets), len(jobs)), flush=True)
    found = {}; t0 = time.time()
    with Pool(a.workers) as P:
        for c in P.imap_unordered(attempt, jobs):
            if c and tuple(c["type"]) not in found:
                found[tuple(c["type"])] = c
                print("[%.0fs] FOUND %s (d = %d)" % (time.time() - t0, fmt(tuple(c["type"])), c["d"]), flush=True)
    print("found %d of %d" % (len(found), len(targets)))
    if a.add:
        from find_examples import add_certificate
        for c in found.values():
            print("  ", fmt(tuple(c["type"])), "added" if add_certificate(c) else "already present")
