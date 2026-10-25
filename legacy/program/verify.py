# Independent re-verification of every certificate: recompute the pencil multiset exactly.
import json, sys
from math import comb
import pool
from pool import Pool
from db import load
db = load()
bad = 0; tot = 0
for n, m in sorted(db.items()):
    for sig, cert in m.items():
        tot += 1
        d = cert["d"]; pool.D = d
        pts = [tuple(tuple(c) for c in p) for p in cert["points"]]
        P = Pool(pts, "v", d)
        ok = len(P.pts) == n and tuple(P.rich()) == tuple(sig)
        # pairs check: every pair of points on exactly one spanned line (automatic), sum check
        if ok:
            s2 = sum(comb(len(L), 2) for L in P.lines)
            ok = s2 == comb(n, 2)
        if not ok:
            bad += 1; print("BAD", n, sig, cert["src"])
print("verified", tot, "certificates,", bad, "bad")
