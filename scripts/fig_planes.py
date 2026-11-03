"""Static figure for the page on planes in space (docs/planes.md): the local arrangement at a point, as great
circles on a sphere.  The rotating drawings on that page are made by docs/javascripts/planes3d.js.

usage: python scripts/fig_planes.py     -> snippets/fig/planes-sphere.svg

Colours come from CSS classes (docs/stylesheets/extra.css), so the figure follows the light and dark themes.
"""
import math
import os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "snippets", "fig")


def view(yaw, pitch):
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    return Rx @ Ry


class Scene:
    def __init__(self, size=300, R=1.0, yaw=0.6, pitch=0.45, scale=None):
        self.size, self.R, self.M = size, R, view(yaw, pitch)
        self.s = scale or size * 0.43 / R
        self.items = []  # (depth, svg)

    def p2(self, x):
        y = self.M @ np.asarray(x, float)
        return self.size / 2 + self.s * y[0], self.size / 2 - self.s * y[1], y[2]

    def path(self, pts, closed=False):
        q = [self.p2(p) for p in pts]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y, _ in q) + (" Z" if closed else "")
        return d, sum(z for *_, z in q) / len(q)

    def point(self, p, cls="fig-pt", r=5.0):
        x, y, z = self.p2(p)
        self.items.append((z + 10, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" class="{cls}"/>'))

    def svg(self, title):
        body = "\n".join(s for _, s in sorted(self.items, key=lambda t: t[0]))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.size} {self.size}" width="{self.size}" '
                f'height="{self.size}" role="img"><title>{title}</title>\n{body}\n</svg>\n')


def sphere_a3():
    """The six planes x_i = +-x_j through the centre meet a sphere in six great circles: four lines on three planes
    (the body diagonals) give the four triple points, i.e. the complete quadrilateral."""
    sc = Scene(R=1.0, yaw=0.42, pitch=0.33, scale=125)
    size = sc.size
    sc.items.append((-100, f'<circle cx="{size / 2}" cy="{size / 2}" r="{sc.s:.1f}" class="fig-sphere"/>'))
    normals = [(1, -1, 0), (1, 1, 0), (1, 0, -1), (1, 0, 1), (0, 1, -1), (0, 1, 1)]
    for n in normals:
        n = np.array(n, float) / math.sqrt(2)
        u = np.cross(n, [0.3, 0.5, 0.8])
        u /= np.linalg.norm(u)
        v = np.cross(n, u)
        ts = np.linspace(0, 2 * math.pi, 241)
        pts = [math.cos(t) * u + math.sin(t) * v for t in ts]
        # split into front and back arcs
        seg, segs = [], []
        for p in pts:
            fr = (sc.M @ p)[2] >= 0
            if seg and seg[-1][1] != fr:
                segs.append(seg)
                seg = [seg[-1]]
            seg.append((p, fr))
        segs.append(seg)
        for s in segs:
            fr = s[-1][1]
            dd, _ = sc.path([p for p, _ in s])
            sc.items.append((5 if fr else -50, f'<path d="{dd}" class="{"fig-gc" if fr else "fig-gc back"}"/>'))
    for d in ([1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]):
        for sgn in (1, -1):
            p = sgn * np.array(d, float) / math.sqrt(3)
            fr = (sc.M @ p)[2] >= 0
            sc.point(p, "fig-pt" if fr else "fig-pt back", 5.5 if fr else 4)
    for d in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
        for sgn in (1, -1):
            p = sgn * np.array(d, float)
            fr = (sc.M @ p)[2] >= 0
            sc.point(p, "fig-pt3" if fr else "fig-pt3 back", 3.5 if fr else 2.5)
    return sc


def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "planes-sphere": (sphere_a3(), "Six planes through a point cut a small sphere in six great circles"),
    }
    for name, (sc, title) in figs.items():
        with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(sc.svg(title))
        print("wrote", name)


if __name__ == "__main__":
    main()
