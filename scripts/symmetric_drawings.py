"""Symmetric drawings for the gallery: for known types, a drawing with as much symmetry as we could find.

A pool is a symmetric set of lines of RP^2 (unit normals in R^3) together with a view axis c: the drawing is the
affine chart z = 1 in a basis whose third vector is c, so c is the centre of the picture.  Pools:
  * sides of regular k-gons and star k-gons (several radii) and the lines through the centre, k = 2 .. 12;
  * the planes perpendicular to the symmetry axes of the icosahedron (31) and of the octahedron (13), seen along an
    axis;
  * plane sections u^perp of the mirror arrangements F4, H4, B4, D4 (scripts/mirror_sections.py), seen along a line
    of the section.
The symmetry group G of the pool around c (rotations about c and a reflection in a plane through c) acts on the
lines; every union of G-orbits is a drawing with that symmetry.  Besides the full group we use its subgroup of odd
rotation order, and "tilted" views: c turned inside a mirror plane, which keeps that one reflection and moves points
away from the line at infinity.

A drawing is admissible only if no two of its lines are parallel (no intersection point at infinity; the problem
asks for lines without parallels), and its numerically computed type is a certified type.  For each type we keep the
drawing with the largest symmetry group, then the best ratio (smallest distance between intersection points) /
(largest distance from the centre).  The lines are scaled so that every intersection point lies in the unit disc.

The drawings are floating-point realizations of the type, not certificates: the certified coordinates are in
data/certificates, and the two arrangements need not be projectively equivalent.  scripts/build_gallery_data.py
checks every drawing with the same tolerance as the certified drawings.

usage: python scripts/symmetric_drawings.py [NMAX] [WORKERS]       -> data/symmetric_drawings.json
"""
import itertools, json, math, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from mirror_sections import roots, section

PHI = (1 + 5 ** 0.5) / 2
Z = np.array([0, 0, 1.0])
SYSTEM = {"F4": "F4 (the symmetries of the 24-cell)", "H4": "H4 (the symmetries of the 600-cell)", "B4": "B4 (the symmetries of the 4-cube)", "D4": "D4"}


def unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def dedupe(L):
    U = []
    for l in L:
        if np.linalg.norm(l) < 1e-9:
            continue
        l = unit(l)
        if all(np.linalg.norm(np.cross(l, m)) > 1e-9 for m in U):
            U.append(l)
    return U


def polygon_pool(k):
    L = []
    for m in range(4):
        r = math.cos(m * math.pi / k)
        if r <= 1e-9 or (m and 2 * m >= k):
            continue
        for off in (0.0, math.pi / k):
            L += [[math.cos(2 * math.pi * j / k + off), math.sin(2 * math.pi * j / k + off), -r] for j in range(k)]
    L += [[math.cos(math.pi * j / k), math.sin(math.pi * j / k), 0.0] for j in range(2 * k)]
    return dedupe(L)


def axes_pool(kind):
    if kind == "icosahedron":
        V = []
        for a in (-1, 1):
            for b in (-1, 1):
                V += [(0, a, b * PHI), (a, b * PHI, 0), (b * PHI, 0, a)]
        V = [unit(v) for v in V]
        g = 1 / 5 ** 0.5
        E = [a + b for a, b in itertools.combinations(V, 2) if abs(np.dot(a, b) - g) < 1e-9]
        F = [a + b + c for a, b, c in itertools.combinations(V, 3)
             if all(abs(np.dot(x, y) - g) < 1e-9 for x, y in ((a, b), (a, c), (b, c)))]
        return dedupe(V + E + F)
    E = np.eye(3)
    return dedupe(list(E) + [np.array(s, float) for s in itertools.product((1, -1), repeat=3)] +
                  [E[i] + s * E[j] for i, j in itertools.combinations(range(3), 2) for s in (1, -1)])


def rot(axis, t):
    a = unit(axis)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def preserves(M, L):
    return all(any(np.linalg.norm(np.cross(M @ l, m)) < 1e-8 for m in L) for l in L)


