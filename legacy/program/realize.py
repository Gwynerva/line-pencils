# Numerically realise a linear space (given its blocks of size>=3) in the real projective plane,
# then try to recognise exact coordinates (rational or a + b sqrt d) and verify exactly.
import numpy as np, itertools, math, sys, json
from fractions import Fraction as Fr
from scipy.optimize import least_squares

def frame_choice(n, blocks):
    col = set()
    for B in blocks:
        for t in itertools.combinations(sorted(B), 3): col.add(t)
    for q in itertools.combinations(range(n), 4):
        if all(t not in col for t in itertools.combinations(q, 3)): return list(q), col
    return None, col

def realize(n, blocks, starts=200, seed=0):
    rng = np.random.default_rng(seed)
    fr, col = frame_choice(n, blocks)
    if fr is None: return None
    F = {fr[0]: [1,0,0], fr[1]: [0,1,0], fr[2]: [0,0,1], fr[3]: [1,1,1]}
    free = [i for i in range(n) if i not in F]
    trip = [t for B in blocks for t in itertools.combinations(sorted(B), 3)]
    noncol = [t for t in itertools.combinations(range(n), 3) if t not in col]
    def pts(z):
        P = np.zeros((n, 3))
        for i, v in F.items(): P[i] = v
        for k, i in enumerate(free): P[i] = z[3*k:3*k+3]
        return P
    def res(z):
        P = pts(z)
        Pn = P / np.linalg.norm(P, axis=1)[:, None]
        r = [np.linalg.det(Pn[list(t)]) for t in trip]
        r += [ (np.linalg.norm(P[i]) - 1.0) * 0.1 for i in free]  # scale gauge
        return np.array(r)
    best = None
    for s in range(starts):
        z0 = rng.normal(size=3*len(free))
        r = least_squares(res, z0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        P = pts(r.x); Pn = P / np.linalg.norm(P, axis=1)[:, None]
        e = max(abs(np.linalg.det(Pn[list(t)])) for t in trip) if trip else 0
        if e > 1e-11: continue
        m = min(abs(np.linalg.det(Pn[list(t)])) for t in noncol)
        if m < 1e-4: continue
        if best is None or m > best[1]: best = (Pn, m)
        if m > 1e-2: break
    return best

def recognise(x, ds=(0, 5, 2, 3, 6, 7), maxden=400):
    """find a + b sqrt(d) close to x with small denominators"""
    for d in ds:
        if d == 0:
            f = Fr(x).limit_denominator(maxden)
            if abs(float(f) - x) < 1e-9: return (0, f, Fr(0))
        else:
            s = math.sqrt(d)
            for bden in range(1, 13):
                for bnum in range(-40, 41):
                    if bnum == 0: continue
                    b = Fr(bnum, bden)
                    a = Fr(x - float(b) * s).limit_denominator(maxden)
                    if abs(float(a) + float(b) * s - x) < 1e-9: return (d, a, b)
    return None

def exactify(P):
    """P: numeric points (n x 3). Returns (d, exact points as triples of (Fr a, Fr b)) or None."""
    out = []; dset = set()
    for p in P:
        k = int(np.argmax(np.abs(p) > 1e-9))
        q = p / p[k]
        trip = []
        for c in q:
            r = recognise(float(c))
            if r is None: return None
            d, a, b = r
            if d: dset.add(d)
            trip.append((d, a, b))
        out.append(trip)
    if len(dset) > 1: return None
    d = dset.pop() if dset else 0
    return d, [[(a, b) for (_, a, b) in t] for t in out]

def certify(n, d, pts_frac, want_sig):
    import pool
    from pool import Pool, from_frac
    pool.D = d
    pts = [from_frac(tuple(p)) for p in pts_frac]
    P = Pool(pts, "cert", d)
    if len(P.pts) != n: return None
    sig = tuple(P.rich())
    return sig, P.pts
