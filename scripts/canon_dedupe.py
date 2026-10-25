"""Exact isomorphism classes for the orientable linear spaces of a type with a UNIQUE largest block B (size s),
all other blocks meeting B in at most one point (automatic), by a canonical form.

Structure: points off B form the set X (|X| = n - s).  Every other block is {q} ∪ Y with q ∈ B, Y ⊆ X, or Y ⊆ X alone.
An isomorphism must map B to B and X to X, and the blocks through q are determined by the set of pairs of X they
cover.  So the space is encoded as the multiset of pair-masks {mask(q) : q ∈ B} (a mask has one bit per pair of
X, set iff the pair lies in a block through q) together with the mask of pairs in blocks inside X.  The canonical
form is the lexicographic minimum over all permutations of X of (sorted q-masks, X-mask); permutations of B are free
because the q-masks are taken as a multiset.  Exact and fast (numpy table of pair permutations).

usage: python scripts/canon_dedupe.py N ENUMFILE OUT.json
"""
import itertools, json, sys
import numpy as np

n = int(sys.argv[1]); fn = sys.argv[2]; out = sys.argv[3]

classes = {}   # canonical key -> [blocks, count]
total = 0
tables = {}


def tables_for(xs):
    """for X of size t: pair index, and the (t! x C(t,2)) permutation table of pair indices"""
    t = len(xs)
    if t in tables:
        return tables[t]
    pairs = list(itertools.combinations(range(t), 2))
    pidx = {p: i for i, p in enumerate(pairs)}
    perms = list(itertools.permutations(range(t)))
    P = np.zeros((len(perms), len(pairs)), dtype=np.int64)
    for a, sig in enumerate(perms):
        for i, (u, v) in enumerate(pairs):
            P[a, i] = pidx[tuple(sorted((sig[u], sig[v])))]
    tables[t] = (pairs, pidx, P)
    return tables[t]


for line in open(fn):
    if not line.startswith("ORIENTABLE"):
        continue
    total += 1
    blocks = [sorted(map(int, b.split(","))) for b in line.split()[1:]]
    B = max(blocks, key=len)
    assert sum(1 for b in blocks if len(b) == len(B)) == 1, "largest block not unique"
    xs = [p for p in range(n) if p not in B]
    xi = {p: i for i, p in enumerate(xs)}
    pairs, pidx, P = tables_for(xs)
    npairs = len(pairs)
    # bit-vector representation: rows = masks (one per q in B, plus one for X-only blocks), columns = pairs
    M = np.zeros((len(B) + 1, npairs), dtype=np.uint8)
    for b in blocks:
        if b is B:
            continue
        qs = [p for p in b if p in B]
        ys = [xi[p] for p in b if p not in B]
        row = B.index(qs[0]) if qs else len(B)
        for u, v in itertools.combinations(sorted(ys), 2):
            M[row, pidx[(u, v)]] = 1
    # apply all permutations: permuted mask bits M[:, P[a]] ; pack into integers
    weights = (1 << np.arange(npairs, dtype=np.int64))
    best = None
    perm_masks = M[:, P]                      # shape (rows, nperm, npairs)
    ints = (perm_masks.astype(np.int64) * weights).sum(axis=2)   # (rows, nperm)
    qpart = np.sort(ints[:-1, :], axis=0)      # sorted q-masks per permutation
    keyarr = np.vstack([qpart, ints[-1:, :]])  # (rows, nperm)
    # lexicographic minimum over permutations
    order = np.lexsort(keyarr[::-1])          # lexsort uses last key as primary -> reverse rows
    a = order[0]
    key = tuple(int(v) for v in keyarr[:, a])
    if key in classes:
        classes[key][1] += 1
    else:
        classes[key] = [blocks, 1]
reps = [{"blocks": v[0], "labelled_count": v[1]} for v in classes.values()]
json.dump({"n": n, "source": fn, "labelled_total": total, "classes": reps, "method": "canonical form over permutations of the points off the unique largest block"}, open(out, "w"), indent=1)
print("labelled orientable linear spaces:", total, "; isomorphism classes:", len(reps), [r["labelled_count"] for r in reps])
