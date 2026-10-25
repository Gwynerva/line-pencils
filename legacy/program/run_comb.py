import sys, json, subprocess, time
from cands import candidates
n = int(sys.argv[1]); secs = float(sys.argv[2]) if len(sys.argv)>2 else 30
cs = candidates(n)
inp = "".join(f"{n} 0 {secs} {' '.join(map(str,c))}\n" for c in cs)
t0 = time.time()
out = subprocess.run(["./ls"], input=inp, capture_output=True, text=True).stdout.strip().split("\n")
res = {}
st = {"YES":0,"NO":0,"TIMEOUT":0}
for c, line in zip(cs, out):
    s = line.split()[0]; st[s]+=1
    blocks = []
    if "|" in line:
        blocks = [list(map(int,b.split(","))) for b in line.split("|")[1].split()]
    res[json.dumps(list(c))] = [s, blocks]
json.dump(res, open(f"combC_{n}.json","w"))
print(n, len(cs), st, f"{time.time()-t0:.1f}s", flush=True)
