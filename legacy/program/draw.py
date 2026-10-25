# Turn a certificate (points in RP^2, exact) into a nice drawing of LINES (projective duality):
# point (a:b:c)  ->  line a x + b y + c = 0.  Pencils of k lines <-> lines through k points.
import numpy as np, math, json, itertools

def num(c, d):
    a, b = c
    return a + b * math.sqrt(d) if d else float(a)

def lines_from_cert(cert):
    d = cert["d"]
    P = np.array([[num(c, d) for c in p] for p in cert["points"]], float)
    P /= np.linalg.norm(P, axis=1)[:, None]
    return P

def groups(L, tol=1e-7):
    """intersection points of lines L (rows are line coords): returns list of (xyz, set of line idx)"""
    n = len(L); pts = []
    for i, j in itertools.combinations(range(n), 2):
        X = np.cross(L[i], L[j]); X /= np.linalg.norm(X)
        for g in pts:
            if np.linalg.norm(np.cross(g[0], X)) < tol:
                g[1].update((i, j)); break
        else:
            pts.append([X, {i, j}])
    return pts

def layout_score(L, G):
    # affine intersection points must be finite and well spread
    X = np.array([g[0] for g in G])
    z = X[:, 2]
    if np.min(np.abs(z)) < 1e-9: return -1, None
    A = X[:, :2] / z[:, None]
    c = A.mean(0); A0 = A - c
    R = np.max(np.linalg.norm(A0, axis=1))
    if R == 0: return -1, None
    A0 /= R
    if len(A0) == 1: return 1.0, A0
    D = np.linalg.norm(A0[:, None, :] - A0[None, :, :], axis=2) + np.eye(len(A0)) * 9
    dmin = D.min()
    # angles between lines: avoid near-parallel lines
    ang = np.arctan2(-L[:, 0], L[:, 1]) % math.pi
    s = np.sort(ang); gaps = np.diff(np.concatenate([s, [s[0] + math.pi]]))
    amin = gaps.min() if len(L) > 1 else 1
    # distance from each line to the points not on it should not be tiny either
    return dmin * (0.3 + min(amin, 0.5)), A0

def best_layout(P, tries=1500, seed=0):
    rng = np.random.default_rng(seed)
    n = len(P)
    if n == 1:
        return np.array([[0.0, 1.0, 0.0]]), []
    best = (-2, None, None)
    M0 = np.eye(3)
    for t in range(tries):
        if t < tries // 2 or best[1] is None:
            M = rng.normal(size=(3, 3))
        else:
            M = best[1] + rng.normal(scale=0.15, size=(3, 3))
        L = P @ M.T
        L /= np.linalg.norm(L, axis=1)[:, None]
        G = groups(L)
        sc, A = layout_score(L, G)
        if sc > best[0]: best = (sc, M, (L, G, A))
    L, G, A = best[2]
    return best
