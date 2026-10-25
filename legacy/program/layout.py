# Nice drawings of line arrangements from point certificates (projective duality).
import numpy as np, math, itertools, json
from draw import lines_from_cert

def incidence_groups(P, tol=1e-8):
    """Groups of lines (dual points P) through a common point. Returns list of (index set, point)."""
    n = len(P); out = []
    for i, j in itertools.combinations(range(n), 2):
        X = np.cross(P[i], P[j]); X /= np.linalg.norm(X)
        for g in out:
            if i in g[0] and j in g[0]: break
        else:
            S = {k for k in range(n) if abs(P[k] @ X) < tol}
            out.append((S, X))
    return out

def evaluate(P, X0, M, members):
    L = P @ M.T
    Minv_T = np.linalg.inv(M).T
    X = X0 @ Minv_T.T
    if np.min(np.abs(X[:, 2]) / np.linalg.norm(X, axis=1)) < 1e-6: return -1, None
    A = X[:, :2] / X[:, 2:3]
    c = A.mean(0)
    C = np.cov((A - c).T) + 1e-12*np.eye(2) if len(A) > 2 else np.eye(2)
    w, V = np.linalg.eigh(C)
    if w.min() <= 0: return -1, None
    T = V @ np.diag(1/np.sqrt(w)) @ V.T
    B = (A - c) @ T.T
    R = np.max(np.linalg.norm(B, axis=1))
    if R == 0: return -1, None
    B /= R
    # transform lines with the same affine map: point u -> T(u-c)/R
    # line a x + b y + c0 = 0 in old coords; new coords v: u = R T^{-1} v + c
    Ti = np.linalg.inv(T) * R
    Ln = np.empty_like(L)
    Ln[:, :2] = L[:, :2] @ Ti
    Ln[:, 2] = L[:, :2] @ c + L[:, 2]
    Ln /= np.linalg.norm(Ln[:, :2], axis=1)[:, None]
    if len(B) > 1:
        D = np.linalg.norm(B[:, None] - B[None], axis=2) + 9*np.eye(len(B))
        dmin = D.min()
    else: dmin = 1
    # clearance: point to non-incident line
    dist = np.abs(B @ Ln[:, :2].T + Ln[:, 2][None, :])   # points x lines
    mask = members  # True where line passes through point
    dd = np.where(mask, 9, dist)
    clear = dd.min() if dd.size else 1
    ang = np.arctan2(Ln[:, 1], Ln[:, 0]) % math.pi
    s = np.sort(ang); gaps = np.diff(np.concatenate([s, [s[0] + math.pi]]))
    agap = gaps.min()
    score = min(dmin, 2*clear) * min(1.0, agap / 0.12)
    return score, (Ln, B)

def layout(cert, tries=2500, climb=2500, seed=0):
    P = lines_from_cert(cert)
    n = len(P)
    rng = np.random.default_rng(seed)
    if n == 1:
        return {"lines": [[1.0, 0.0, 0.0]], "points": []}
    G = incidence_groups(P)
    X0 = np.array([g[1] for g in G])
    members = np.array([[k in g[0] for k in range(n)] for g in G])
    best = (-2, None, None)
    for t in range(tries):
        M = rng.normal(size=(3, 3))
        sc, res = evaluate(P, X0, M, members)
        if sc > best[0]: best = (sc, M, res)
    step = 0.3
    for t in range(climb):
        M = best[1] + rng.normal(scale=step, size=(3, 3))
        sc, res = evaluate(P, X0, M, members)
        if sc > best[0]: best = (sc, M, res)
        if t % 500 == 499: step *= 0.6
    Ln, B = best[2]
    pts = [[round(float(B[i, 0]), 4), round(float(B[i, 1]), 4), len(G[i][0])] for i in range(len(G))]
    lines = [[round(float(a), 5), round(float(b), 5), round(float(c), 5)] for a, b, c in Ln]
    return {"lines": lines, "points": pts, "score": round(float(best[0]), 4)}
