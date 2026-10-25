"""Numerical realization of a linear space in the real projective plane, followed by exact
reconstruction of the coordinates and verification with the exact verifier.

Input: n and the blocks (lines with >= 3 points) of a linear space on points 0..n-1.
We look for n points of RP^2 (dual: n lines) such that exactly the prescribed triples are
collinear.  Four points that are pairwise non-collinear in the space are fixed to the standard
projective frame; the rest are unknowns.  Collinearity = 3x3 determinant = 0, solved by
least squares from random starts.  A numerical solution is accepted only if the prescribed
determinants vanish to 1e-12 and all other determinants are bounded away from zero.

Exactification: every coordinate is recognised as a rational number with small denominator, or
as a + b*sqrt(d) for d in a short list; the resulting certificate is checked by verifier/verify.py.
A certificate is returned only if it verifies.

usage (library):  realize_blocks(n, blocks, seed, starts) -> certificate dict or None
usage (cli):      python scripts/realize.py N "0,1,2 0,3,4 ..." [starts]
"""
import itertools, json, math, os, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import least_squares

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "verifier"))
from verify import verify, Reject


def collinear_triples(blocks):
    col = set()
    for B in blocks:
        for t in itertools.combinations(sorted(B), 3):
            col.add(t)
    return col


def frame_choice(n, col):
    for q in itertools.combinations(range(n), 4):
        if all(t not in col for t in itertools.combinations(q, 3)):
            return list(q)
    return None


