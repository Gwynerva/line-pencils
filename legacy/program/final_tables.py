# Final classification of every arithmetic candidate for n <= NMAX.
import json, os, sys
from math import comb
from cands import candidates
from status import melchior_ok, cs_ok
from db import load
def classify(nmax):
    db = load()
    table = {}
    for n in range(1, nmax + 1):
        rows = []
        combf = json.load(open(f"comb_all_{n}.json")) if os.path.exists(f"comb_all_{n}.json") else {}
        eng = json.load(open(f"engine_{n}.json")) if os.path.exists(f"engine_{n}.json") else {}
        for s in candidates(n):
            k = json.dumps(list(s))
            if n <= 2:
                rows.append((s, "real", 0)); continue
            if s in db.get(n, {}):
                rows.append((s, "real", db[n][s]["d"])); continue
            c = combf.get(k)
            if c == "NO": rows.append((s, "comb", None)); continue
            if not melchior_ok(n, s): rows.append((s, "melchior", None)); continue
            if not cs_ok(n, s): rows.append((s, "cs", None)); continue
            e = eng.get(k, {})
            if e.get("m0") == "NO": rows.append((s, "comb", None)); continue
            if e.get("m1") == "NO": rows.append((s, "orient", None)); continue
            rows.append((s, "open", None))
        table[n] = rows
    return table
if __name__ == "__main__":
    nmax = int(sys.argv[1])
    T = classify(nmax)
    for n, rows in T.items():
        from collections import Counter
        c = Counter(r[1] for r in rows)
        combyes = sum(1 for r in rows if r[1] in ("real", "orient", "melchior", "cs", "open") ) - 0
        print(n, len(rows), dict(c))
