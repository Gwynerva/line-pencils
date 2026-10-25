"""Parallel driver for the exhaustive engine (engine/ls.c).

usage: python scripts/engine_run.py N MODE SECONDS OUT.json [--workers W]
           [--filter all|theorems] [--only k1,k2,...;k1,k2,... ] [--retry STATUS]

MODE 0: does a linear space with these pencils exist?        (combinatorial sieve)
MODE 4: does an orientable linear space exist (chirotope)?   (orientability sieve)
Each query gets SECONDS of CPU; result statuses are YES / NO / TIMEOUT.
Results are checkpointed into OUT.json after every answer (safe to interrupt and
re-run: finished queries are skipped unless --retry names their status).
"""
import argparse, json, os, subprocess, sys, time, threading, queue
sys.path.insert(0, os.path.dirname(__file__))
from pencils import candidates, theorem_ok, key, unkey

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine", "ls.exe" if os.name == "nt" else "ls")

ap = argparse.ArgumentParser()
ap.add_argument("n", type=int); ap.add_argument("mode", type=int); ap.add_argument("secs", type=float)
ap.add_argument("out")
ap.add_argument("--workers", type=int, default=os.cpu_count())
ap.add_argument("--filter", default="all", choices=["all", "theorems"])
ap.add_argument("--only", default=None, help="semicolon-separated comma-lists of pencil sizes")
ap.add_argument("--retry", default="", help="comma-separated statuses to re-run, e.g. TIMEOUT")
ap.add_argument("--order", default="hard", choices=["hard", "easy"], help="hard: many pencils first (load balance); easy: few pencils first")
args = ap.parse_args()

n, mode, secs = args.n, args.mode, args.secs
if args.only:
    todo = [unkey(k.strip()) for k in args.only.split(";") if k.strip() != ""]
else:
    todo = candidates(n)
    if args.filter == "theorems":
        todo = [s for s in todo if theorem_ok(n, s)]
res = json.load(open(args.out)) if os.path.exists(args.out) else {}
retry = set(x for x in args.retry.split(",") if x)
work = [s for s in todo if key(s) not in res or res[key(s)]["status"] in retry]
# hardest first (more pencils of size 3 tend to be slower) -> better load balance
work.sort(key=lambda s: (-len(s), s) if args.order == "hard" else (len(s), s))
print(f"n={n} mode={mode} secs={secs} total={len(todo)} todo={len(work)} workers={args.workers}", flush=True)

q = queue.Queue()
for s in work: q.put(s)
lock = threading.Lock()
t_start = time.time()
done = [0]

def save():
    tmp = args.out + ".tmp"
    with open(tmp, "w") as f: json.dump(res, f, indent=0, sort_keys=True)
    for attempt in range(50):                      # Windows: another reader may hold the file briefly
        try:
            os.replace(tmp, args.out); return
        except PermissionError:
            time.sleep(0.2)
    os.replace(tmp, args.out)

def worker(wid):
    p = subprocess.Popen([ENGINE], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    while True:
        try: s = q.get_nowait()
        except queue.Empty: break
        t0 = time.time()
        p.stdin.write(f"{n} {mode} {secs} {' '.join(map(str, s))}\n"); p.stdin.flush()
        line = p.stdout.readline().strip()
        dt = time.time() - t0
        head, _, tail = line.partition("|")
        st = head.split()[0]
        r = {"status": st, "mode": mode, "secs": secs, "time": round(dt, 2), "info": head.strip()}
        if tail.strip():
            r["blocks"] = [list(map(int, b.split(","))) for b in tail.split()]
        with lock:
            res[key(s)] = r; done[0] += 1
            save()
            if st != "YES" or done[0] % 50 == 0:
                print(f"[{done[0]}/{len(work)} {time.time()-t_start:.0f}s] {s} {st} {dt:.1f}s", flush=True)
    p.stdin.close(); p.wait()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(args.workers)]
for t in threads: t.start()
for t in threads: t.join()
from collections import Counter
print("done", dict(Counter(v["status"] for k, v in res.items() if unkey(k) in set(todo))), f"{time.time()-t_start:.0f}s", flush=True)
