"""Constructive search for a real arrangement of a given pencil type.

For a type (list of pencil sizes >= 3) on n lines:
  1. ask the SAT encoder of scripts/sat_orient.py for an ORIENTABLE linear space of that type;
  2. try to realize it numerically and reconstruct exact coordinates (scripts/realize.py);
  3. if that fails, add a blocking clause for this labelled linear space and go to 1
     (labelled solutions that are relabelings of an already tried one are skipped by a cheap
     isomorphism invariant);
  4. stop at the first verified certificate, or after --max linear spaces / --time seconds.

Found certificates are appended to data/certificates/n{n}.json (after verification).

usage: python scripts/find_examples.py N "k1,k2,..." [--max M] [--time T] [--starts S] [--seeds R]
"""
import argparse, json, os, sys, time
from collections import Counter
from itertools import combinations
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "verifier"))
from pencils import key, unkey, fmt
from sat_orient import build
from realize import realize_blocks
from verify import verify


def invariant(n, blocks):
    """Cheap isomorphism invariant: refined point 'colours' (Weisfeiler-Lehman style, 3 rounds)."""
    col = [tuple(sorted(len(B) for B in blocks if i in B)) for i in range(n)]
    for _ in range(3):
        new = []
        for i in range(n):
            nb = []
            for B in blocks:
                if i in B:
                    nb.append(tuple(sorted(col[j] for j in B if j != i)))
            new.append((col[i], tuple(sorted(nb))))
        col = new
    return tuple(sorted(col))


def add_certificate(cert):
    fn = os.path.join(ROOT, "data", "certificates", "n%d.json" % cert["n"])
    certs = json.load(open(fn)) if os.path.exists(fn) else []
    if any(sorted(c["type"], reverse=True) == sorted(cert["type"], reverse=True) for c in certs):
        return False
    certs.append(cert)
    certs.sort(key=lambda c: (-sum(c["type"]), c["type"]))
    with open(fn, "w") as f:
        json.dump(certs, f, separators=(",", ":")); f.write("\n")
    return True


def search(n, sizes, max_spaces=200, time_limit=1800, starts=40, seeds=3, verbose=True):
    from pysat.solvers import Solver
    t0 = time.time()
    cl, xs, pool = build(n, sizes)
    seen = set(); tried = 0; dup = 0
    with Solver(name="cadical195", bootstrap_with=cl) as slv:
        while tried < max_spaces and time.time() - t0 < time_limit:
            if not slv.solve():
                return None, {"status": "exhausted", "tried": tried, "dup": dup, "time": time.time() - t0}
            model = set(l for l in slv.get_model() if l > 0)
            blocks = [list(S) for S, v in xs.items() if v in model]
            slv.add_clause([-xs[tuple(S)] for S in blocks])     # block this labelled space
            inv = invariant(n, blocks)
            if inv in seen:
                dup += 1
                continue
            seen.add(inv); tried += 1
            for seed in range(seeds):
                cert = realize_blocks(n, blocks, seed=seed, starts=starts,
                                      source="SAT-found orientable linear space, numerical realization, exact reconstruction")
                if cert:
                    cert["blocks"] = blocks
                    return cert, {"status": "found", "tried": tried, "dup": dup, "time": time.time() - t0}
            if verbose:
                print(f"  [{time.time()-t0:.0f}s] linear space #{tried} not realized numerically", flush=True)
    return None, {"status": "limit", "tried": tried, "dup": dup, "time": time.time() - t0}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("type")
    ap.add_argument("--max", type=int, default=200); ap.add_argument("--time", type=float, default=1800)
    ap.add_argument("--starts", type=int, default=40); ap.add_argument("--seeds", type=int, default=3)
    a = ap.parse_args()
    n = a.n; sizes = list(unkey(a.type))
    print(f"n={n} type {fmt(sizes)}", flush=True)
    cert, info = search(n, sizes, a.max, a.time, a.starts, a.seeds)
    print(info)
    if cert:
        verify(cert)
        new = add_certificate(cert)
        print("CERTIFICATE", "added" if new else "already present", json.dumps(cert))
