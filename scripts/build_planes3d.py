"""Scenes for the interactive plane drawings on docs/planes.md (docs/javascripts/planes3d.js).

usage: python scripts/build_planes3d.py      -> docs/assets/data/planes3d.json

Each scene starts from integer planes a x + b y + c z + d w = 0.  Its lines and points (with the planes through them)
are computed exactly (scripts/planes_verify.py).  Then a projective transformation is chosen so that every point is
finite and the drawing is legible: a random search maximizing the smallest distance between two points and the
smallest angle between two planes, relative to the size of the configuration (scenes in FIXED are drawn as given).  The output stores, in the new
affine coordinates, the planes (unit normal, offset), the points and the lines (each with the planes through it),
and the radius of the ball to which the planes are clipped; the whole configuration lies well inside the ball.
"""
import json
import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from planes_verify import flats_of_rank, rank  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCENES = {
    # two skew lines, each on three planes, drawn as they are (FIXED): lines {3^2}, points [4{3}^6]
    "skew": [[0, 1, 0, 0], [0, 1, 1, 1], [0, 1, -1, -1], [1, 0, 0, 0], [1, 0, 1, -1], [1, 0, -1, 1]],
    # three planes through a line and two more: lines {3}, points [4{3}^2]
    "book": [[1, 0, 0, 0], [1, 2, 0, 0], [1, -2, 0, 0], [0, 1, 4, -2], [1, -1, 3, 2]],
    # four planes through a point, no three through a line: lines {}, points [4{}]
    "four": [[1, 1, 1, 0], [1, -1, -1, 0], [-1, 1, -1, 0], [-1, -1, 1, 0]],
    # the six mirror planes of a regular tetrahedron and one more plane: lines {3^4}, points [6{3^4}, 4{3}^4]
    "mirrors": [[1, -1, 0, 0], [1, 1, 0, 0], [1, 0, -1, 0], [1, 0, 1, 0], [0, 1, -1, 0], [0, 1, 1, 0], [3, 5, 7, -9]],
}
FIXED = {"skew"}  # symmetric scenes kept as they are (all their points are finite)


def structure(V):
    lines = sorted(sorted(L) for L in flats_of_rank(V, 2))
    points = sorted(sorted(P) for P in flats_of_rank(V, 3)) if rank(V) >= 3 else []
    return lines, points


def homog_point(V, P):
    """The point (x : y : z : w) on the planes P: a null vector of their rows."""
    A = np.array([V[i] for i in P], float)
    return np.linalg.svd(A)[2][-1]


def score(Vt, pts_h, normals_only=False):
    X = []
    for p in pts_h:
        if abs(p[3]) < 1e-6 * np.linalg.norm(p):
            return -1, None
        X.append(p[:3] / p[3])
    X = np.array(X)
    c = X.mean(axis=0)
    size = max(np.linalg.norm(X - c, axis=1).max(), 1e-9)
    if len(X) > 1:
        dmin = min(np.linalg.norm(a - b) for a, b in combinations(X, 2)) / size
    else:
        dmin = 1.0
    N = [v[:3] / np.linalg.norm(v[:3]) for v in Vt]
    amin = min(np.arccos(min(1.0, abs(a @ b))) for a, b in combinations(N, 2))
    return min(dmin, 1.4 * amin), (X, c, size)


def best_view(V, points, trials=4000, seed=1, fixed=False):
    rng = np.random.default_rng(seed)
    Vh = np.array(V, float)
    pts_h = [homog_point(V, P) for P in points]
    best = (-2, None, None)

    def attempt(M):
        nonlocal best
        if abs(np.linalg.det(M)) < 1e-3:
            return
        Vt = Vh @ np.linalg.inv(M)
        s, info = score(Vt, [M @ p for p in pts_h])
        if s > best[0]:
            best = (s, (Vt, info), M)

    if fixed:
        attempt(np.eye(4))
        return best[:2]
    for t in range(trials):  # random start, then a hill climb with shrinking steps
        attempt(np.eye(4) if t == 0 else np.eye(4) + rng.normal(scale=0.6, size=(4, 4)))
    for t in range(trials):
        attempt(best[2] + rng.normal(scale=0.25 * (1 - t / trials) + 0.01, size=(4, 4)))
    return best[:2]


def build(name, V):
    lines, points = structure(V)
    s, (Vt, (X, c, size)) = best_view(V, points, fixed=name in FIXED)
    if not points:
        c, size = np.zeros(3), 1.0
    out = {"name": name, "planes": [], "points": [], "lines": []}
    for v in Vt:
        n = v[:3]
        d = -(v[3] + n @ c)  # plane n.(x + c) + v3 = 0  ->  n.x = d  in centred coordinates
        k = np.linalg.norm(n)
        out["planes"].append([*(n / k / 1.0), d / k / size])
    for P, x in zip(points, X if points else []):
        out["points"].append({"at": list((x - c) / size), "on": P})
    for L in lines:
        a, b = Vt[L[0]], Vt[L[1]]
        u = np.cross(a[:3], b[:3])
        u /= np.linalg.norm(u)
        # a point of the line, in centred and scaled coordinates
        pa = out["planes"][L[0]]
        pb = out["planes"][L[1]]
        A = np.array([pa[:3], pb[:3], u])
        x0 = np.linalg.solve(A, [pa[3], pb[3], 0])
        out["lines"].append({"at": list(x0), "dir": list(u), "on": L})
    out["R"] = 1.35 if points else 1.0
    print(f"{name}: {len(V)} planes, {len(lines)} lines, {len(points)} points, legibility {s:.3f}")
    return out


def main():
    scenes = {name: build(name, V) for name, V in SCENES.items()}
    path = os.path.join(ROOT, "docs", "assets", "data", "planes3d.json")
    with open(path, "w") as fh:
        json.dump(scenes, fh, separators=(",", ":"))
    print("wrote", path)


if __name__ == "__main__":
    main()
