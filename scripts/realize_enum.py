"""Try to realize every orientable linear space listed by the engine in mode 5.

usage: python scripts/realize_enum.py N ENUMFILE [--starts S] [--seeds R] [--max M]
ENUMFILE: output of `printf 'N 5 SECS k1 k2 ...' | engine/ls5.exe`, lines "ORIENTABLE b1 b2 ..." with
blocks as comma-separated point indices.  Labelled spaces that are relabelings of an already tried
one (cheap invariant) are skipped.  The first verified certificate is appended to data/certificates.
"""
import argparse, json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "verifier"))
from realize import realize_blocks
from find_examples import invariant, add_certificate
from pencils import fmt

ap = argparse.ArgumentParser()
ap.add_argument("n", type=int); ap.add_argument("enumfile")
ap.add_argument("--starts", type=int, default=30); ap.add_argument("--seeds", type=int, default=2)
ap.add_argument("--max", type=int, default=10 ** 9)
a = ap.parse_args()
n = a.n
seen = set(); tried = 0; dup = 0; t0 = time.time()
for line in open(a.enumfile):
    if not line.startswith("ORIENTABLE"):
        continue
    blocks = [sorted(map(int, b.split(","))) for b in line.split()[1:]]
    inv = invariant(n, blocks)
    if inv in seen:
        dup += 1; continue
    seen.add(inv); tried += 1
    if tried > a.max:
        break
    for seed in range(a.seeds):
        cert = realize_blocks(n, blocks, seed=seed, starts=a.starts,
                              source="engine-enumerated orientable linear space, numerical realization, exact reconstruction")
        if cert:
            cert["blocks"] = blocks
            print("FOUND after %d spaces (%d duplicates) %.0fs" % (tried, dup, time.time() - t0), flush=True)
            print(json.dumps(cert), flush=True)
            print("added" if add_certificate(cert) else "already present", flush=True)
            sys.exit(0)
    if tried % 10 == 0:
        print("[%.0fs] %d non-isomorphic spaces tried, %d duplicates, none realized" % (time.time() - t0, tried, dup), flush=True)
print("DONE: %d non-isomorphic spaces, %d duplicates, none realized, %.0fs" % (tried, dup, time.time() - t0))
