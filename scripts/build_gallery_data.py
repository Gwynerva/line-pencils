"""Data for the interactive drawings on the site: docs/assets/data/gallery.json.

For every certificate (data/certificates/n{n}.json) a projective transformation is chosen once for legibility
(scripts/draw_svg.py: layout), and the transformed lines are stored as floats; the browser computes the intersection
points and their pencils itself (docs/javascripts/arrangements.js).  The exact certificate coefficients are stored as
well, for display.  The regular pentagram with its axes is stored under "star" with exact 5-fold symmetry.

Every stored drawing is checked here: the pencils recomputed from the float lines with the same tolerance as the
browser must give exactly the certified type.  Where data/symmetric_drawings.json (scripts/symmetric_drawings.py)
has a symmetric drawing of the type, it is checked in the same way and stored as "S" (with its symmetry order and a
sentence on how it was obtained); the gallery shows it under "Beautiful" and the certified drawing under "Exact".

usage: python scripts/build_gallery_data.py [NMAX]
"""
import itertools, json, math, os, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from draw_svg import layout
from pencils import f0

TOL = 1e-4          # same tolerance as arrangements.js; coordinates are stored with 7 decimals
SEP = 2e-3          # distinct points must be at least this far apart (else another layout is tried)


def pencils_float(L, sep=SEP):
    """multiplicities >= 3 of the intersection points of lines L = [[a, b, c], ...] (affine picture, z = 1)"""
    pts = []
    for i, j in itertools.combinations(range(len(L)), 2):
        a1, b1, c1 = L[i]; a2, b2, c2 = L[j]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-12:
            return None
        x = (-c1 * b2 + c2 * b1) / det; y = (-a1 * c2 + a2 * c1) / det
        for p in pts:
            if abs(p[0] - x) < TOL and abs(p[1] - y) < TOL:
                p[2].update((i, j)); break
        else:
            pts.append([x, y, {i, j}])
    for p, q in itertools.combinations(pts, 2):
        if math.hypot(p[0] - q[0], p[1] - q[1]) < sep:
            return None
    return sorted((len(p[2]) for p in pts if len(p[2]) >= 3), reverse=True)


def relayout(cert, t):
    """For numerically ill-conditioned certificates (huge integers, nearly coincident points): realize the same
    incidence structure numerically with well-separated points (scripts/realize.py) and lay that out instead.
    The drawing then shows the certified combinatorics; the exact numbers stay those of the certificate."""
    sys.path.insert(0, os.path.join(ROOT, "verifier"))
    from verify import pencils_of
    from realize import numeric_realization
    n = cert["n"]
    Lx = [tuple((c[0], c[1]) for c in line) for line in cert["lines"]]
    blocks = [sorted(S) for S in pencils_of(Lx, cert["d"]) if len(S) >= 3]
    for seed in range(5):
        num = numeric_realization(n, blocks, seed=seed, starts=200, min_gap=1e-2)
        if num is None:
            continue
        for s2 in range(6):
            lay = layout(cert, seed=s2, lines=num[0])
            L = [[round(a, 7), round(b, 7), round(cc, 7)] for a, b, cc in lay["lines"]]
            if pencils_float(L, SEP / 4) == t:
                return L
    return None


def star_lines():
    tips = [(math.cos(math.pi / 2 + 2 * math.pi * i / 5), math.sin(math.pi / 2 + 2 * math.pi * i / 5)) for i in range(5)]

    def through(p, q):
        a, b = q[1] - p[1], p[0] - q[0]; c = -(a * p[0] + b * p[1]); nn = math.hypot(a, b)
        return [a / nn, b / nn, c / nn]
    L = [through(tips[i], tips[(i + 2) % 5]) for i in range(5)] + [through((0, 0), tips[i]) for i in range(5)]
    return [[round(a, 6), round(b, 6), round(c, 6)] for a, b, c in L]


SYM_FILE = os.path.join(ROOT, "data", "symmetric_drawings.json")
SYM = json.load(open(SYM_FILE)) if os.path.exists(SYM_FILE) else {}


def main(nmax):
    out = {"star": {"n": 10, "type": [5] + [3] * 10, "L": star_lines()}, "n": {}}
    assert pencils_float(out["star"]["L"]) == [5] + [3] * 10
    for n in range(1, nmax + 1):
        if n == 1:
            certs = [{"n": 1, "type": [], "d": 0, "lines": [[[0, 0], [1, 0], [0, 0]]], "source": "a single line"}]
        elif n == 2:
            certs = [{"n": 2, "type": [], "d": 0, "lines": [[[1, 0], [0, 0], [0, 0]], [[0, 0], [1, 0], [0, 0]]], "source": "two lines"}]
        else:
            fn = os.path.join(ROOT, "data", "certificates", "n%d.json" % n)
            if not os.path.exists(fn):
                continue
            certs = json.load(open(fn))
        items = []
        for c in certs:
            t = sorted(c["type"], reverse=True)
            best = None
            for seed, sep in [(s_, SEP) for s_ in range(8)] + [(s_, SEP / 4) for s_ in range(8, 24)]:
                lay = layout(c, seed=seed)
                L = [[round(a, 7), round(b, 7), round(cc, 7)] for a, b, cc in lay["lines"]]
                if n <= 2 or pencils_float(L, sep) == t:
                    best = L; break
            if best is None:
                best = relayout(c, t)
            if best is None:
                raise SystemExit("n=%d type %s: no layout reproduces the type" % (n, t))
            items.append({"type": t, "f0": f0(n, tuple(t)), "d": c["d"], "source": c.get("source", ""),
                          "L": best, "exact": c["lines"]})
        sym = SYM.get(str(n), {})
        for it in items:
            s_ = sym.get(",".join(map(str, it["type"])))
            if s_ and pencils_float(s_["L"], SEP / 4) == it["type"]:
                it.update({"S": s_["L"], "sym": s_["symmetry"], "rot": s_["rotation"], "how": s_["how"]})
        items.sort(key=lambda it: (-max(it["type"] or [2]), -len(it["type"]), it["type"]), reverse=False)
        out["n"][str(n)] = items
        print("n=%d: %d drawings, %d with a symmetric view" % (n, len(items), sum(1 for it in items if "S" in it)), flush=True)
    os.makedirs(os.path.join(ROOT, "docs", "assets", "data"), exist_ok=True)
    with open(os.path.join(ROOT, "docs", "assets", "data", "gallery.json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print("size: %.0f KB" % (os.path.getsize(os.path.join(ROOT, "docs", "assets", "data", "gallery.json")) / 1024))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 14)
