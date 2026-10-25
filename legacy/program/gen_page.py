import json, sys
from final_tables import classify
nmax = int(sys.argv[1]); out = sys.argv[2]
T = classify(nmax)
A = json.load(open("atlas_data.json"))
DATA, STATS, IMP = {}, {}, {}
for n in range(2, nmax + 1):
    rows = T[n]
    if any(r[1] == "open" for r in rows): raise SystemExit(f"n={n} still has open cases")
    real = [r for r in rows if r[1] == "real"]
    real.sort(key=lambda r: list(r[0]) + [0], reverse=True)   # pencil first ... no pencils last
    items = []
    for s, _, d in real:
        key = json.dumps(list(s))
        dd = A[str(n)][key]
        if n == 10 and list(s) == [5] + [3]*10:
            dd = json.load(open("star.json"))
        items.append({"s": list(s), "L": dd["lines"], "P": [[p[0], p[1], p[2]] for p in dd["points"]], "d": d or 0})
    DATA[n] = items
    try: combyes = sum(1 for v in json.load(open(f"comb_all_{n}.json")).values() if v == "YES")
    except FileNotFoundError: combyes = len(rows)
    if n <= 2: combyes = len(real)
    STATS[n] = {"arith": len(rows), "comb": combyes, "real": len(real)}
    IMP[n] = [{"s": list(s), "r": r} for s, r, _ in rows if r != "real"]
html = open("atlas_template.html").read()
html = html.replace("/*DATA*/", json.dumps(DATA, separators=(",", ":")))
html = html.replace("/*STATS*/", json.dumps(STATS, separators=(",", ":")))
html = html.replace("/*IMP*/", json.dumps(IMP, separators=(",", ":")))
open(out, "w").write(html)
print("written", out, len(html)//1024, "KB", {n: STATS[n]["real"] for n in STATS})
