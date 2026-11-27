"""Generate the data-driven tables of the site into snippets/ (included with pymdownx.snippets).

usage: python scripts/build_tables.py
Produces:
  snippets/open12.md       table of the types for n = 12 that pass every inequality, with how each was decided
  snippets/sequences.md    the main sequence table (intervals for terms not known exactly)
"""
import json, os, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from pencils import fmt, f0, key, unkey
OUT = os.path.join(ROOT, "snippets")
os.makedirs(OUT, exist_ok=True)


def tex(t):
    c = Counter(t); parts = []
    for k in sorted(c, reverse=True):
        parts.append(f"{k}^{{{c[k]}}}" if c[k] > 1 else str(k))
    return "\\{" + ", ".join(parts) + "\\}" if parts else "\\{\\}"


def load(p):
    p = os.path.join(ROOT, p)
    return json.load(open(p)) if os.path.exists(p) else {}


seq = load("data/results/sequences.json")


def cell(v):
    if v is None:
        return "—"
    return f"<span class=\"status-bound\">{v[0]} … {v[1]}</span>" if isinstance(v, list) else str(v)


# ---- open12 table
rows = load("data/results/classification_n12.json")
orient = {}
for src in ("runs/orient_12.json", "runs/sat_orient_12.json"):
    for k, v in load(src).items():
        if v.get("status") in ("YES", "NO"):
            orient[k] = (v["status"], src.split("/")[-1], v.get("time"))
lines = ["| type | $f_0$ | orientable? | verdict |", "|---|---|---|---|"]
notes = {}
recent = {"3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3": "realizable ([Example C3c](../theorems.md#c3c))"}
sel = [r for r in rows if r["verdict"] in ("open", "non-orientable", "non-realizable-proved", "theorem", "literature")
       or key(tuple(r["type"])) in recent]
for r in sorted(sel, key=lambda r: (r["verdict"] != "open", key(tuple(r["type"])) not in recent, -sum(r["type"]), r["type"])):
    t = tuple(r["type"]); k = key(t)
    o = orient.get(k)
    if "orient_split" in r.get("reference", "") or "orchard12" in r.get("reference", ""):
        ostr = "no"
    elif o is None:
        ostr = "—"
    else:
        ostr = "no" if o[0] == "NO" else "yes"
    if k in recent:
        st = recent[k]
    elif r["verdict"] == "open":
        st = "**undecided**: " + notes.get(k, "the orientability search did not finish")
    elif r["verdict"] == "non-orientable":
        st = "non-orientable"
    elif r["verdict"] == "non-realizable-proved":
        st = "Gröbner ([C4, C5](../theorems.md#lines-vs-pseudolines))"
    elif r["verdict"] == "theorem" and "orchard12" in r.get("reference", ""):
        st = "non-orientable ([C3a](../theorems.md#c3a))"
    elif r["verdict"] == "theorem" and "orient_split" in r.get("reference", ""):
        st = "non-orientable ([C3b](../theorems.md#c3b))"
    elif r["verdict"] == "theorem":
        st = "Hesse arrangement ([C3](../theorems.md#c3))"
    else:
        st = "orchard bound $t_3 \\le 19$"
    lines.append(f"| ${tex(t)}$ | {r['f0']} | {ostr} | {st} |")
open(os.path.join(OUT, "open12.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

# ---- sequence table
hdr = ["| $n$ | $a(n)$ arithmetic | $b(n)$ combinatorial | $c(n)$ realizable | $d(n)$ values of $f_0$ |", "|---|---|---|---|---|"]
body = []
for i in range(len(seq["a"])):
    values = [seq[s][i] if i < len(seq[s]) else None for s in "abcd"]
    body.append("| %d | %s |" % (i + 1, " | ".join(map(cell, values))))
open(os.path.join(OUT, "sequences.md"), "w", encoding="utf-8", newline="\n").write("\n".join(hdr + body) + "\n")

print("tables written; open types at n=12:", sum(1 for r in rows if r["verdict"] == "open"))
