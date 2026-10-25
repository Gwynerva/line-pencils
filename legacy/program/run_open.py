# Run the C engine (mode 0 then mode 1) on candidates that pass theorem filters and are not realized.
import sys, json, subprocess, time, os
from cands import candidates
from status import melchior_ok, cs_ok, debruijn_ok
from db import load
n = int(sys.argv[1]); mode = int(sys.argv[2]); secs = float(sys.argv[3])
db = load(); have = set(db.get(n, {}))
resfile = f"engine_{n}.json"
res = json.load(open(resfile)) if os.path.exists(resfile) else {}
todo = []
for s in candidates(n):
    if not (melchior_ok(n,s) and cs_ok(n,s) and debruijn_ok(n,s)): continue
    if s in have: continue
    key = json.dumps(list(s))
    r = res.get(key, {})
    if r.get("m0") == "NO": continue
    if mode == 0 and r.get("m0") in ("YES",): continue
    if mode == 1 and (r.get("m1") in ("YES","NO") or r.get("m0") != "YES"): continue
    todo.append(s)
print(n, "mode", mode, "todo", len(todo), flush=True)
p = subprocess.Popen(["./ls"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
t0 = time.time()
for s in todo:
    p.stdin.write(f"{n} {4 if mode == 1 else mode} {secs} {' '.join(map(str,s))}\n"); p.stdin.flush()
    line = p.stdout.readline().strip()
    st = line.split()[0]
    key = json.dumps(list(s))
    r = res.setdefault(key, {})
    r["m%d" % mode] = st
    if "|" in line:
        r["blocks%d" % mode] = [list(map(int,b.split(","))) for b in line.split("|")[1].split()]
    r["info%d" % mode] = line.split("|")[0]
    if st != "YES": print(s, line.split("|")[0], flush=True)
    json.dump(res, open(resfile + ".tmp", "w")); os.replace(resfile + ".tmp", resfile)
p.stdin.close(); p.wait()
from collections import Counter
print("done", Counter(v.get("m%d"%mode) for v in res.values()), f"{time.time()-t0:.0f}s")
