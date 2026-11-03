"""Checkable UNSAT verdicts: DIMACS CNF + LRAT proof (CaDiCaL), checked by cake_lpr (CakeML, formally verified).

A "NO" from a SAT solver is only as good as the solver.  For every UNSAT instance that a claim of the project rests
on, this module writes the CNF in DIMACS, runs the standalone CaDiCaL binary with `--lrat` (binary LRAT), and checks
the proof with `cake_lpr`, whose correctness (if it prints `s VERIFIED UNSAT`, the CNF is unsatisfiable) is proved
in HOL4 down to the machine code (Tan, Heule, Myreen, "Verified propagation redundancy and compositional UNSAT
checking in CakeML", 2023).  What remains trusted is (a) that the CNF encodes the mathematical statement -- the
encoders are short and documented in the scripts that call this module -- and (b) the case reductions around the
instances (stated where they are made).  The SAT solver is not trusted.

The instances behind the n = 12 claims are listed in data/proofs/lrat_n12.json (the manifest) by the SHA-256 of their
CNF, which is a deterministic function of the encoder (python-sat's cardinality encodings included, so the
python-sat version is pinned in the manifest and in CI).

usage:
  python scripts/sat_proof.py make  [MANIFEST] [--dir D] [--only NAME,..] [--workers W]
        build every instance, solve with CaDiCaL --lrat, check with cake_lpr, write the manifest
  python scripts/sat_proof.py check [MANIFEST] [--dir D] [--only NAME,..] [--workers W]
        rebuild every CNF, compare its hash with the manifest, re-solve and check the proof (used by CI)
  python scripts/sat_proof.py cnf NAME OUT.cnf      write one instance's CNF (for checking by other tools)
binaries: $CADICAL (default `cadical`) and $CAKE_LPR (default `cake_lpr`) on PATH.
"""
import argparse, hashlib, json, os, subprocess, sys, time
from itertools import combinations
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "proofs", "lrat_n12.json")
CADICAL = os.environ.get("CADICAL", "cadical")
CAKE_LPR = os.environ.get("CAKE_LPR", "cake_lpr")


def dimacs(clauses, comment=()):
    """DIMACS text (bytes) of a clause list; the variable count is the largest variable used."""
    nv = max((abs(l) for c in clauses for l in c), default=0)
    out = ["c %s" % line for line in comment]
    out.append("p cnf %d %d" % (nv, len(clauses)))
    out += [" ".join(map(str, c)) + " 0" for c in clauses]
    return ("\n".join(out) + "\n").encode()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def cnf_sha256(clauses):
    """hash of the clause part only (comments excluded), so the hash identifies the formula"""
    return sha256(dimacs(clauses))


