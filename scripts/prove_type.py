"""Prove that a pencil type is not realizable by real lines, given the complete list of isomorphism classes
of its ORIENTABLE linear spaces (from scripts/dedupe_enum.py applied to a complete engine mode-5 enumeration).

For each class the algebraic prover (scripts/algebraic_nonrealizability.py) must return PROVED; then no linear
space of the type has a realization, i.e. the type is not realizable (non-orientable linear spaces cannot be
realized anyway).  The proof record is written to data/proofs/{type}.json and can be re-checked by re-running
the Groebner computations it lists.

usage: python scripts/prove_type.py N CLASSES.json OUT.json [--candidates K]
"""
import argparse, json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from algebraic_nonrealizability import prove
from pencils import fmt

ap = argparse.ArgumentParser()
ap.add_argument("n", type=int); ap.add_argument("classes"); ap.add_argument("out")
ap.add_argument("--candidates", type=int, default=8)
a = ap.parse_args()
cl = json.load(open(a.classes))
n = a.n
sizes = sorted((len(B) for B in cl["classes"][0]["blocks"]), reverse=True)
record = {"n": n, "type": sizes, "enumeration": cl["source"], "labelled_orientable_linear_spaces": cl["labelled_total"],
          "isomorphism_classes": len(cl["classes"]), "classes": []}
t0 = time.time()
all_ok = True
for i, c in enumerate(cl["classes"]):
    print("class %d/%d (%d labelled copies)" % (i + 1, len(cl["classes"]), c["labelled_count"]), flush=True)
    r = prove(n, c["blocks"], k=a.candidates, verbose=True)
    r["blocks"] = c["blocks"]; r["labelled_count"] = c["labelled_count"]
    record["classes"].append(r)
    all_ok &= (r["status"] == "PROVED")
    json.dump(record, open(a.out, "w"), indent=1)
record["verdict"] = "NOT REALIZABLE: every orientable linear space of this type is proved non-realizable" if all_ok else "UNDECIDED"
record["time"] = round(time.time() - t0, 1)
json.dump(record, open(a.out, "w"), indent=1)
print(fmt(sizes), record["verdict"], "(%.0fs)" % record["time"])
