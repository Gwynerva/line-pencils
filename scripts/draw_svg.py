"""Draw an arrangement from an exact certificate as an SVG picture.

A certificate stores the n lines by coefficient vectors (projectively).  To draw it we apply a
projective transformation chosen so that every intersection point is finite and the picture is
well spread: random 3x3 matrices followed by a short random hill-climb on a score that rewards
large distances between distinct points, clearance between points and the lines not through them,
and angular separation of the lines.  The transformation is applied to the exact coefficients
converted to floats; incidences are preserved exactly by projective maps, so the picture shows the
true pencils (the exact data remain the certificate).

Colours by multiplicity (used everywhere on the site):
    2: grey    3: blue    4: orange    5: red    6: purple    7+: black

usage: python scripts/draw_svg.py N TYPE OUT.svg           (one certificate)
       python scripts/draw_svg.py --all OUTDIR [NMAX]        (every certificate -> OUTDIR/n{n}/{type}.svg)
"""
import itertools, json, math, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from pencils import key, unkey, fmt

# Points are coloured on an ordered scale: the more lines through a point, the warmer and larger the dot.
#   2 = small neutral grey, then 3 blue, 4 violet, 5 magenta, 6 red, 7 orange, 8 amber, 9+ dark brown.
COLOURS = {2: "#a6abb3", 3: "#2f6fd6", 4: "#6a4fc4", 5: "#b03aa0", 6: "#d9382e", 7: "#ee7a1d", 8: "#f0b400", 9: "#5a3a1a"}
LINE_COLOUR = "#3b3f44"


def colour(k):
    return COLOURS.get(min(k, 9), "#5a3a1a")


def lines_float(cert):
    d = cert["d"]; s = math.sqrt(d) if d else 0.0
    L = np.array([[c[0] + c[1] * s for c in line] for line in cert["lines"]], float)
    return L / np.linalg.norm(L, axis=1)[:, None]


def pencils(L, tol=1e-9):
    """[(set of line indices, point as projective 3-vector)] computed numerically (the exact
    structure is certified separately; tol only groups numerically identical points)."""
    n = len(L); out = []
    for i, j in itertools.combinations(range(n), 2):
        if any(i in g[0] and j in g[0] for g in out):
            continue
        X = np.cross(L[i], L[j]); X /= np.linalg.norm(X)
        S = {k for k in range(n) if abs(L[k] @ X) < tol}
        out.append((S, X))
    return out


def evaluate(L, X0, M, member):
    """Apply projective map M (acting on points as X -> M X, on lines as L -> L M^{-1}); return score and
    affine picture normalised to the unit disc."""
    try:
        Minv = np.linalg.inv(M)
    except np.linalg.LinAlgError:
        return -1, None
    X = X0 @ M.T
    if np.min(np.abs(X[:, 2]) / np.linalg.norm(X, axis=1)) < 1e-3:
        return -1, None
    A = X[:, :2] / X[:, 2:3]
    Ln = L @ Minv
    c = A.mean(0)
    A0 = A - c
    R = np.max(np.linalg.norm(A0, axis=1)) if len(A0) > 1 else 1.0
    if R == 0:
        return -1, None
    B = A0 / R
    # transform lines consistently: new point v = (u - c)/R  ->  u = R v + c ; a u + b u' + e = 0
    Lb = np.empty_like(Ln)
    Lb[:, :2] = Ln[:, :2] * R
    Lb[:, 2] = Ln[:, :2] @ c + Ln[:, 2]
    Lb /= np.linalg.norm(Lb[:, :2], axis=1)[:, None]
    if len(B) > 1:
        D = np.linalg.norm(B[:, None] - B[None], axis=2) + 9 * np.eye(len(B))
        dmin = D.min()
    else:
        dmin = 1.0
    dist = np.abs(B @ Lb[:, :2].T + Lb[:, 2][None, :])
    dd = np.where(member, 9, dist)
    clear = dd.min() if dd.size else 1.0
    ang = np.arctan2(Lb[:, 1], Lb[:, 0]) % math.pi
    s = np.sort(ang); gaps = np.diff(np.concatenate([s, [s[0] + math.pi]]))
    agap = gaps.min() if len(s) > 1 else 1.0
    # also keep the picture round-ish: penalise points crowding the centre
    spread = np.mean(np.linalg.norm(B, axis=1)) if len(B) > 1 else 1.0
    score = min(dmin, 1.5 * clear) * min(1.0, agap / 0.10) * (0.5 + spread)
    return score, (Lb, B)


