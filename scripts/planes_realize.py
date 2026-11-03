"""Integer realizations of simple matroids of rank <= 4 (arrangements of planes in RP^3).

A plane a x + b y + c z + d w = 0 is stored as the integer vector (a, b, c, d).  The matroid of the planes (rank of a
set = rank of its vectors) is the intersection lattice.  Realizations are searched constructively: elements are
placed one at a time in a random order; each new vector is a random integer point of the intersection of the spans
of the already placed parts of the flats that must contain it.  A candidate is accepted only if its matroid,
recomputed in exact arithmetic, equals the target.  This finds every matroid that has such a construction sequence;
the others are reported as unresolved and treated separately.

usage: python scripts/planes_realize.py N   (reads runs/planes_matroids_n{N}.json, writes runs/planes_real_n{N}.json)
"""

import json
import math
import random
import sys
from fractions import Fraction

sys.path.insert(0, "scripts")
import planes_matroids as pm  # noqa: E402


def rank(vecs):
    rows = [[Fraction(x) for x in v] for v in vecs]
    r = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def nullspace(rows, ncol):
    """Basis of {x : rows . x = 0} over Q."""
    A = [[Fraction(x) for x in v] for v in rows]
    piv_cols = []
    r = 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        A[r] = [a / A[r][c] for a in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
    free = [c for c in range(ncol) if c not in piv_cols]
    basis = []
    for fcol in free:
        x = [Fraction(0)] * ncol
        x[fcol] = Fraction(1)
        for i, pc in enumerate(piv_cols):
            x[pc] = -A[i][fcol]
        basis.append(x)
    return basis


def matroid_of(vecs):
    """Flats of the matroid of the vectors, by rank (exact)."""
    n = len(vecs)
    rk = {}
    for mask in range(1 << n):
        rk[mask] = rank([vecs[i] for i in range(n) if mask >> i & 1]) if mask else 0
    flats = {}
    for mask in range(1 << n):
        if all(rk[mask | (1 << i)] > rk[mask] for i in range(n) if not mask >> i & 1):
            flats.setdefault(rk[mask], set()).add(mask)
    return {k: frozenset(v) for k, v in flats.items()}


def closure(flats, X):
    c = None
    for s in flats.values():
        for F in s:
            if F & X == X and (c is None or pm.popcount(F) < pm.popcount(c)):
                c = F
    return c


def try_realize(n, flats, rng, coef=3):
    order = list(range(n))
    rng.shuffle(order)
    allf = [F for s in flats.values() for F in s]
    vecs = {}
    placed = 0
    for j in order:
        b = 1 << j
        eqs = []
        for F in allf:
            if not F & b:
                continue
            X = F & placed
            if X == 0 or not (closure(flats, X) & b):
                continue
            V = [vecs[i] for i in range(n) if X >> i & 1]
            eqs.extend(nullspace(V, 4))  # equations of span(V)
        basis = nullspace(eqs, 4) if eqs else [[Fraction(int(i == k)) for i in range(4)] for k in range(4)]
        if not basis:
            return None
        for _ in range(20):
            cs = [rng.randint(-coef, coef) for _ in basis]
            v = [sum(c * bv[i] for c, bv in zip(cs, basis)) for i in range(4)]
            if any(v):
                break
        else:
            return None
        den = 1
        for x in v:
            den = den * x.denominator // math.gcd(den, x.denominator)
        v = [int(x * den) for x in v]
        g = 0
        for x in v:
            g = math.gcd(g, x)
        vecs[j] = [x // g for x in v]
        placed |= b
    return [vecs[i] for i in range(n)]


def realize(n, flats, tries=300, seed=1):
    rng = random.Random(seed)
    target = {k: set(v) for k, v in flats.items()}
    for t in range(tries):
        v = try_realize(n, flats, rng, coef=2 + t // 50)
        if v is None:
            continue
        got = matroid_of(v)
        if {k: set(s) for k, s in got.items()} == target:
            return v
    return None


if __name__ == "__main__":
    N = int(sys.argv[1])
    levels = pm.load(f"runs/planes_matroids_n{N}.json")
    out = {}
    for n in sorted(levels):
        res = []
        bad = 0
        for flats in levels[n]:
            v = realize(n, flats)
            bad += v is None
            res.append(v)
        out[n] = res
        print(f"n={n}: {len(res)} matroids, {len(res) - bad} realized, {bad} unresolved", flush=True)
    with open(f"runs/planes_real_n{N}.json", "w") as fh:
        json.dump(out, fh)
