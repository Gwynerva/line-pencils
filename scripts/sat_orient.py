"""Orientability sieve by SAT: is there an ORIENTABLE linear space with the given pencil sizes?

An arrangement of n real lines gives (dually) n points of RP^2; the sign of the determinant
chi(a,b,c) = sign det(p_a, p_b, p_c) is a chirotope: an alternating map {triples} -> {+,0,-}
whose zero set is exactly the set of collinear triples, satisfying the 3-term Grassmann-Pluecker
relations: for every a and every x1 < x2 < x3 < x4 (all different from a) the three numbers
      chi(a x1 x2) chi(a x3 x4),   - chi(a x1 x3) chi(a x2 x4),   chi(a x1 x4) chi(a x2 x3)
are either all zero or contain both a positive and a negative one.
(Bjorner-Las Vergnas-Sturmfels-White-Ziegler, Oriented Matroids, Thm 3.6.2 / Def. 3.5.3.)
So: no orientable linear space with the prescribed block sizes => no real arrangement.

Encoding (CNF, solved by CaDiCaL via python-sat):
  * block variables x_S (S a k-subset, k a size in the type) with the cardinality constraints of
    scripts/sat_linear_space.py (exactly c_k blocks of size k, two blocks share <= 1 point);
  * collinearity variables col_T for every triple T, with col_T <-> OR_{S contains T} x_S;
  * sign variables sgn_T (sgn = true means chi(T) = + for T in increasing order);
  * for every GP relation (a; x1 x2 x3 x4) and each of its three terms t: aux variables
        zero_t  = col(first triple) or col(second triple)
        plus_t  = not zero_t and (value of the term is +)
        minus_t = not zero_t and (value of the term is -)
    where the value is sgn(T1) xor sgn(T2) xor (permutation parities) xor (t == 2);
    and the clauses  (zero_t or plus_1 or plus_2 or plus_3), (zero_t or minus_1 or minus_2 or minus_3)
    for t = 1,2,3: if any term is non-zero, both signs occur.
  * symmetry breaking: the first block of the largest size is {0..k-1}; reorientation freedom is
    used to fix sgn(0,1,x) = + whenever (0,1,x) is not collinear.

usage: python scripts/sat_orient.py N OUT.json [--only "k,k,..;k,k,.."] [--workers W] [--timeout S]
       python scripts/sat_orient.py --test
"""
import argparse, json, os, sys, time
from itertools import combinations
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pencils import candidates, theorem_ok, key, unkey


def parity3(a, b, c):
    p = 0
    if a > b: p ^= 1
    if a > c: p ^= 1
    if b > c: p ^= 1
    return p


