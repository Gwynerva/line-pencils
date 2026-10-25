import random, sys, json, time, os
from geom import *
from math import comb

def grid_pool(m, dirs=True, dmax=2):
    pool = [(x,y,1) for x in range(m) for y in range(m)]
    if dirs:
        ds=set()
        for a in range(-dmax,dmax+1):
            for b in range(-dmax,dmax+1):
                v = norm((a,b,0))
                if v: ds.add(v)
        pool += sorted(ds)
    return pool

def tri_pool(r):
    # triangular lattice in coordinates (a,b) with a+b<=r etc, plus directions
    pool = [(a,b,1) for a in range(-r,r+1) for b in range(-r,r+1) if abs(a)+abs(b)+abs(a+b) <= 2*r]
    pool += [(1,0,0),(0,1,0),(1,-1,0),(1,1,0),(2,-1,0),(1,-2,0)]
    return pool

def closure_config(n, rng):
    """Random 'constructible' config: points added as intersections of spanned lines,
    points on spanned lines, or random points."""
    P = []
    S = set()
    def add(p):
        p = norm(p)
        if p is None or p in S: return False
        P.append(p); S.add(p); return True
    base = rng.randint(3,4)
    while len(P) < base:
        add((rng.randint(-5,5), rng.randint(-5,5), rng.choice([1,1,1,0])))
    tries = 0
    while len(P) < n and tries < 200:
        tries += 1
        r = rng.random()
        if r < 0.75 and len(P) >= 4:
            a,b,c,d = rng.sample(P,4)
            L1 = cross(a,b); L2 = cross(c,d)
            add(cross(L1,L2))
        elif r < 0.9 and len(P)>=2:
            a,b = rng.sample(P,2)
            s,t = rng.randint(-4,4), rng.randint(-4,4)
            add(tuple(s*a[i]+t*b[i] for i in range(3)))
        else:
            add((rng.randint(-9,9), rng.randint(-9,9), rng.choice([1,1,1,0])))
    return P if len(P)==n else None

def run(nmax, seconds, out):
    rng = random.Random(int.from_bytes(os.urandom(8),'little'))
    found = {n:{} for n in range(1,nmax+1)}
    if os.path.exists(out):
        d = json.load(open(out))
        for n,v in d.items():
            if int(n) <= nmax: found[int(n)] = {tuple(json.loads(k)):p for k,p in v.items()}
    pools = [grid_pool(3), grid_pool(4), grid_pool(5), grid_pool(4,dmax=3), grid_pool(6,dirs=False), tri_pool(2), tri_pool(3)]
    t0 = time.time(); it = 0
    while time.time()-t0 < seconds:
        it += 1
        n = rng.randint(3, nmax)
        if rng.random() < 0.5:
            pool = rng.choice(pools)
            if len(pool) < n: continue
            P = rng.sample(pool, n)
        else:
            P = closure_config(n, rng)
            if P is None: continue
        s = signature(P)
        if s is None: continue
        if s not in found[n]:
            found[n][s] = [list(p) for p in P]
    json.dump({n:{json.dumps(list(k)):v for k,v in d.items()} for n,d in found.items()}, open(out,'w'))
    return found, it

if __name__ == "__main__":
    nmax = int(sys.argv[1]); secs = float(sys.argv[2]); out = sys.argv[3]
    found, it = run(nmax, secs, out)
    print("iterations", it)
    for n in range(1,nmax+1): print(n, len(found[n]))
