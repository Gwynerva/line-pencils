# Exact-symmetric drawing of {5, 3^10, 2^5}: regular pentagram + its 5 symmetry axes.
import numpy as np, itertools, json
tips = [np.array([np.cos(np.pi/2 + 2*np.pi*i/5), np.sin(np.pi/2 + 2*np.pi*i/5)]) for i in range(5)]
def line_through(p, q):
    a, b = q[1]-p[1], p[0]-q[0]; c = -(a*p[0] + b*p[1]); n = np.hypot(a, b); return [a/n, b/n, c/n]
L = [line_through(tips[i], tips[(i+2) % 5]) for i in range(5)]          # pentagram
L += [line_through(np.zeros(2), tips[i]) for i in range(5)]              # axes
L = np.array(L)
pts = []
for i, j in itertools.combinations(range(10), 2):
    X = np.linalg.solve(L[[i, j], :2], -L[[i, j], 2])
    for g in pts:
        if np.linalg.norm(g[0] - X) < 1e-9: g[1].update((i, j)); break
    else: pts.append([X, {i, j}])
R = max(np.linalg.norm(g[0]) for g in pts)
s = 1.0 / R
L2 = L.copy(); L2[:, 2] *= s
out = {"lines": [[round(float(a), 6), round(float(b), 6), round(float(c), 6)] for a, b, c in L2],
       "points": [[round(float(g[0][0]*s), 5), round(float(g[0][1]*s), 5), sorted(g[1])] for g in pts]}
from collections import Counter
print(Counter(len(g[1]) for g in pts), "R", R)
json.dump(out, open("star.json", "w"))