def layout(cert, tries=600, climb=600, seed=0, lines=None):
    """lines: optional float lines (n x 3) to lay out instead of the certificate's own (e.g. a numerical
    re-realization of the same incidence structure when the certificate is numerically ill-conditioned)"""
    L = lines_float(cert) if lines is None else np.asarray(lines, float) / np.linalg.norm(np.asarray(lines, float), axis=1)[:, None]
    n = len(L)
    rng = np.random.default_rng(seed)
    if n == 1:
        return {"lines": [[0.0, 1.0, 0.0]], "points": [], "score": 1.0}
    G = pencils(L)
    X0 = np.array([g[1] for g in G])
    member = np.array([[k in g[0] for k in range(n)] for g in G])
    if len(G) == 1:   # a pencil: draw as a regular star
        Ls = [[-math.sin(math.pi * k / n), math.cos(math.pi * k / n), 0.0] for k in range(n)]
        return {"lines": Ls, "points": [[0.0, 0.0, sorted(G[0][0])]], "score": 1.0}
    best = (-2, None, None)
    for t in range(tries):
        M = rng.normal(size=(3, 3))
        sc, res = evaluate(L, X0, M, member)
        if sc > best[0]:
            best = (sc, M, res)
    step = 0.3
    for t in range(climb):
        M = best[1] + rng.normal(scale=step, size=(3, 3))
        sc, res = evaluate(L, X0, M, member)
        if sc > best[0]:
            best = (sc, M, res)
        if t % 150 == 149:
            step *= 0.6
    Lb, B = best[2]
    return {"lines": [[float(a), float(b), float(c)] for a, b, c in Lb],
            "points": [[float(B[i, 0]), float(B[i, 1]), sorted(G[i][0])] for i in range(len(G))],
            "score": float(best[0])}


def clip_line(a, b, c, R):
    """segment of the line a x + b y + c = 0 inside the disc of radius R (centre 0), or None"""
    nrm = math.hypot(a, b); a, b, c = a / nrm, b / nrm, c / nrm
    d = -c
    if abs(d) >= R:
        return None
    h = math.sqrt(R * R - d * d)
    px, py = a * d, b * d
    tx, ty = -b, a
    return (px - h * tx, py - h * ty, px + h * tx, py + h * ty)


def svg(cert, size=360, margin=1.18, show_doubles=True, lay=None, caption=None, stroke=1.4, dot=None):
    lay = lay or layout(cert)
    n = cert["n"]
    R = margin
    half = size / 2
    sc = half / R
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img">']
    if caption:
        out.append(f"<title>{caption}</title>")
    out.append(f'<circle cx="{half}" cy="{half}" r="{half-0.5}" fill="#ffffff" stroke="#e3e5e8" stroke-width="1"/>')
    out.append(f'<clipPath id="c"><circle cx="{half}" cy="{half}" r="{half-1}"/></clipPath>')
    out.append('<g clip-path="url(#c)">')
    for a, b, c in lay["lines"]:
        seg = clip_line(a, b, c, R * 1.05)
        if seg is None:
            continue
        x1, y1, x2, y2 = seg
        out.append(f'<line x1="{half + sc*x1:.1f}" y1="{half - sc*y1:.1f}" x2="{half + sc*x2:.1f}" y2="{half - sc*y2:.1f}" '
                   f'stroke="{LINE_COLOUR}" stroke-width="{stroke}" stroke-linecap="round"/>')
    dot = dot or max(2.2, size / 90)
    for x, y, S in sorted(lay["points"], key=lambda p: len(p[2])):
        k = len(S)
        if k == 2 and not show_doubles:
            continue
        r = dot * (0.75 if k == 2 else 1.0 + 0.18 * (k - 3))
        out.append(f'<circle cx="{half + sc*x:.1f}" cy="{half - sc*y:.1f}" r="{r:.1f}" fill="{colour(k)}" stroke="#ffffff" stroke-width="1"/>')
    out.append("</g></svg>")
    return "\n".join(out)


def all_certificates(outdir, nmax=13, size=360):
    index = {}
    for n in range(1, nmax + 1):
        fn = os.path.join(ROOT, "data", "certificates", "n%d.json" % n)
        certs = json.load(open(fn)) if os.path.exists(fn) else []
        if n == 1:
            certs = [{"n": 1, "type": [], "d": 0, "lines": [[[0, 0], [1, 0], [0, 0]]]}]
        if n == 2:
            certs = [{"n": 2, "type": [], "d": 0, "lines": [[[1, 0], [0, 0], [0, 0]], [[0, 0], [1, 0], [0, 0]]]}]
        os.makedirs(os.path.join(outdir, "n%d" % n), exist_ok=True)
        index[n] = []
        for c in certs:
            t = tuple(sorted(c["type"], reverse=True))
            name = ("-".join(map(str, t)) or "general") + ".svg"
            path = os.path.join(outdir, "n%d" % n, name)
            lay = layout(c)
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg(c, size=size, lay=lay, caption="n = %d, type %s" % (n, fmt(t))))
            index[n].append({"type": list(t), "file": "n%d/%s" % (n, name), "d": c["d"], "source": c.get("source", ""), "score": round(lay["score"], 4)})
        print("n=%d: %d drawings" % (n, len(certs)), flush=True)
    with open(os.path.join(outdir, "index.json"), "w") as f:
        json.dump(index, f)


if __name__ == "__main__":
    if sys.argv[1] == "--all":
        all_certificates(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 13)
    else:
        n = int(sys.argv[1]); t = list(unkey(sys.argv[2]))
        certs = json.load(open(os.path.join(ROOT, "data", "certificates", "n%d.json" % n)))
        c = next(c for c in certs if sorted(c["type"], reverse=True) == sorted(t, reverse=True))
        open(sys.argv[3], "w", encoding="utf-8").write(svg(c, caption="n = %d, type %s" % (n, fmt(t))))
