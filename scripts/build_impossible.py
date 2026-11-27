"""Generate docs/impossible.md ("What cannot be drawn") from data/results/classification_n{n}.json.

For each n: how many admissible types fail each test, a table of the types that are combinatorially possible but
not realizable for a reason other than an inequality (orientability, theorems, algebraic certificates, literature),
the undecided types, and the inequality failures in a collapsible list.

usage: python scripts/build_impossible.py [NMAX]
"""
import json, os, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from pencils import t2

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def utype(t):
    c = Counter(t)
    parts = [f"{k}<sup>{c[k]}</sup>" if c[k] > 1 else str(k) for k in sorted(c, reverse=True)]
    return "{" + ", ".join(parts) + "}" if parts else "{ }"


REASON = {
    "non-orientable": "no linear space of this type admits an orientation (exhaustive search)",
    "non-realizable-proved": "orientable, but every orientable linear space of this type forces an extra collinearity (checked cofactor certificate; [Theorems C4, C5](theorems.md#lines-vs-pseudolines))",
    "theorem": "its nine quadruple points would form a real Hesse configuration, which Sylvester–Gallai forbids ([Proposition C3](theorems.md#c3))",
    "literature": "orchard problem: twelve lines have at most 19 triple points (Burr, Grünbaum, Sloane 1974)",
}
ORCH = "none of its linear spaces (five up to isomorphism: Steiner triple systems of order 13 minus a point) admits an orientation ([Proposition C3a](theorems.md#c3a))"
SPLIT = "none of its linear spaces admits an orientation: SAT on each of the 8 possible configurations of the five 4-pencils, with LRAT proofs checked by cake_lpr ([Proposition C3b](theorems.md#c3b))"
BAND = "band theorem"
BAND_NOTE = ("The types marked \"band theorem\" are excluded by [Theorem B4](theorems.md#bands): removing the largest "
             "pencil leaves a configuration that no arrangement of the remaining lines produces.\n")


def main(nmax):
    out = ["---", 'description: "The pencil types that pass the combinatorial test but cannot be drawn with straight lines, '
           'for each number of lines, with the reason for each and the types still undecided."', "---", "",
           "# What cannot be drawn", "",
           "Most arithmetically admissible pencil types cannot be drawn. This page lists, for each number of lines, "
           "the types that survive the combinatorial test but are still impossible, together with the reason, and "
           "the types that are undecided. Types that already fail the combinatorial test (the pencils cannot be placed so "
           "that every two lines meet only once) or one of the classical inequalities are only counted; the full lists are in "
           "`data/results/classification_n{n}.json`.", "",
           "## Three famous impossible pictures", "",
           "Each of these is a perfectly good linear space, and the last two even exist with complex coordinates, "
           "but no drawing with straight real lines exists. Dashed curves mark the lines that would have to bend.", "",
           '<div class="figs" markdown>', ""]
    for f, cap in (("fano.svg", "The Fano plane, type {3<sup>7</sup>} for 7 lines: there is no ordinary point at all, which the Sylvester–Gallai theorem forbids."),
                   ("moebius-kantor.svg", "The Möbius–Kantor configuration, type {3<sup>8</sup>} for 8 lines: it passes every inequality, but admits no orientation."),
                   ("hesse.svg", "The Hesse configuration: nine points, every pair on a line of three. Dually, nine lines of type {3<sup>12</sup>}, the dual Hesse arrangement.")):
        out += ['<figure markdown="1">', "", f'--8<-- "fig/{f}"', "", f"<figcaption>{cap}</figcaption>", "</figure>", ""]
    out += ["</div>", ""]
    for n in range(4, nmax + 1):
        fn = os.path.join(ROOT, "data", "results", "classification_n%d.json" % n)
        if not os.path.exists(fn):
            continue
        rows = json.load(open(fn))
        cnt = Counter(r["verdict"] for r in rows)
        out.append(f"## {n} lines\n")
        parts = [f"{len(rows)} admissible types", f"{cnt['real']} realizable"]
        if cnt["no-linear-space"]:
            k = cnt['no-linear-space']
            parts.append(f"{k} {'fails' if k == 1 else 'fail'} the combinatorial test")
        ineq = cnt["melchior"] + cnt["csima-sawyer"] + cnt["debruijn-erdos"]
        if ineq:
            parts.append(f"{ineq} {'fails' if ineq == 1 else 'fail'} an inequality (Melchior or Csima–Sawyer)")
        if cnt["open"]:
            parts.append(f"{cnt['open']} undecided")
        out.append("; ".join(parts) + ".\n")
        if n == 13:
            out.append("These totals record the local classification. "
                       "[Kim's complete combinatorial table](sequences/combinatorial.md#mark-kims-extension-to-15-points) "
                       "contains 729 possible types and includes all 39 undecided real types.\n")
        if any(r["verdict"] in ("melchior", "csima-sawyer") and r.get("linear_space") is None for r in rows):
            out.append("For this number of lines the inequalities were checked first, and only the types that pass them "
                       "went to the combinatorial test, so the count of combinatorial failures covers those types only.\n")
        special = [r for r in rows if r["verdict"] in REASON or (r["verdict"] == "theorem" and "bands" in r.get("reference", ""))]
        if special:
            if any("bands" in r.get("reference", "") for r in special):
                out.append(BAND_NOTE)
            out.append("| type | points | why it cannot be drawn |\n|---|---|---|")
            for r in sorted(special, key=lambda r: (-sum(r["type"]), r["type"])):
                ref = r.get("reference", "")
                why = BAND if "bands" in ref else ORCH if "orchard12" in ref else SPLIT if "orient_split" in ref else REASON[r["verdict"]]
                out.append(f"| {utype(r['type'])} | {r['f0']} | {why} |")
            out.append("")
        openr = [r for r in rows if r["verdict"] == "open"]
        if openr:
            k = len(openr)
            out.append(f'<details><summary>{k} undecided {"type" if k == 1 else "types"}</summary>\n')
            out.append(", ".join(utype(r["type"]) for r in sorted(openr, key=lambda r: (-sum(r["type"]), r["type"]))) + ".\n")
            out.append("</details>\n")
        ineqr = [r for r in rows if r["verdict"] in ("melchior", "csima-sawyer", "debruijn-erdos")]
        if ineqr:
            k = len(ineqr)
            out.append(f'<details><summary>{k} {"type" if k == 1 else "types"} excluded by an inequality</summary>\n')
            out.append(", ".join(utype(r["type"]) for r in sorted(ineqr, key=lambda r: (-sum(r["type"]), r["type"]))) + ".\n")
            out.append("</details>\n")
    with open(os.path.join(ROOT, "docs", "impossible.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    print("docs/impossible.md written")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 13)