def numeric_realization(n, blocks, seed=0, starts=100, min_gap=1e-3):
    rng = np.random.default_rng(seed)
    col = collinear_triples(blocks)
    fr = frame_choice(n, col)
    if fr is None:
        return None
    F = {fr[0]: [1, 0, 0], fr[1]: [0, 1, 0], fr[2]: [0, 0, 1], fr[3]: [1, 1, 1]}
    free = [i for i in range(n) if i not in F]
    trip = sorted(col)
    noncol = [t for t in itertools.combinations(range(n), 3) if t not in col]
    if not trip:
        return None

    def pts(z):
        P = np.zeros((n, 3))
        for i, v in F.items():
            P[i] = v
        for k, i in enumerate(free):
            P[i] = z[3 * k:3 * k + 3]
        return P

    def res(z):
        P = pts(z)
        nr = np.linalg.norm(P, axis=1)
        Pn = P / nr[:, None]
        r = [np.linalg.det(Pn[list(t)]) for t in trip]
        r += [(np.linalg.norm(P[i]) - 1.0) * 0.1 for i in free]      # scale gauge
        return np.array(r)

    best = None
    for _ in range(starts):
        z0 = rng.normal(size=3 * len(free))
        try:
            r = least_squares(res, z0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        except Exception:
            continue
        P = pts(r.x); Pn = P / np.linalg.norm(P, axis=1)[:, None]
        e = max(abs(np.linalg.det(Pn[list(t)])) for t in trip)
        if e > 1e-11:
            continue
        m = min(abs(np.linalg.det(Pn[list(t)])) for t in noncol) if noncol else 1
        if m < min_gap:
            continue
        if best is None or m > best[1]:
            best = (Pn, m)
        if m > 3e-2:
            break
    return best


def snap_to_rationals(n, blocks, P0, max_den=12, min_gap=1e-4):
    """Move a numerical realization P0 to a point of the realization space with rational
    coordinates by fixing, one at a time, a coordinate to a nearby simple rational and
    re-solving the collinearity equations for the remaining coordinates.

    Each point is normalised so that its largest coordinate is 1; the other two are unknowns.
    Returns the final numerical points (n x 3) with all coordinates rational (to precision) or None."""
    col = collinear_triples(blocks)
    trip = sorted(col)
    noncol = [t for t in itertools.combinations(range(n), 3) if t not in col]
    piv = [int(np.argmax(np.abs(p))) for p in P0]
    Q = np.array([p / p[k] for p, k in zip(P0, piv)])
    unknown = [(i, j) for i in range(n) for j in range(3) if j != piv[i]]
    fixed = {}

    def build(zvals, unk):
        P = Q.copy()
        for (i, j), v in fixed.items():
            P[i, j] = v
        for (i, j), v in zip(unk, zvals):
            P[i, j] = v
        return P

    def resid(zvals, unk):
        P = build(zvals, unk)
        Pn = P / np.linalg.norm(P, axis=1)[:, None]
        return np.array([np.linalg.det(Pn[list(t)]) for t in trip])

    stuck = set()
    while unknown and len(stuck) < len(unknown):
        # candidate: unknown coordinate closest to a rational with small denominator
        best = None
        for (i, j) in unknown:
            if (i, j) in stuck:
                continue
            x = Q[i, j]
            f = Fr(x).limit_denominator(max_den)
            err = abs(float(f) - x)
            if best is None or err < best[0]:
                best = (err, (i, j), f)
        _, (i, j), f = best
        ok = False
        for cand in sorted({f, Fr(Q[i, j]).limit_denominator(2 * max_den), Fr(Q[i, j]).limit_denominator(4)}, key=lambda c: abs(float(c) - Q[i, j])):
            fixed[(i, j)] = float(cand)
            unk = [u for u in unknown if u != (i, j)]
            z0 = np.array([Q[a, b] for a, b in unk])
            if unk:
                r = least_squares(resid, z0, args=(unk,), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
                z = r.x
            else:
                z = z0
            P = build(z, unk)
            Pn = P / np.linalg.norm(P, axis=1)[:, None]
            e = max(abs(np.linalg.det(Pn[list(t)])) for t in trip) if trip else 0
            m = min(abs(np.linalg.det(Pn[list(t)])) for t in noncol) if noncol else 1
            if e < 1e-11 and m > min_gap:
                Q = P; unknown = unk; ok = True
                break
            del fixed[(i, j)]
        if not ok:
            stuck.add((i, j))     # this coordinate is forced by the others: leave it to exactify()
    return Q


def recognise(x, ds, maxden):
    """x -> (d, a, b) with x = a + b*sqrt(d) (d = 0: rational).  Small denominators are tried
    first, then quadratic irrationalities with small coefficients, then larger denominators,
    so that e.g. 0.6180339887... is recognised as (-1 + sqrt 5)/2 and not as a Fibonacci ratio."""
    for md in (64, 1000):
        f = Fr(x).limit_denominator(md)
        if abs(float(f) - x) < 1e-10:
            return (0, f, Fr(0))
    for d in ds:
        s = math.sqrt(d)
        for bden in range(1, 13):
            for bnum in range(-40, 41):
                if bnum == 0:
                    continue
                b = Fr(bnum, bden)
                a = Fr(x - float(b) * s).limit_denominator(1000)
                if abs(float(a) + float(b) * s - x) < 1e-10:
                    return (d, a, b)
    if maxden > 1000:
        f = Fr(x).limit_denominator(maxden)
        if abs(float(f) - x) < 1e-11:
            return (0, f, Fr(0))
    return None


def exactify(P, ds=(2, 3, 5, 6, 7, 13, 17, 21), maxden=1000):
    """P: numeric points (n x 3) -> (d, list of lines as integer pairs) or None."""
    out = []; dset = set()
    for p in P:
        k = int(np.argmax(np.abs(p)))
        q = p / p[k]
        trip = []
        for c in q:
            r = recognise(float(c), ds, maxden)
            if r is None:
                return None
            d, a, b = r
            if d:
                dset.add(d)
            trip.append((a, b))
        out.append(trip)
    if len(dset) > 1:
        return None
    d = dset.pop() if dset else 0
    lines = []
    for trip in out:
        den = 1
        for a, b in trip:
            den = den * a.denominator // math.gcd(den, a.denominator)
            den = den * b.denominator // math.gcd(den, b.denominator)
        v = [[int(a * den), int(b * den)] for a, b in trip]
        g = 0
        for a, b in v:
            g = math.gcd(g, abs(a)); g = math.gcd(g, abs(b))
        if g > 1:
            v = [[a // g, b // g] for a, b in v]
        lines.append(v)
    return d, lines


def realize_blocks(n, blocks, seed=0, starts=100, source="numerical realization + exact reconstruction"):
    """Return a verified certificate for the type of this linear space, or None."""
    sizes = sorted((len(B) for B in blocks), reverse=True)
    num = numeric_realization(n, blocks, seed=seed, starts=starts)
    if num is None:
        return None
    def attempt(ex):
        if ex is None:
            return None
        d, lines = ex
        cert = {"n": n, "type": sizes, "d": d, "lines": lines, "source": source}
        try:
            verify(cert)
        except Reject:
            return None
        return cert

    cert = attempt(exactify(num[0]))
    if cert is None:
        Q = snap_to_rationals(n, blocks, num[0])
        if Q is not None:
            cert = attempt(exactify(Q, maxden=10 ** 6))
    if cert is not None and cert["d"] != 0:
        cert["source"] += " (field Q(sqrt %d))" % cert["d"]
    return cert


if __name__ == "__main__":
    n = int(sys.argv[1])
    blocks = [list(map(int, b.split(","))) for b in sys.argv[2].split()]
    starts = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    c = realize_blocks(n, blocks, starts=starts)
    print(json.dumps(c) if c else "no exact realization found")