def mirror_through(L, c):
    for l in L:
        d = np.cross(c, l)
        if np.linalg.norm(d) > 1e-9:
            d = unit(d)
            if preserves(np.eye(3) - 2 * np.outer(d, d), L):
                return d
    return None


def group(L, c, odd):
    k = max(k for k in range(1, 13) if preserves(rot(c, 2 * math.pi / k), L))
    while odd and k % 2 == 0:
        k //= 2
    G = [rot(c, 2 * math.pi * j / k) for j in range(k)]
    d = mirror_through(L, c)
    if d is not None:
        G += [(np.eye(3) - 2 * np.outer(d, d)) @ g for g in G]
    return G, k


def orbits(L, G):
    seen, out = set(), []
    for i in range(len(L)):
        if i in seen:
            continue
        orb = {next(j for j in range(len(L)) if np.linalg.norm(np.cross(g @ L[i], L[j])) < 1e-8) for g in G}
        seen |= orb
        out.append(sorted(orb))
    return out


def pools():
    for k in range(2, 13):
        yield "polygon", k, polygon_pool(k), Z
    for kind in ("icosahedron", "octahedron"):
        P = axes_pool(kind)
        for c in P:
            yield kind, None, P, c
    for nm in ("F4", "H4", "B4", "D4"):
        R = roots(nm)
        for u in R[:12]:
            P = section(R, u)
            for c in P[:6]:
                yield nm, None, P, c


def views():
    for kind, k, P, c in pools():
        yield kind, k, P, c, "full"
        yield kind, k, P, c, "odd"
        d = mirror_through(P, c)
        if d is not None:
            e = unit(np.cross(d, c))
            for t in (0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 0.9):
                yield kind, k, P, unit(c * math.cos(t) + e * math.sin(t)), ("tilt", d)


def how(kind, k, mode, rot_order):
    if kind == "polygon":
        s = "Sides of a regular %d-gon and of its star polygons, and lines through its centre" % k
    elif kind in ("icosahedron", "octahedron"):
        s = "Planes perpendicular to symmetry axes of the %s, seen along an axis" % kind
    else:
        s = "A plane section of the mirrors of the 4-dimensional root system %s" % SYSTEM[kind]
    if mode == "tilt":
        s += "; seen at an angle within a mirror plane, which keeps one reflection and leaves no parallel lines"
    return s + "."


def chart(L, c):
    a = unit(np.cross(c, [0.3, 0.7, 0.1])); b = np.cross(c, a)
    M = [np.array([a, b, c]) @ l for l in L]
    ref = next((m for m in M if abs(m[2]) > 1e-9 and np.hypot(m[0], m[1]) > 1e-9), None)
    if ref is not None:                              # turn the picture so that one line is horizontal
        t = math.atan2(ref[1], ref[0]) - math.pi / 2
        Rz = np.array([[math.cos(t), math.sin(t), 0], [-math.sin(t), math.cos(t), 0], [0, 0, 1]])
        M = [Rz @ m for m in M]
    return M


def finish(M):
    """scale so that all intersection points lie in the unit disc; return (lines, spread) or None"""
    pts = []
    for i, j in itertools.combinations(range(len(M)), 2):
        p = np.cross(M[i], M[j])
        if abs(p[2]) < 1e-12 * np.linalg.norm(p):
            return None
        pts.append(p[:2] / p[2])
    P = np.array(pts)
    R = max(np.hypot(P[:, 0], P[:, 1]).max(), 1e-9)
    U = []
    for q in P:
        if all(np.hypot(*(q - u)) > 1e-7 * R for u in U):
            U.append(q)
    dmin = min((np.hypot(*(u - v)) for u, v in itertools.combinations(U, 2)), default=R)
    L = []
    for a, b, c in M:
        s = math.hypot(a, b)
        L.append([round(a / s, 7), round(b / s, 7), round(c / R / s, 7)])
    return L, dmin / R