def solve_and_check(clauses, stem, keep=True, timeout=None):
    """Write STEM.cnf, run CaDiCaL --lrat into STEM.lrat, check with cake_lpr.  Returns a dict with the verdict.
    status: UNSAT-VERIFIED (proof accepted), SAT, UNSAT-REJECTED, TIMEOUT or ERROR."""
    os.makedirs(os.path.dirname(os.path.abspath(stem)), exist_ok=True)
    data = dimacs(clauses)
    cnf, prf = stem + ".cnf", stem + ".lrat"
    with open(cnf, "wb") as f:
        f.write(data)
    nv = max((abs(l) for c in clauses for l in c), default=0)
    res = {"cnf_sha256": sha256(data), "vars": nv, "clauses": len(clauses)}
    t0 = time.time()
    try:
        p = subprocess.run([CADICAL, "-q", "--lrat=true", "--binary=true", cnf, prf],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        res.update(status="TIMEOUT", solve_time=round(time.time() - t0, 1))
        return res
    res["solve_time"] = round(time.time() - t0, 1)
    if p.returncode == 10:
        res["status"] = "SAT"
        return res
    if p.returncode != 20:
        res.update(status="ERROR", error=p.stderr.decode(errors="replace")[-500:])
        return res
    res["proof_bytes"] = os.path.getsize(prf)
    t0 = time.time()
    q = subprocess.run([CAKE_LPR, cnf, prf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res["check_time"] = round(time.time() - t0, 1)
    ok = q.returncode == 0 and q.stdout.decode().strip().splitlines()[-1:] == ["s VERIFIED UNSAT"]
    res["status"] = "UNSAT-VERIFIED" if ok else "UNSAT-REJECTED"
    if not ok:
        res["error"] = (q.stdout + q.stderr).decode(errors="replace")[-500:]
    if not keep:
        for fn in (cnf, prf):
            os.remove(fn)
    return res


# ----------------------------------------------------------------------------
# the n = 12 instances
# ----------------------------------------------------------------------------
def instances():
    """name -> (claim, description, builder spec).  The spec is JSON so that the manifest is self-contained."""
    out = {}
    # Proposition C3a: every point deletion of both STS(13).  Each system is rebuilt from its stored deletion of
    # point 0 (runs/orchard12.json): the uncovered pairs of the 12-point space plus the deleted point are its blocks.
    orchard = json.load(open(os.path.join(ROOT, "runs", "orchard12.json")))
    for c in orchard["classes"]:
        if c["deleted_point"] != 0:
            continue
        sts = [[p + 1 for p in B] for B in c["blocks"]]
        covered = {frozenset(q) for B in c["blocks"] for q in combinations(B, 2)}
        sts += [[0, a + 1, b + 1] for a, b in combinations(range(12), 2) if frozenset((a, b)) not in covered]
        assert len(sts) == 26 and len({frozenset(q) for B in sts for q in combinations(B, 2)}) == 78
        for oo in range(13):
            relabel = {p: i for i, p in enumerate(q for q in range(13) if q != oo)}
            L = sorted(sorted(relabel[p] for p in B) for B in sts if oo not in B)
            name = "C3a_sts13p%d_del%d" % (c["sts13_pasch"], oo)
            out[name] = {"claim": "Proposition C3a", "kind": "orient_fixed", "n": 12, "blocks": L,
                         "what": "the linear space (STS(13) with %d Pasch configurations, point %d deleted) has no "
                                 "chirotope" % (c["sts13_pasch"], oo)}
    out["C3a_type"] = {"claim": "Proposition C3a", "kind": "orient_type", "n": 12, "type": [3] * 20,
                       "what": "no orientable linear space of type {3^20} (whole type, no case split)"}
    from orient_split import cases
    for i, b in enumerate(cases()):
        out["C3b_case%d" % (i + 1)] = {"claim": "Proposition C3b", "kind": "orient_split", "n": 12, "blocks4": b, "n3": 9,
                                      "what": "no orientable linear space of type {4^5, 3^9} with these five 4-blocks"}
    orient = json.load(open(os.path.join(ROOT, "runs", "orient_12.json")))
    for k, v in sorted(orient.items()):
        if v["status"] == "NO":
            s = [int(x) for x in k.split(",")]
            out["orient_" + k.replace(",", "-")] = {"claim": "c(12): non-orientable types", "kind": "orient_type", "n": 12,
                                                    "type": s, "what": "no orientable linear space of type {%s}" % k}
    return out


def build_clauses(spec):
    from sat_orient import build
    if spec["kind"] == "orient_fixed":
        cl, _, _ = build(spec["n"], [len(B) for B in spec["blocks"]], fixed_blocks=spec["blocks"])
    elif spec["kind"] == "orient_type":
        cl, _, _ = build(spec["n"], tuple(spec["type"]))
    elif spec["kind"] == "orient_split":
        from orient_split import split_clauses
        cl = split_clauses(spec["blocks4"], spec["n3"])
    elif spec["kind"] == "linear_space":
        from sat_linear_space import clauses
        cl = clauses(spec["n"], tuple(spec["type"]))
    else:
        raise ValueError(spec["kind"])
    return cl


def _job(args):
    name, spec, d, timeout = args
    cl = build_clauses(spec)
    r = solve_and_check(cl, os.path.join(d, name), keep=True, timeout=timeout)
    return name, r


def pysat_version():
    import pysat
    return pysat.__version__


TOOLS = {"cadical": "CaDiCaL 2.1.3 (git tag rel-2.1.3), standalone binary, options -q --lrat=true --binary=true",
         "cake_lpr": "github.com/tanyongkiam/cake_lpr commit 033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2 (x64 cake_lpr.S, "
                     "sha256 checked against cake_lpr.sha256)"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "check", "cnf"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--dir", default=os.path.join(ROOT, "runs", "proofs"), help="where CNF and LRAT files are written")
    ap.add_argument("--only", default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=None, help="per-instance solver time limit (s)")
    a = ap.parse_args()
    if a.cmd == "cnf":
        name, out = a.args
        spec = instances()[name]
        with open(out, "wb") as f:
            f.write(dimacs(build_clauses(spec), comment=[spec["what"]]))
        sys.exit(0)
    man_path = a.args[0] if a.args else MANIFEST
    if a.cmd == "make":
        allspecs = instances()
        man = json.load(open(man_path)) if os.path.exists(man_path) else {"instances": {}}
        names = a.only.split(",") if a.only else list(allspecs)
        specs = {k: allspecs[k] for k in names}
    else:
        man = json.load(open(man_path))
        names = a.only.split(",") if a.only else sorted(man["instances"])
        specs = {k: man["instances"][k]["spec"] for k in names}
        if man.get("python_sat") != pysat_version():
            print("WARNING: manifest built with python-sat %s, running %s (CNF hashes may differ)"
                  % (man.get("python_sat"), pysat_version()), flush=True)
    t0 = time.time(); bad = 0; ok = 0
    jobs = [(k, specs[k], a.dir, a.timeout) for k in names]
    with Pool(a.workers) as P:
        for name, r in P.imap_unordered(_job, jobs):
            print("[%5.0fs] %-40s %-15s solve %6ss  proof %s B  check %ss" % (
                time.time() - t0, name, r["status"], r.get("solve_time"), r.get("proof_bytes"), r.get("check_time")),
                flush=True)
            if a.cmd == "make":
                if r["status"] == "UNSAT-VERIFIED":      # only checked verdicts enter the manifest
                    man["instances"][name] = dict(r, spec=specs[name], claim=specs[name]["claim"])
                    man["python_sat"] = pysat_version(); man["tools"] = TOOLS
                    with open(man_path, "w", newline="\n") as f:
                        json.dump(man, f, indent=1, sort_keys=True); f.write("\n")
                else:
                    bad += 1
            else:
                want = man["instances"][name]["cnf_sha256"]
                if r["cnf_sha256"] != want:
                    print("  CNF HASH MISMATCH: %s, manifest %s" % (r["cnf_sha256"], want)); bad += 1
                elif r["status"] != "UNSAT-VERIFIED":
                    print("  NOT VERIFIED:", r.get("error", r["status"])); bad += 1
                else:
                    ok += 1
                for ext in (".cnf", ".lrat"):
                    fn = os.path.join(a.dir, name + ext)
                    if os.path.exists(fn):
                        os.remove(fn)
    print("done in %.0fs: %d verified, %d problems" % (time.time() - t0, ok, bad) if a.cmd == "check"
          else "done in %.0fs, %d not verified" % (time.time() - t0, bad))
    sys.exit(1 if bad else 0)
