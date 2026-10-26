"""Generate the data-driven tables of the site into snippets/ (included with pymdownx.snippets).

usage: python scripts/build_tables.py
Produces:
  snippets/open12.md       table of the types for n = 12 that pass the inequalities but were hard to decide
  snippets/sequences.md    the main sequence table with per-term status
  snippets/counts.md       a(n), b(n), c(n), d(n) one-line summaries used in several pages
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
    return f"<span class=\"status-bound\">{v[0]} … {v[1]}</span>" if isinstance(v, list) else str(v)


# ---- open12 table
rows = load("data/results/classification_n12.json")
orient = {}
for src in ("runs/orient_12.json", "runs/sat_orient_12.json"):
    for k, v in load(src).items():
        if v.get("status") in ("YES", "NO"):
            orient[k] = (v["status"], src.split("/")[-1], v.get("time"))
lines = ["| type | $f_0$ | orientable? | status |", "|---|---|---|---|"]
notes = {}
recent = {"3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3": "realizable: found by the zone walk ([algorithms](../algorithms.md#zone-walk)), integer coefficients"}
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
        st = "not realizable: no orientable linear space"
    elif r["verdict"] == "non-realizable-proved":
        st = "not realizable although orientable: Gröbner certificate for every orientable linear space ([Theorems C4, C5](../theorems.md#lines-vs-pseudolines))"
    elif r["verdict"] == "theorem" and "orchard12" in r.get("reference", ""):
        st = "not realizable: none of its linear spaces is orientable ([Proposition C3a](../theorems.md))"
    elif r["verdict"] == "theorem" and "orient_split" in r.get("reference", ""):
        st = "not realizable: none of its linear spaces is orientable ([Proposition C3b](../theorems.md))"
    elif r["verdict"] == "theorem":
        st = "not realizable: theorem (dual Hesse configuration + Sylvester–Gallai)"
    else:
        st = "not realizable: orchard bound $t_3 \\le 19$ (Burr–Grünbaum–Sloane)"
    lines.append(f"| ${tex(t)}$ | {r['f0']} | {ostr} | {st} |")
open(os.path.join(OUT, "open12.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

# ---- sequence table
hdr = ["| $n$ | $a(n)$ arithmetic | $b(n)$ combinatorial | $c(n)$ realizable | $d(n)$ values of $f_0$ |", "|---|---|---|---|---|"]
body = []
for i in range(len(seq["a"])):
    body.append(f"| {i+1} | {cell(seq['a'][i])} | {cell(seq['b'][i])} | {cell(seq['c'][i])} | {cell(seq['d'][i])} |")
open(os.path.join(OUT, "sequences.md"), "w", encoding="utf-8").write("\n".join(hdr + body) + "\n")

# ---- counts
def seqstr(q):
    return ", ".join(str(v) if not isinstance(v, list) else f"[{v[0]}…{v[1]}]" for v in seq[q])
open(os.path.join(OUT, "counts.md"), "w", encoding="utf-8").write(
    "\n".join([f"* $a(n)$: {seqstr('a')}", f"* $b(n)$: {seqstr('b')}", f"* $c(n)$: {seqstr('c')}", f"* $d(n)$: {seqstr('d')}"]) + "\n")
print("tables written; open types at n=12:", sum(1 for r in rows if r["verdict"] == "open"))
