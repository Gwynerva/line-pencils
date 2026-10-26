"""Exclude the type {4^5, 3^9} for 12 lines: no linear space of this type is orientable.

Elements 0..11 are the lines, blocks are the pencils.  Two blocks share at most one line, so the five
4-blocks are described, up to relabelling, by the lines that lie in at least two of them: a family F of
subsets (of size >= 2) of the five 4-blocks in which two members share at most one block.  Every block has
4 lines, so the other incidences are lines in exactly one 4-block, and the remaining lines are in none.
Only 8 of these configurations fit into 12 lines (there are 20 incidences on 12 lines).

For each of the 8 cases the 4-blocks are fixed and SAT decides whether an ORIENTABLE linear space of type
{4^5, 3^9} with exactly these 4-blocks exists (the encoding of scripts/sat_orient.py: chirotope signs with
the 3-term Grassmann-Pluecker relations, plus unit clauses for the 4-blocks).  Result: all 8 cases are
unsatisfiable, with three different solvers.  As a control, the realizable type {4^5, 3^8} gives a
satisfiable instance in every case.  Hence no arrangement of 12 lines, not even of pseudolines, has type
{4^5, 3^9}.

usage: python scripts/orient_split.py [OUT.json]       (default runs/orient_split_12.json)
       python scripts/orient_split.py --control        (the same cases for {4^5, 3^8}; all must be YES)
"""
import itertools, json, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCKS = range(5)
SUBSETS = [frozenset(c) for r in (2, 3, 4, 5) for c in itertools.combinations(BLOCKS, r)]
SOLVERS = ("cadical195", "glucose4", "maplechrono")


def families():
    """all families F of subsets of the five 4-blocks, members pairwise sharing <= 1 block, degrees <= 4"""
    out = []

    def rec(start, fam, pairs, deg):
        out.append(fam)
        for i in range(start, len(SUBSETS)):
            s = SUBSETS[i]
            pr = {frozenset(p) for p in itertools.combinations(sorted(s), 2)}
            if pr & pairs or any(deg[b] == 4 for b in s):
                continue
            rec(i + 1, fam + [s], pairs | pr, [d + (b in s) for b, d in enumerate(deg)])
    rec(0, [], set(), [0] * 5)
    return out


def canon(fam):
    return min(tuple(sorted(tuple(sorted(p[b] for b in s)) for s in fam)) for p in itertools.permutations(BLOCKS))


def blocks_of(fam):
    """the five 4-blocks on lines 0..11 (block 0 = {0,1,2,3}), or None if 12 lines do not suffice"""
    lines = [set(s) for s in fam]
    for b in BLOCKS:
        lines += [{b}] * (4 - sum(1 for s in fam if b in s))
    if len(lines) > 12:
        return None
    lines += [set()] * (12 - len(lines))
    lines.sort(key=lambda s: 0 not in s)
    return [sorted(i for i in range(12) if b in lines[i]) for b in BLOCKS]


def cases():
    out = {}
    for fam in families():
        b = blocks_of(fam)
        if b is not None:
            out.setdefault(canon(fam), b)
    return list(out.values())


def solve(args):
    blocks4, n3, solver = args
    from sat_orient import build
    from pysat.solvers import Solver
    cl, xs, pool = build(12, [4] * 5 + [3] * n3)
    want = {tuple(b) for b in blocks4}
    for S, v in xs.items():
        if len(S) == 4:
            cl.append([v] if S in want else [-v])
    t0 = time.time()
    with Solver(name=solver, bootstrap_with=cl) as slv:
        ok = slv.solve()
    return {"blocks4": blocks4, "solver": solver, "status": "YES" if ok else "NO", "time": round(time.time() - t0, 1)}


if __name__ == "__main__":
    control = "--control" in sys.argv
    n3 = 8 if control else 9
    cs = cases()
    print("type {4^5, 3^%d}: %d cases for the 4-blocks" % (n3, len(cs)), flush=True)
    jobs = [(b, n3, s) for s in (SOLVERS[:1] if control else SOLVERS) for b in cs]
    with Pool(min(8, len(jobs))) as P:
        res = P.map(solve, jobs)
    for r in res:
        print("  %-12s %s %5.1fs  %s" % (r["solver"], r["status"], r["time"], r["blocks4"]))
    verdict = {r["status"] for r in res}
    print("all cases:", verdict)
    if not control:
        assert verdict == {"NO"}, "some case is not refuted"
        out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "runs", "orient_split_12.json")
        with open(out, "w") as f:
            json.dump({"type": [4] * 5 + [3] * 9, "cases": len(cs), "verdict": "NOT ORIENTABLE", "runs": res}, f, indent=0)
            f.write("\n")