def build(n, sizes, fixed_blocks=None):
    """Return (clauses, var dict, pool).  If fixed_blocks is given, the linear space is fixed
    (unit clauses for its blocks) and only the chirotope is searched."""
    from pysat.formula import IDPool
    from pysat.card import CardEnc, EncType
    from collections import Counter
    pool = IDPool()
    cl = []
    cnt = Counter(sizes)
    xs = {}
    for k in cnt:
        for S in combinations(range(n), k):
            xs[S] = pool.id(("x",) + S)
    for k, c in cnt.items():
        lits = [xs[S] for S in combinations(range(n), k)]
        cl += CardEnc.equals(lits=lits, bound=c, vpool=pool, encoding=EncType.seqcounter).clauses
    for p, q in combinations(range(n), 2):
        lits = [v for S, v in xs.items() if p in S and q in S]
        if len(lits) > 1:
            cl += CardEnc.atmost(lits=lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses
    if fixed_blocks is not None:
        want = {tuple(sorted(B)) for B in fixed_blocks}
        for S, v in xs.items():
            cl.append([v] if S in want else [-v])
    elif sizes:
        cl.append([xs[tuple(range(max(sizes)))]])
    col = {}; sgn = {}
    for T in combinations(range(n), 3):
        col[T] = pool.id(("c",) + T); sgn[T] = pool.id(("s",) + T)
        sup = [v for S, v in xs.items() if set(T) <= set(S)]
        # col_T <-> OR sup
        cl.append([-col[T]] + sup)
        for v in sup:
            cl.append([col[T], -v])
    # reorientation normalisation: sgn(0,1,x) = + unless collinear
    for x in range(2, n):
        T = (0, 1, x)
        cl.append([col[T], sgn[T]])

    def chi(a, b, c):
        T = tuple(sorted((a, b, c)))
        return col[T], sgn[T], parity3(a, b, c)

    for a in range(n):
        others = [x for x in range(n) if x != a]
        for x1, x2, x3, x4 in combinations(others, 4):
            terms = []
            for (p, q, r, s, neg) in ((x1, x2, x3, x4, 0), (x1, x3, x2, x4, 1), (x1, x4, x2, x3, 0)):
                c1, s1, p1 = chi(a, p, q); c2, s2, p2 = chi(a, r, s)
                z = pool.id(); pl = pool.id(); mi = pool.id()
                # z <-> c1 or c2
                cl.append([-z, c1, c2]); cl.append([z, -c1]); cl.append([z, -c2])
                # value v = s1 xor s2 xor const, const = p1^p2^neg;  plus <-> (not z) and v ; minus <-> (not z) and not v
                const = p1 ^ p2 ^ neg
                # v is true iff s1 xor s2 == 1 xor const  (v = + means term positive)
                # encode plus: plus -> not z ; plus -> (s1 xor s2 = 1^const); (not z and s1 xor s2 = 1^const) -> plus
                for aux, want in ((pl, 1 ^ const), (mi, 0 ^ const)):
                    cl.append([-aux, -z])
                    # aux -> (s1 xor s2 == want)
                    if want == 1:
                        cl.append([-aux, s1, s2]); cl.append([-aux, -s1, -s2])
                        # (not z) and (s1 xor s2) -> aux
                        cl.append([z, aux, -s1, s2]); cl.append([z, aux, s1, -s2])
                    else:
                        cl.append([-aux, s1, -s2]); cl.append([-aux, -s1, s2])
                        cl.append([z, aux, s1, s2]); cl.append([z, aux, -s1, -s2])
                terms.append((z, pl, mi))
            zs = [t[0] for t in terms]; pls = [t[1] for t in terms]; mis = [t[2] for t in terms]
            for z in zs:
                cl.append([z] + pls); cl.append([z] + mis)
    return cl, xs, pool


def solve(args):
    n, s, timeout = args
    from pysat.solvers import Solver
    t0 = time.time()
    cl, xs, pool = build(n, s)
    res = {"vars": pool.top, "clauses": len(cl)}
    with Solver(name="cadical195", bootstrap_with=cl) as slv:
        if timeout:
            import threading
            timer = threading.Timer(timeout, lambda: slv.interrupt()); timer.start()
            ok = slv.solve_limited(expect_interrupt=True)
            timer.cancel()
        else:
            ok = slv.solve()
        if ok is None:
            res["status"] = "TIMEOUT"
        else:
            res["status"] = "YES" if ok else "NO"
            if ok:
                model = set(l for l in slv.get_model() if l > 0)
                res["blocks"] = [list(S) for S, v in xs.items() if v in model]
    res["time"] = round(time.time() - t0, 2)
    return key(s), res


def orientable_fixed(n, blocks):
    """Is this particular linear space orientable? (chirotope existence only)"""
    from pysat.solvers import Solver
    sizes = [len(B) for B in blocks]
    cl, xs, pool = build(n, sizes, fixed_blocks=blocks)
    with Solver(name="cadical195", bootstrap_with=cl) as slv:
        return slv.solve()


def _replace(src, dst):
    for attempt in range(50):
        try:
            os.replace(src, dst); return
        except PermissionError:
            time.sleep(0.2)
    os.replace(src, dst)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        fano = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
        print("Fano orientable?", orientable_fixed(7, fano), "(expect False)")
        mk = [tuple(sorted({i % 8, (i + 1) % 8, (i + 3) % 8})) for i in range(8)]
        print("Moebius-Kantor orientable?", orientable_fixed(8, mk), "(expect False)")
        pappus = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (0, 5, 7), (1, 3, 8), (1, 5, 6), (2, 3, 7), (2, 4, 6)]
        print("Pappus orientable?", orientable_fixed(9, pappus), "(expect True)")
        print("non-Pappus orientable?", orientable_fixed(9, pappus[:-1]), "(expect True)")
        for n, s, exp in ((7, (3,) * 7, "NO"), (8, (3,) * 8, "NO"), (9, (3,) * 12, "NO"), (9, (3,) * 10, "YES"), (11, (3,) * 16, "YES"), (10, (5,) + (3,) * 10, "YES")):
            k, r = solve((n, s, None))
            print(n, s, r["status"], r["time"], "s  (expect", exp + ")")
        sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("out")
    ap.add_argument("--only", default=None); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=None); ap.add_argument("--filter", default="all")
    a = ap.parse_args()
    n = a.n
    todo = [unkey(k) for k in a.only.split(";")] if a.only else candidates(n)
    if a.filter == "theorems":
        todo = [s for s in todo if theorem_ok(n, s)]
    res = json.load(open(a.out)) if os.path.exists(a.out) else {}
    work = [s for s in todo if key(s) not in res or res[key(s)]["status"] == "TIMEOUT"]
    work.sort(key=lambda s: (-len(s), s))
    print(f"n={n} total={len(todo)} todo={len(work)}", flush=True)
    t0 = time.time()
    with Pool(a.workers) as P:
        for k, r in P.imap_unordered(solve, [(n, s, a.timeout) for s in work]):
            res[k] = r
            print(f"[{time.time()-t0:.0f}s] {unkey(k)} {r['status']} {r['time']}s", flush=True)
            json.dump(res, open(a.out + ".tmp", "w"), indent=0, sort_keys=True); _replace(a.out + ".tmp", a.out)
    from collections import Counter
    print("done", dict(Counter(v["status"] for v in res.values())), f"{time.time()-t0:.0f}s")
