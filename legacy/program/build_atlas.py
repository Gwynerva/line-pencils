# Build drawing data for the atlas page from exact certificates.
import json, sys, time, itertools, numpy as np, os, math
from db import load
from layout import layout, incidence_groups
from draw import lines_from_cert
from relax import relax, check

def groups_exact(cert):
    P = lines_from_cert(cert)
    G = incidence_groups(P, tol=1e-9)
    return [sorted(g[0]) for g in G]

def draw_one(n, sig, cert, seed=0):
    G = groups_exact(cert)
    if len(G) == 1:
        L = [[-math.sin(math.pi*k/n), math.cos(math.pi*k/n), 0.0] for k in range(n)]
        return {"lines": [[round(a,5), round(b,5), 0.0] for a,b,_ in L], "points": [[0.0, 0.0, list(range(n))]]}
    lay = layout(cert, tries=700, climb=700, seed=seed)
    L = np.array(lay["lines"])
    best = None
    if n >= 3:
        try:
            L2 = relax(L, G)
        except Exception:
            L2 = None
        if L2 is not None: best = L2
    if best is None:
        best = L
        if n >= 2 and not check(best, G, sep=1e-6): print("WARN layout check failed", n, sig, flush=True)
    # points
    pts = []
    for g in G:
        i, j = g[0], g[1]
        A = best[[i, j], :2]; X = np.linalg.solve(A, -best[[i, j], 2])
        pts.append([round(float(X[0]), 4), round(float(X[1]), 4), g])
    lines = [[round(float(a), 5), round(float(b), 5), round(float(c), 5)] for a, b, c in best]
    return {"lines": lines, "points": pts}

if __name__ == "__main__":
    nmax = int(sys.argv[1]); out = sys.argv[2]
    db = load()
    data = json.load(open(out)) if os.path.exists(out) else {}
    t0 = time.time()
    for n in range(1, nmax + 1):
        key = str(n)
        data.setdefault(key, {})
        if n == 1:
            data[key]["[]"] = {"lines": [[0, 1, 0]], "points": [], "d": 0}; continue
        if n == 2:
            data[key]["[]"] = {"lines": [[0.6, 0.8, 0], [-0.8, 0.6, 0]], "points": [[0, 0, [0, 1]]], "d": 0}; continue
        for sig, cert in sorted(db.get(n, {}).items()):
            k = json.dumps(list(sig))
            if k in data[key]: continue
            dd = draw_one(n, sig, cert)
            dd["d"] = cert["d"]
            data[key][k] = dd
        json.dump(data, open(out, "w"))
        print(n, len(data[key]), f"{time.time()-t0:.0f}s", flush=True)
