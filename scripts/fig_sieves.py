"""Figure: the three sieves as nested sets, with the counts for a given n.

usage: python scripts/fig_sieves.py OUT.svg [n]  (counts read from data/results/sequences.json)
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
seq = json.load(open(os.path.join(ROOT, "data", "results", "sequences.json")))
a, b, c = seq["a"][n - 1], seq["b"][n - 1], seq["c"][n - 1]


def txt(v):
    return ("%d … %d" % tuple(v)) if isinstance(v, list) else str(v)


W, H = 680, 400
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Georgia, \'Source Serif 4\', serif">',
       '<title>The three sieves as nested sets</title>']
# (x, y, w, h, fill, stroke, title line, count line)
boxes = [(16, 16, 648, 368, "#f3f4f7", "#c8ccd3", "all multisets of pencil sizes", ""),
         (40, 56, 600, 304, "#e4e9f3", "#9fb0cf", "arithmetically admissible", f"a({n}) = {txt(a)}"),
         (76, 110, 528, 226, "#cfd9ec", "#6f86b5", "combinatorially possible (linear spaces)", f"b({n}) = {txt(b)}"),
         (130, 178, 420, 134, "#aebfe0", "#2b3a67", "realizable by real lines", f"c({n}) = {txt(c)}")]
for x, y, w, h, fill, stroke, title, count in boxes:
    inner = ' inner' if title.startswith('realizable') else ''
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="fig-box{inner}"/>')
    svg.append(f'<text x="{x + 16}" y="{y + 24}" font-size="15" class="fig-text">{title}</text>')
    if count:
        svg.append(f'<text x="{x + w - 16}" y="{y + 24}" font-size="15" text-anchor="end" font-weight="bold" class="fig-text">{count}</text>')
# the gap between the two inner boxes
svg.append('<text x="340" y="328" text-anchor="middle" font-size="12.5" class="fig-text">between the two inner boxes: orientable but not realizable, e.g. {6, 4, 3<tspan dy="-5" font-size="9">12</tspan><tspan dy="5">} for n = 12</tspan></text>')
svg.append('</svg>')
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(svg))
