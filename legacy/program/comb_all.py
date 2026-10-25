import sys, json, subprocess, time, os
from cands import candidates
n = int(sys.argv[1]); secs = float(sys.argv[2])
cs = candidates(n)
out = {}
p = subprocess.Popen(["./ls"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
t0 = time.time()
for s in cs:
    p.stdin.write(f"{n} 0 {secs} {' '.join(map(str,s))}\n"); p.stdin.flush()
    out[json.dumps(list(s))] = p.stdout.readline().split()[0]
p.stdin.close(); p.wait()
json.dump(out, open(f"comb_all_{n}.json", "w"))
from collections import Counter
print(n, Counter(out.values()), f"{time.time()-t0:.0f}s", flush=True)
