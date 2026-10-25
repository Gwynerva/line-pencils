"""Logo / favicon: a pencil of full lines through one point, crossed by a transversal ("fan" design).

Lines are full chords of the icon's disc, so they stick out on both sides of the pencil point. Every dot has a
transparent ring cut out of the lines around it (a larger one for the pencil point, a small one for the crossings).
Colours are the site's blues, with a light and a dark set switched by prefers-color-scheme.

usage: python scripts/logo_fan.py OUTDIR                 writes the variants and OUTDIR/preview.html
       python scripts/logo_fan.py --final NAME OUT.svg
"""
import math, os, sys

LIGHT = {"line": "#3274dc", "dot": "#163f9e", "dot2": "#3274dc"}   # --lp-s3 / --lp-s4 of the site (light)
DARK = {"line": "#7ea8ff", "dot": "#eef4ff", "dot2": "#a3c1ff"}    # the site's dark-scheme blues


def meet(a, b, c, d):
    den = (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
    u = a[0] * b[1] - a[1] * b[0]; v = c[0] * d[1] - c[1] * d[0]
    return ((u * (c[0] - d[0]) - (a[0] - b[0]) * v) / den, (u * (c[1] - d[1]) - (a[1] - b[1]) * v) / den)


def chord(p, q, R):
    dx, dy = q[0] - p[0], q[1] - p[1]; n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
    t0 = -(p[0] * dx + p[1] * dy); cx, cy = p[0] + t0 * dx, p[1] + t0 * dy
    h = math.sqrt(max(R * R - cx * cx - cy * cy, 0))
    return (cx - h * dx, cy - h * dy, cx + h * dx, cy + h * dy)


def icon(angles=(15, 60, 105, 150), centre=(-0.1, 0.3), trans=((-1, -0.55), (1, -0.3)), R=0.98, Rt=0.98,
         w=0.11, r_centre=0.18, r_dot=0.1, gap_centre=0.07, gap_dot=0.04, title="a pencil of lines and a transversal"):
    c = centre; segs = []; dots = [(c, r_centre, "dot", gap_centre)]
    for a in angles:
        q = (c[0] + math.cos(math.radians(a)), c[1] + math.sin(math.radians(a)))
        segs.append(chord(c, q, R))
        dots.append((meet(c, q, trans[0], trans[1]), r_dot, "dot2", gap_dot))
    segs.append(chord(trans[0], trans[1], Rt))
    holes = "".join(f'<circle cx="{p[0]:.3f}" cy="{-p[1]:.3f}" r="{r + g:.3f}" fill="black"/>' for p, r, _, g in dots)
    lines = "".join(f'<line x1="{a:.3f}" y1="{-b:.3f}" x2="{cc:.3f}" y2="{-dd:.3f}" class="l"/>' for a, b, cc, dd in segs)
    dts = "".join(f'<circle cx="{p[0]:.3f}" cy="{-p[1]:.3f}" r="{r}" class="{k}"/>' for p, r, k, _ in dots)
    style = (f".l{{stroke:{LIGHT['line']};stroke-width:{w};stroke-linecap:round}}.dot{{fill:{LIGHT['dot']}}}.dot2{{fill:{LIGHT['dot2']}}}"
             f"@media (prefers-color-scheme: dark){{.l{{stroke:{DARK['line']}}}.dot{{fill:{DARK['dot']}}}.dot2{{fill:{DARK['dot2']}}}}}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 2 2" width="64" height="64"><title>{title}</title>'
            f'<style>{style}</style><mask id="m"><rect x="-1" y="-1" width="2" height="2" fill="white"/>{holes}</mask>'
            f'<g mask="url(#m)">{lines}</g>{dts}</svg>')


V = {
    # the liked design, in the site's colours, small rings around the small dots
    "F1-original": dict(),
    # thicker lines and dots: reads better at 16 px
    "F2-bold": dict(w=0.14, r_centre=0.21, r_dot=0.12, gap_centre=0.08, gap_dot=0.05),
    # the chosen logo: F2-bold with the upper right line steeper (no longer reads as parallel to the transversal)
    # and the rightmost crossing moved inside the icon
    "logo": dict(angles=(30, 62, 105, 140), w=0.14, r_centre=0.21, r_dot=0.12, gap_centre=0.08, gap_dot=0.05),
    # three lines in the pencil instead of four
    "F3-three": dict(angles=(25, 80, 140), w=0.13, r_centre=0.2, r_dot=0.12),
    # pencil point moved further up and right, so the crossings sit nearer the centre
    "F4-corner": dict(centre=(0.15, 0.38), angles=(20, 65, 110, 155), trans=((-1, -0.5), (1, -0.22)), w=0.12, r_centre=0.2, r_dot=0.11),
    # horizontal transversal
    "F5-level": dict(trans=((-1, -0.45), (1, -0.45)), w=0.12, r_centre=0.2, r_dot=0.11),
    # five lines, finer
    "F6-five": dict(angles=(10, 45, 80, 115, 150), w=0.1, r_centre=0.19, r_dot=0.09, gap_dot=0.035),
    # lines clipped a little shorter: tips stay inside a smaller disc
    "F7-compact": dict(R=0.9, Rt=0.92, w=0.13, r_centre=0.2, r_dot=0.12),
}

if __name__ == "__main__":
    if sys.argv[1] == "--final":
        open(sys.argv[3], "w", encoding="utf-8").write(icon(**V[sys.argv[2]]))
        print("written", sys.argv[3]); sys.exit(0)
    OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".svg"):
            os.remove(os.path.join(OUT, f))
    for name, kw in V.items():
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(icon(**kw))
    import time
    ver = int(time.time())
    rows = []
    for scheme, bg, fg in (("light", "#ffffff", "#222"), ("light", "#eef0f3", "#222"), ("dark", "#202124", "#eee"), ("dark", "#35363a", "#eee")):
        cells = "".join(f'<td style="padding:12px 16px;text-align:center"><img src="{n}.svg?v={ver}" width="16"> <img src="{n}.svg?v={ver}" width="32"> '
                        f'<img src="{n}.svg?v={ver}" width="64"><br><span style="font:12px sans-serif;color:{fg}">{n}</span></td>' for n in V)
        rows.append(f'<tr style="background:{bg};color-scheme:{scheme}">{cells}</tr>')
    open(os.path.join(OUT, "preview.html"), "w", encoding="utf-8").write(
        "<!doctype html><html><body style='margin:0'><p style='font:13px sans-serif;margin:8px'>Colours follow the browser's light/dark "
        "setting (the dark rows show the dark colours only when the system is in dark mode).</p>"
        "<table style='border-collapse:collapse'>" + "".join(rows) + "</table></body></html>")
    print("written", list(V))
