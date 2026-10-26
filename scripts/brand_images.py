"""Raster images for browsers and for GitHub: PNG favicons and the repository banner.

  docs/assets/favicon-{16,32,48,192,512}.png, docs/assets/favicon.ico, docs/assets/apple-touch-icon.png
      the logo (docs/assets/logo.svg: a pencil of four lines and a transversal) on a dark blue rounded tile with light
      lines, so that it reads on light and on dark tab bars; browsers that understand SVG favicons keep logo.svg.
  docs/assets/banner-light.png, docs/assets/banner-dark.png   (1280 x 400, for README.md via <picture>)
  docs/assets/social.png                                       (1280 x 640, social preview / og:image)
      logo, title, subtitle and a symmetric arrangement from data/symmetric_drawings.json.

Drawn with Pillow at 4x and downsampled; the geometry of the logo is read from logo.svg.

usage: python scripts/brand_images.py
"""
import itertools, json, math, os, re
from PIL import Image, ImageChops, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "docs", "assets")
FONTS = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")
SS = 4                                                   # supersampling factor


def logo_geometry():
    s = open(os.path.join(ASSETS, "logo.svg"), encoding="utf-8").read()
    lines = [tuple(map(float, m)) for m in re.findall(r'<line x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', s)]
    mask = s[s.index("<mask"):s.index("</mask>")]
    holes = [tuple(map(float, m)) for m in re.findall(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([-\d.]+)" fill="black"', mask)]
    rest = s[s.index("</g>"):]
    dots = [(float(x), float(y), float(r), c) for x, y, r, c in re.findall(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([-\d.]+)" class="(\w+)"', rest)]
    return lines, holes, dots


def draw_logo(size, line_col, dot_col, dot2_col, scale=1.0):
    """the logo on a transparent square of `size` pixels (viewBox -1..1 scaled by `scale`)"""
    W = size * SS
    f = lambda v: (v * scale + 1) / 2 * W
    lines, holes, dots = logo_geometry()
    lay = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    w = max(1, round(0.14 * scale / 2 * W))
    for x1, y1, x2, y2 in lines:
        d.line([f(x1), f(y1), f(x2), f(y2)], fill=line_col, width=w)
        for x, y in ((x1, y1), (x2, y2)):                 # round caps
            d.ellipse([f(x) - w / 2, f(y) - w / 2, f(x) + w / 2, f(y) + w / 2], fill=line_col)
    m = Image.new("L", (W, W), 255)
    dm = ImageDraw.Draw(m)
    for x, y, r in holes:
        dm.ellipse([f(x - r), f(y - r), f(x + r), f(y + r)], fill=0)
    lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", (W, W), 0), m))
    d = ImageDraw.Draw(lay)
    for x, y, r, c in dots:
        d.ellipse([f(x - r), f(y - r), f(x + r), f(y + r)], fill=dot_col if c == "dot" else dot2_col)
    return lay


def tile_icon(size):
    """favicon: the logo, light on a dark blue rounded tile"""
    W = size * SS
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, W - 1, W - 1], radius=round(W * 0.22), fill=(22, 43, 92, 255))
    logo = draw_logo(size, (126, 168, 255, 255), (255, 255, 255, 255), (178, 204, 255, 255), scale=0.82)
    img.alpha_composite(logo)
    return img.resize((size, size), Image.LANCZOS)


def arrangement_layer(L, W, H, cx, cy, R, col, pt_cols, lw, pr):
    """draw lines L (unit-disc normalised) centred at (cx, cy) with radius R; the lines run across the whole image"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    Rc = math.hypot(W, H) / R
    for a, b, c in L:
        n = math.hypot(a, b); a, b, c = a / n, b / n, c / n
        if abs(c) >= Rc:
            continue
        h = math.sqrt(Rc * Rc - c * c); px, py = -a * c, -b * c
        p1 = (px + h * b, py - h * a); p2 = (px - h * b, py + h * a)
        d.line([cx + p1[0] * R, cy - p1[1] * R, cx + p2[0] * R, cy - p2[1] * R], fill=col, width=lw)
    pts = {}
    for i, j in itertools.combinations(range(len(L)), 2):
        (a1, b1, c1), (a2, b2, c2) = L[i], L[j]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-12:
            continue
        x = (-c1 * b2 + c2 * b1) / det; y = (-a1 * c2 + a2 * c1) / det
        key = (round(x, 5), round(y, 5))
        pts.setdefault(key, set()).update((i, j))
    for (x, y), s in sorted(pts.items(), key=lambda kv: len(kv[1])):
        k = len(s)
        if k < 3:
            continue
        r = pr * (1 + 0.35 * (k - 3))
        d.ellipse([cx + x * R - r, cy - y * R - r, cx + x * R + r, cy - y * R + r], fill=pt_cols[min(k, len(pt_cols) + 2) - 3])
    return lay


def banner(W, H, dark, L, path):
    bg = (16, 22, 34) if dark else (247, 249, 252)
    ink = (232, 238, 247) if dark else (22, 30, 44)
    muted = (150, 164, 185) if dark else (88, 100, 120)
    line_col = (196, 210, 232, 150) if dark else (60, 74, 98, 140)
    pts = [(122, 167, 255), (255, 170, 90), (238, 110, 180), (90, 210, 160)] if dark else [(47, 111, 214), (224, 123, 31), (194, 51, 142), (26, 158, 106)]
    w, h = W * SS, H * SS
    u = min(h, w / 3.2)                              # layout unit: the height of a 1280 x 400 banner
    top = (h - u) / 2
    img = Image.new("RGBA", (w, h), bg + (255,))
    x0 = int(u * 0.16)
    title = ImageFont.truetype(os.path.join(FONTS, "georgiab.ttf"), int(u * 0.15))
    sub = ImageFont.truetype(os.path.join(FONTS, "georgia.ttf"), int(u * 0.058))
    small = ImageFont.truetype(os.path.join(FONTS, "segoeui.ttf"), int(u * 0.045))
    SUB = "Pencil types of line arrangements and the integer sequences they generate"
    te = x0 + max(title.getlength("How n Lines Can Meet"), sub.getlength(SUB))   # right edge of the text
    # the arrangement fills the height and the right part; behind the text it is almost transparent
    cx = max(w - h * 0.62, te + h * 0.30)
    art = arrangement_layer(L, w, h, int(cx), h // 2, h * 0.44, line_col, pts, max(2, SS), 4.2 * SS)
    ramp = Image.new("L", (w, h), 255)
    rise = int(h * 0.30)                              # width of the transition after the text
    ramp.paste(28, (0, 0, int(te), h))
    ramp.paste(Image.linear_gradient("L").rotate(90, expand=True).resize((rise, h))
               .point(lambda v: int(28 + 227 * (v / 255) ** 1.5)), (int(te), 0))
    art.putalpha(ImageChops.multiply(art.getchannel("A"), ramp))
    img.alpha_composite(art)
    ls = int(u * 0.30)
    logo = draw_logo(max(1, ls // SS), (122, 167, 255, 255) if dark else (50, 116, 220, 255),
                     (238, 244, 255, 255) if dark else (22, 63, 158, 255), (163, 193, 255, 255) if dark else (50, 116, 220, 255))
    logo = logo.resize((ls, ls), Image.LANCZOS)
    img.alpha_composite(logo, (x0, int(top + u * 0.14)))
    d = ImageDraw.Draw(img)
    d.text((x0, int(top + u * 0.50)), "How n Lines Can Meet", font=title, fill=ink)
    d.text((x0, int(top + u * 0.69)), SUB, font=sub, fill=muted)
    d.text((x0, int(top + u * 0.81)), "gwynerva.github.io/line-pencils", font=small, fill=(122, 167, 255) if dark else (47, 111, 214))
    img.convert("RGB").resize((W, H), Image.LANCZOS).save(path, optimize=True)


def main():
    for s in (16, 32, 48, 192, 512):
        tile_icon(s).save(os.path.join(ASSETS, "favicon-%d.png" % s), optimize=True)
    tile_icon(180).save(os.path.join(ASSETS, "apple-touch-icon.png"), optimize=True)
    tile_icon(256).save(os.path.join(ASSETS, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    sym = json.load(open(os.path.join(ROOT, "data", "symmetric_drawings.json")))
    # the most symmetric drawing with many triple points: prefer 12 lines, rotation order 3
    cand = [(v["symmetry"], len(k.split(",")), n, k, v) for n, d in sym.items() for k, v in d.items() if v["rotation"] >= 3 and int(n) <= 13]
    best = max(cand, key=lambda z: (z[2] == "12", z[1], z[0]))
    L = best[4]["L"]
    print("banner arrangement: n = %s, type {%s}, symmetry %d" % (best[2], best[3], best[0]))
    banner(1280, 400, False, L, os.path.join(ASSETS, "banner-light.png"))
    banner(1280, 400, True, L, os.path.join(ASSETS, "banner-dark.png"))
    banner(1280, 640, True, L, os.path.join(ASSETS, "social.png"))
    print("written:", ", ".join(sorted(f for f in os.listdir(ASSETS) if f.endswith((".png", ".ico")))))


if __name__ == "__main__":
    main()
