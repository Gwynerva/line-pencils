# Spread out a line arrangement while keeping exactly its pencil structure.
import numpy as np, math, itertools
from scipy.optimize import minimize

def lines_to_tr(L):
    # L rows (a,b,c): a x + b y + c = 0  ->  cos t x + sin t y = r
    out = []
    for a, b, c in L:
        nrm = math.hypot(a, b); a, b, c = a/nrm, b/nrm, c/nrm
        out += [math.atan2(b, a), -c]
    return np.array(out)

def tr_to_lines(v):
    t = v[0::2]; r = v[1::2]
    return np.stack([np.cos(t), np.sin(t), -r], axis=1)

def inter(L, i, j):
    A = np.array([L[i, :2], L[j, :2]]); b = -np.array([L[i, 2], L[j, 2]])
    return np.linalg.solve(A, b)

class Relaxer:
    def __init__(self, groups, n):
        self.n = n
        self.groups = [sorted(g) for g in groups]
        self.rich = [g for g in self.groups if len(g) >= 3]
        self.rep = [(g[0], g[1]) for g in self.groups]
        self.member = np.zeros((len(self.groups), n), bool)
        for gi, g in enumerate(self.groups):
            for k in g: self.member[gi, k] = True
    def points(self, L):
        P = []
        for i, j in self.rep:
            det = L[i,0]*L[j,1] - L[i,1]*L[j,0]
            if abs(det) < 1e-12: det = 1e-12
            x = (-L[i,2]*L[j,1] + L[j,2]*L[i,1]) / det
            y = (-L[i,0]*L[j,2] + L[j,0]*L[i,2]) / det
            P.append((x, y))
        return np.array(P)
    def residuals(self, v):
        L = tr_to_lines(v); res = []
        P = self.points(L)
        for gi, g in enumerate(self.groups):
            if len(g) < 3: continue
            x, y = P[gi]
            for k in g[2:]: res.append(L[k,0]*x + L[k,1]*y + L[k,2])
        return np.array(res)
    def energy(self, v, mu=1e4):
        L = tr_to_lines(v); P = self.points(L)
        E = 0.0
        if len(P) > 1:
            D2 = ((P[:, None] - P[None]) ** 2).sum(-1) + np.eye(len(P))
            iu = np.triu_indices(len(P), 1)
            E += (1.0 / (D2[iu] + 1e-4)).sum() / len(iu[0])
        dist = P @ L[:, :2].T + L[:, 2][None, :]
        dd = np.where(self.member, 1.0, dist**2)
        E += 0.5 * (1.0 / (dd + 1e-4)).sum() / dd.size
        rad = np.sqrt((P**2).sum(1))
        E += 50 * (np.maximum(0, rad - 1.0) ** 2).sum()
        res = self.residuals(v)
        E += mu * (res**2).sum()
        return E
    def project(self, v, iters=60):
        # Gauss-Newton on the concurrency constraints only (min-norm steps)
        for _ in range(iters):
            r = self.residuals(v)
            if r.size == 0 or np.max(np.abs(r)) < 1e-14: break
            J = np.zeros((len(r), len(v))); h = 1e-7
            for k in range(len(v)):
                e = np.zeros(len(v)); e[k] = h
                J[:, k] = (self.residuals(v + e) - self.residuals(v - e)) / (2*h)
            step, *_ = np.linalg.lstsq(J, -r, rcond=None)
            v = v + step
        return v

def check(L, groups, tol=1e-9, sep=2e-3):
    """Recompute the intersection structure numerically and compare."""
    n = len(L)
    pts = []
    for i, j in itertools.combinations(range(n), 2):
        A = np.array([L[i, :2], L[j, :2]])
        if abs(np.linalg.det(A)) < 1e-9: return False
        X = np.linalg.solve(A, -np.array([L[i, 2], L[j, 2]]))
        pts.append((X, {i, j}))
    # cluster
    cl = []
    for X, s in pts:
        for c in cl:
            if np.linalg.norm(c[0] - X) < 1e-7: c[1].update(s); break
        else: cl.append([X, set(s)])
    got = sorted(sorted(c[1]) for c in cl)
    want = sorted(sorted(g) for g in groups)
    if got != want: return False
    C = np.array([c[0] for c in cl])
    if len(C) > 1:
        D = np.linalg.norm(C[:, None] - C[None], axis=2) + 9*np.eye(len(C))
        if D.min() < sep: return False
    # no point too close to a line it is not on
    for X, s in cl:
        for k in range(n):
            if k not in s and abs(L[k,0]*X[0] + L[k,1]*X[1] + L[k,2]) < sep: return False
    return True

def relax(lines, groups, maxiter=400):
    n = len(lines)
    R = Relaxer(groups, n)
    v0 = lines_to_tr(np.array(lines))
    res = minimize(R.energy, v0, method="L-BFGS-B", options={"maxiter": maxiter})
    v = R.project(res.x)
    L = tr_to_lines(v)
    P = R.points(L)
    # normalise into the unit disk
    c = P.mean(0); s = np.max(np.linalg.norm(P - c, axis=1))
    L2 = L.copy(); L2[:, 2] = (L[:, 2] + L[:, :2] @ c) / s
    if check(L2, groups): return L2
    return None
