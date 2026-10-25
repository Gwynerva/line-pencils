import random, sys, time, json, os
from pool import Pool, State, anneal
from pools_build import all_pools
from db import load, save, put

def missing_targets(n, db):
    f = f"combC_{n}.json"
    if not os.path.exists(f): return []
    d = json.load(open(f))
    have = db.get(n, {})
    return [tuple(json.loads(k)) for k, v in d.items() if v[0] == "YES" and tuple(json.loads(k)) not in have]

def main(nmin, nmax, secs, seed):
    rng = random.Random(seed)
    t0 = time.time()
    pools = all_pools(rng)
    print("pools built", len(pools), f"{time.time()-t0:.0f}s", [ (p.name, len(p.pts)) for p in pools], flush=True)
    db = load()
    new = 0
    rec = {}
    while time.time() - t0 < secs:
        pool = rng.choice(pools)
        n = rng.randint(nmin, nmax)
        if len(pool.pts) < n: continue
        miss = missing_targets(n, db)
        if miss and rng.random() < 0.7:
            target = rng.choice(miss)
        else:
            # random target: a signature with many 3s/4s
            target = tuple(sorted([rng.choice([3,3,3,4,4,5]) for _ in range(rng.randint(1, 2*n))], reverse=True))
        record = {}
        res = anneal(pool, n, target, 3000, rng, record=record)
        for sig, S in record.items():
            if put(db, n, sig, pool.d, [pool.pts[i] for i in S], pool.name):
                new += 1
                print("new", n, sig, pool.name, flush=True)
        if new and rng.random() < 0.05: save(db)
    save(db)
    print({n: len(m) for n, m in sorted(db.items())})

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
