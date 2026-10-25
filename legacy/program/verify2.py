# Second, independent verifier (no shared code): exact 3x3 determinants in Z[sqrt d],
# lines reconstructed as maximal collinear sets from pairs.
import json, itertools
from math import comb
raw = json.load(open("realized.json"))
def mul(x, y, d): return (x[0]*y[0] + d*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def det(p, q, r, d):
    def m(a, b): return mul(a, b, d)
    def s(a, b): return (a[0]-b[0], a[1]-b[1])
    def a_(a, b): return (a[0]+b[0], a[1]+b[1])
    t1 = m(p[0], s(m(q[1], r[2]), m(q[2], r[1])))
    t2 = m(p[1], s(m(q[0], r[2]), m(q[2], r[0])))
    t3 = m(p[2], s(m(q[0], r[1]), m(q[1], r[0])))
    v = a_(s(t1, t2), t3)
    return v == (0, 0)
bad = 0; tot = 0
for n, m in raw.items():
    n = int(n)
    for key, cert in m.items():
        tot += 1
        d = cert["d"]; P = [tuple(tuple(c) for c in p) for p in cert["points"]]
        sig = tuple(json.loads(key))
        # distinct points: no two proportional -> check via cross product zero = det with random third? use 2x2 minors
        ok = len(P) == n
        for i, j in itertools.combinations(range(n), 2):
            p, q = P[i], P[j]
            minors = [(mul(p[a], q[b], d)[0]-mul(p[b], q[a], d)[0], mul(p[a], q[b], d)[1]-mul(p[b], q[a], d)[1]) for a, b in ((0,1),(0,2),(1,2))]
            if all(x == (0, 0) for x in minors): ok = False
        lines = {}
        for i, j in itertools.combinations(range(n), 2):
            S = frozenset([i, j] + [k for k in range(n) if k not in (i, j) and det(P[i], P[j], P[k], d)])
            lines[S] = 1
        sizes = tuple(sorted((len(S) for S in lines if len(S) >= 3), reverse=True))
        if not ok or sizes != sig:
            bad += 1; print("BAD", n, sig, sizes)
print("second verifier:", tot, "certificates,", bad, "bad")
