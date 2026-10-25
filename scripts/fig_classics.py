"""Figures of the three classical linear spaces that exist combinatorially but not as real lines:
Fano plane (7_3), Moebius-Kantor (8_3), Hesse / AG(2,3) (9_4 12_3).  Straight lines where possible,
one or more curved "lines" (drawn dashed) where the real plane refuses.

usage: python scripts/fig_classics.py OUTDIR
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
# Theme-aware: colours come from CSS classes (fig-line, fig-curve, fig-pt in docs/stylesheets/extra.css);
# the files are inlined into the pages, so they follow the light/dark scheme.

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
S = 320


def head(title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" role="img"><title>{title}</title>']


def seg(p, q, dashed=False):
    cls = "fig-curve" if dashed else "fig-line"
    return f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" class="{cls}"/>'


def ext(p, q, f=0.35):
    """segment through p, q extended by a fraction f on both ends"""
    return ((p[0] - f * (q[0] - p[0]), p[1] - f * (q[1] - p[1])), (q[0] + f * (q[0] - p[0]), q[1] + f * (q[1] - p[1])))


def dot(p, k=3):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="5.5" class="fig-pt"/>'


# ---- Fano: equilateral triangle, medians, incircle
svg = head("The Fano plane: seven points, seven lines of three; one of them must be a circle")
c = (S / 2, S / 2 + 18); R = 118
A = [(c[0] + R * math.cos(math.radians(90 + 120 * i)), c[1] - R * math.sin(math.radians(90 + 120 * i))) for i in range(3)]
M = [((A[(i + 1) % 3][0] + A[(i + 2) % 3][0]) / 2, (A[(i + 1) % 3][1] + A[(i + 2) % 3][1]) / 2) for i in range(3)]
G = (c[0], c[1])
r_in = R / 2
for i in range(3):
    svg.append(seg(*ext(A[i], A[(i + 1) % 3], 0.12)))
    svg.append(seg(*ext(A[i], M[i], 0.12)))
svg.append(f'<circle cx="{G[0]:.1f}" cy="{G[1]:.1f}" r="{r_in:.1f}" class="fig-curve"/>')
for p in A + M + [G]:
    svg.append(dot(p))
svg.append("</svg>")
open(os.path.join(out, "fano.svg"), "w", encoding="utf-8").write("\n".join(svg))

# ---- Moebius-Kantor 8_3: points Z/8, lines {i, i+1, i+3}; drawn abstractly on two concentric squares
cx, cy = S / 2, S / 2
Z = {}
for i in range(4):
    Z[2 * i] = (cx + 120 * math.cos(math.radians(45 + 90 * i)), cy - 120 * math.sin(math.radians(45 + 90 * i)))
    Z[2 * i + 1] = (cx + 55 * math.cos(math.radians(90 * i + 90)), cy - 55 * math.sin(math.radians(90 * i + 90)))
svg = head("The Moebius-Kantor configuration (8_3) on Z/8: lines {i, i+1, i+3}; drawn abstractly, curved where straightness fails")
for i in range(8):
    a, b, d = i % 8, (i + 1) % 8, (i + 3) % 8
    p, q, r = Z[a], Z[b], Z[d]
    # draw as a quadratic curve through the three points (control point chosen so the curve passes through q)
    ctrl = (2 * q[0] - (p[0] + r[0]) / 2, 2 * q[1] - (p[1] + r[1]) / 2)
    svg.append(f'<path d="M {p[0]:.1f} {p[1]:.1f} Q {ctrl[0]:.1f} {ctrl[1]:.1f} {r[0]:.1f} {r[1]:.1f}" class="fig-curve"/>')
for p in Z.values():
    svg.append(dot(p))
svg.append("</svg>")
open(os.path.join(out, "moebius-kantor.svg"), "w", encoding="utf-8").write("\n".join(svg))

# ---- Hesse / AG(2,3): 3x3 grid; rows, columns, 2 diagonals straight (8 lines), the 4 "wrapped" diagonals curved
svg = head("The Hesse configuration AG(2,3): nine points, twelve lines of three; the four wrapped diagonals cannot be straight")
g = {}
for i in range(3):
    for j in range(3):
        g[(i, j)] = (70 + 90 * j, 70 + 90 * i)
for i in range(3):
    svg.append(seg(*ext(g[(i, 0)], g[(i, 2)], 0.15)))
    svg.append(seg(*ext(g[(0, i)], g[(2, i)], 0.15)))
svg.append(seg(*ext(g[(0, 0)], g[(2, 2)], 0.12)))
svg.append(seg(*ext(g[(0, 2)], g[(2, 0)], 0.12)))
wrapped = [[(0, 1), (1, 2), (2, 0)], [(0, 2), (1, 0), (2, 1)], [(0, 1), (1, 0), (2, 2)], [(0, 0), (1, 2), (2, 1)]]
for w in wrapped:
    p, q, r = [g[t] for t in w]
    ctrl = (2 * q[0] - (p[0] + r[0]) / 2, 2 * q[1] - (p[1] + r[1]) / 2)
    svg.append(f'<path d="M {p[0]:.1f} {p[1]:.1f} Q {ctrl[0]:.1f} {ctrl[1]:.1f} {r[0]:.1f} {r[1]:.1f}" class="fig-curve"/>')
for p in g.values():
    svg.append(dot(p, 4))
svg.append("</svg>")
open(os.path.join(out, "hesse.svg"), "w", encoding="utf-8").write("\n".join(svg))
print("written")
