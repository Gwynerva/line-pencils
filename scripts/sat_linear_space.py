"""Independent check of the combinatorial sieve with a SAT solver.

Question: do blocks of the given sizes k_1, ..., k_m (all >= 3) exist on n points such that
any two blocks share at most one point?  (Then the uncovered pairs become 2-point lines and
the whole thing is a linear space with the prescribed t-vector.)

Encoding (nothing clever, so that it is easy to audit):
  * one Boolean variable x_S for every k-subset S of {0..n-1}, for every size k occurring in the type;
  * for every size k: exactly c_k of the variables {x_S : |S| = k} are true   (cardinality constraint);
  * for every pair {p, q}: at most one of the variables {x_S : {p,q} ⊆ S} is true  (blocks meet in <= 1 point);
  * symmetry breaking: the lexicographically first block of the largest size is {0, 1, ..., k-1}
    (valid because the point labels can be permuted).
The solver is CaDiCaL through python-sat.  Cardinality constraints use the sequential counter /
totalizer encodings of pysat.card.

usage: python scripts/sat_linear_space.py N OUT.json [--workers W] [--only ...] [--filter all|theorems]
"""
import argparse, json, os, sys, time
from itertools import combinations
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pencils import candidates, theorem_ok, key, unkey


def solve(args):
    n, s = args
    from pysat.formula import CNF, IDPool
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    from collections import Counter
    t0 = time.time()
    cnt = Counter(s)
    pool = IDPool()
    var = {}
    for k in cnt:
        for S in combinations(range(n), k):
            var[S] = pool.id(S)
    cnf = CNF()
    for k, c in cnt.items():
        lits = [var[S] for S in combinations(range(n), k)]
        cnf.extend(CardEnc.equals(lits=lits, bound=c, vpool=pool, encoding=EncType.seqcounter).clauses)
    for p, q in combinations(range(n), 2):
        lits = [v for S, v in var.items() if p in S and q in S]
        if len(lits) > 1:
            cnf.extend(CardEnc.atmost(lits=lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses)
    if s:
        kmax = max(s)
        cnf.append([var[tuple(range(kmax))]])
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as slv:
        ok = slv.solve()
        blocks = None
        if ok:
            model = set(l for l in slv.get_model() if l > 0)
            blocks = [list(S) for S, v in var.items() if v in model]
    return key(s), {"status": "YES" if ok else "NO", "time": round(time.time() - t0, 2), "vars": pool.top,
                    "clauses": len(cnf.clauses), "blocks": blocks}


def _replace(src, dst):
    for attempt in range(50):
        try:
            os.replace(src, dst); return
        except PermissionError:
            time.sleep(0.2)
    os.replace(src, dst)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("out")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--only", default=None)
    ap.add_argument("--filter", default="all", choices=["all", "theorems"])
    a = ap.parse_args()
    n = a.n
    todo = [unkey(k) for k in a.only.split(";")] if a.only else candidates(n)
    if a.filter == "theorems":
        todo = [s for s in todo if theorem_ok(n, s)]
    res = json.load(open(a.out)) if os.path.exists(a.out) else {}
    work = [s for s in todo if key(s) not in res]
    work.sort(key=lambda s: (-len(s), s))
    print(f"n={n} total={len(todo)} todo={len(work)}", flush=True)
    t0 = time.time(); done = 0
    with Pool(a.workers) as P:
        for k, r in P.imap_unordered(solve, [(n, s) for s in work]):
            res[k] = r; done += 1
            if done % 25 == 0 or r["time"] > 5:
                print(f"[{done}/{len(work)} {time.time()-t0:.0f}s] {unkey(k)} {r['status']} {r['time']}s", flush=True)
            if done % 10 == 0:
                json.dump(res, open(a.out + ".tmp", "w"), indent=0, sort_keys=True); _replace(a.out + ".tmp", a.out)
    json.dump(res, open(a.out + ".tmp", "w"), indent=0, sort_keys=True); _replace(a.out + ".tmp", a.out)
    from collections import Counter
    print("done", dict(Counter(v["status"] for k, v in res.items() if unkey(k) in set(todo))), f"{time.time()-t0:.0f}s")
