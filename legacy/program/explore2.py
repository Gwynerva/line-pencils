import random, sys, time, json, os
from pool import Pool, anneal, with_intersections
from pools_build import all_pools, polygon_pool_points, torsion_points, grid_points, tri_lattice
from db import load, save, put

_cache = {}
def targets(n, db):
    f = f"engine_{n}.json"
    if not os.path.exists(f): return []
    t = time.time()
    if n not in _cache or t - _cache[n][0] > 30:
        try: _cache[n] = (t, json.load(open(f)))
        except Exception: _cache.setdefault(n, (t, {}))
    d = _cache[n][1]; have = db.get(n, {})
    return [tuple(json.loads(k)) for k, v in d.items() if v.get("m0") == "YES" and v.get("m1") != "NO" and tuple(json.loads(k)) not in have]

def extra_pools(rng):
    pools = []
    for m in (5, 10, 8, 12, 6):
        d, pts = polygon_pool_points(m)
        p1 = with_intersections(pts, d, maxadd=80, minrich=3, rng=rng)
        pools.append(Pool(p1, f"poly{m}+X80", d))
        p2 = with_intersections(pts, d, maxadd=60, minrich=2, rng=rng)
        pools.append(Pool(p2, f"poly{m}+X2", d))
    for N in (12, 10, 9):
        tp = torsion_points(N, 2)
        pools.append(Pool(with_intersections(tp, 0, maxadd=120, minrich=3, rng=rng), f"E{N}+X120"))
    return pools

def main(nlist, secs, seed):
    rng = random.Random(seed)
    t0 = time.time()
    pools = all_pools(rng) + extra_pools(rng)
    print("pools", [(p.name, len(p.pts)) for p in pools], f"{time.time()-t0:.0f}s", flush=True)
    db = load()
    while time.time() - t0 < secs:
        n = rng.choice(nlist)
        tg = targets(n, db)
        if not tg: continue
        target = rng.choice(tg)
        pool = rng.choice([p for p in pools if len(p.pts) >= n])
        record = {}
        anneal(pool, n, target, 4000, rng, record=record)
        for sig, S in record.items():
            if put(db, n, sig, pool.d, [pool.pts[i] for i in S], pool.name):
                print("new", n, sig, pool.name, flush=True)
                save(db)
    save(db)
    print("remaining targets", {n: targets(n, db) for n in nlist})

if __name__ == "__main__":
    main([int(x) for x in sys.argv[1].split(",")], float(sys.argv[2]), int(sys.argv[3]))