def process(args):
    """best drawing per type within one view: {(n, type): record}"""
    kind, k, P, c, mode, nmax, certified = args
    if isinstance(mode, str):
        G, rk = group(P, c, mode == "odd")
        md = mode
    else:
        G, rk, md = [np.eye(3), np.eye(3) - 2 * np.outer(mode[1], mode[1])], 1, "tilt"
    O = orbits(P, G)
    best = {}
    if len(O) > 26:
        return best
    # intersection points of the pool as bitmasks (points at infinity separately)
    pts, inf, seenp = [], [], set()
    for i, j in itertools.combinations(range(len(P)), 2):
        p = unit(np.cross(P[i], P[j]))
        m = sum(1 << q for q in range(len(P)) if abs(np.dot(P[q], p)) < 1e-9)
        if m in seenp:
            continue
        seenp.add(m)
        (inf if abs(np.dot(p, c)) < 1e-6 else pts).append(m)
    bad = sum(1 << q for q in range(len(P)) if np.linalg.norm(np.cross(P[q], c)) < 1e-9)
    combos = []

    def rec(start, mask, size):
        if len(combos) > 200000:
            return
        if size >= 3:
            combos.append(mask)
        for o in range(start, len(O)):
            if size + len(O[o]) <= nmax:
                rec(o + 1, mask | sum(1 << q for q in O[o]), size + len(O[o]))
    rec(0, 0, 0)
    for mask in combos:
        if mask & bad or any(bin(mask & q).count("1") >= 2 for q in inf):
            continue                     # a line at infinity or two parallel lines
        n = bin(mask).count("1")
        t = tuple(sorted((x for x in (bin(mask & q).count("1") for q in pts) if x >= 3), reverse=True))
        if t not in certified.get(n, ()):
            continue
        if (n, t) in best:
            continue                     # one drawing per type and view; views compete in main()
        fin = finish(chart([P[q] for q in range(len(P)) if mask >> q & 1], c))
        if fin is None:
            continue
        L, spread = fin
        best[(n, t)] = {"symmetry": len(G), "rotation": rk, "spread": round(spread, 4),
                        "how": how(kind, k, md, rk), "L": L}
    return best


def main(nmax, workers):
    from multiprocessing import Pool
    certified = {}
    for n in range(3, nmax + 1):
        certified[n] = {tuple(c["type"]) for c in json.load(open(os.path.join(ROOT, "data", "certificates", "n%d.json" % n)))}
    jobs, seen = [], set()
    for kind, k, P, c, mode in views():
        key = (kind, k, len(P), tuple(np.round(c, 6)), mode if isinstance(mode, str) else "tilt")
        if key not in seen:
            seen.add(key)
            jobs.append((kind, k, P, c, mode, nmax, certified))
    print("%d views" % len(jobs), flush=True)
    best = {}
    with Pool(workers) as pool:
        for done, local in enumerate(pool.imap_unordered(process, jobs, chunksize=4), 1):
            for key, v in local.items():
                prev = best.get(key)
                if prev is None or (v["symmetry"], v["spread"]) > (prev["symmetry"], prev["spread"]):
                    best[key] = v
            if done % 200 == 0 or done == len(jobs):
                print("  %d / %d views, %d types" % (done, len(jobs), len(best)), flush=True)
    out = {}
    for (n, t), v in sorted(best.items()):
        out.setdefault(str(n), {})[",".join(map(str, t))] = v
    with open(os.path.join(ROOT, "data", "symmetric_drawings.json"), "w", newline="\n") as f:
        json.dump(out, f, separators=(",", ":"))
        f.write("\n")
    for n in range(3, nmax + 1):
        got = out.get(str(n), {})
        print("n=%2d: %3d of %3d types, %d with rotational symmetry" % (n, len(got), len(certified[n]),
              sum(1 for v in got.values() if v["rotation"] >= 3)))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 13, int(sys.argv[2]) if len(sys.argv) > 2 else 8)
