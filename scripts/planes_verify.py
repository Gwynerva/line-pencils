"""Independent check of the plane-arrangement certificates.

Reads runs/planes_certificates.json: for each n a list of entries {"type": ..., "planes": [[a, b, c, d], ...]},
the plane a x + b y + c z + d w = 0 in RP^3.  For every entry the type is recomputed from the integer vectors alone
(exact integer arithmetic, no code shared with the enumeration):

  lines  = maximal sets of >= 2 planes whose normal vectors span a 2-space,
  points = maximal sets of >= 3 planes whose normal vectors span a 3-space,

and the entry is accepted only if the planes are distinct and the recomputed type equals the stored one.  Finally the
number of distinct accepted types per n is printed.

usage: python scripts/planes_verify.py [runs/planes_certificates.json]
"""

import json
import sys
from itertools import combinations


def rank(rows):
    """Rank of an integer matrix by fraction-free Gaussian elimination."""
    M = [list(r) for r in rows]
    r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(r + 1, len(M)):
            if M[i][c]:
                a, b = M[r][c], M[i][c]
                M[i] = [a * x - b * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


def flats_of_rank(V, k):
    """Maximal subsets S with rank(V[S]) = k and |S| >= k, i.e. the rank-k flats spanned by planes."""
    n = len(V)
    found = set()
    for base in combinations(range(n), k):
        if rank([V[i] for i in base]) < k:
            continue
        S = frozenset(i for i in range(n) if rank([V[j] for j in base] + [V[i]]) == k)
        found.add(S)
    return found


def recompute(V):
    n = len(V)
    for i, j in combinations(range(n), 2):
        if rank([V[i], V[j]]) < 2:
            raise ValueError(f"planes {i} and {j} coincide")
    lines = flats_of_rank(V, 2)
    points = flats_of_rank(V, 3) if rank(V) >= 3 else set()
    lam = sorted((len(L) for L in lines if len(L) >= 3), reverse=True)
    pts = []
    for P in points:
        if len(P) >= 4:
            tau = sorted((len(L) for L in lines if L <= P and len(L) >= 3), reverse=True)
            pts.append([len(P), tau])
    pts.sort(reverse=True)
    return {"lines": lam, "points": pts, "f1": len(lines), "f0": len(points)}


def main(path):
    with open(path) as fh:
        data = json.load(fh)
    total_bad = 0
    for n, entries in sorted(data.items(), key=lambda kv: int(kv[0])):
        seen = set()
        bad = 0
        for e in entries:
            V = e["planes"]
            assert len(V) == int(n)
            got = recompute(V)
            claimed = e["type"]
            if got["lines"] != claimed["lines"] or got["points"] != claimed["points"]:
                bad += 1
                print(f"n={n}: MISMATCH claimed {claimed} got {got}")
                continue
            seen.add(json.dumps([got["lines"], got["points"]]))
        total_bad += bad
        print(f"n={n}: {len(entries)} certificates, {len(seen)} distinct verified types, {bad} rejected")
    sys.exit(1 if total_bad else 0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "runs/planes_certificates.json")
