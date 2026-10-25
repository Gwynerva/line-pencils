"""Classify every arithmetically admissible pencil type for n lines and compute the four sequences.

For each type T (pencil sizes >= 3) the verdict is one of
  real              a certificate in data/certificates/n{n}.json verifies (field Q or Q(sqrt d))
  no-linear-space   no linear space with these blocks exists (engine mode 0 "NO", runs/comb_{n}.json;
                    cross-checked by SAT in runs/sat_{n}.json when present)
  melchior          a linear space exists but Melchior's inequality t2 >= 3 + sum (k-3) t_k fails
  csima-sawyer      ... Csima-Sawyer t2 >= 6n/13 (n >= 8) fails
  debruijn-erdos    ... f0 < n (de Bruijn-Erdos) -- never the only reason in practice
  non-orientable    a linear space exists, theorems do not exclude it, but no linear space of this type
                    admits a chirotope (runs/sat_orient_{n}.json or runs/orient_{n}.json say NO)
  theorem           excluded by a theorem proved in notes/ (recorded in data/exclusions.json, kind "theorem")
  non-realizable-proved  orientable, but every orientable linear space of the type carries an exact algebraic
                    certificate of non-realizability (data/proofs/*.json, verdict "NOT REALIZABLE")
  literature        excluded by a published theorem not re-proved here (data/exclusions.json, kind "literature")
  open              none of the above
Sequences:
  a(n) = |A_n|  (arithmetic),  b(n) = #{T : a linear space exists},
  c(n) = #{real}  (exact only if no 'open'),  d(n) = #{f0(T) : T real} (exact only if no 'open').
Writes data/results/classification_n{n}.json and prints a summary.

usage: python scripts/classify.py NMAX
"""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pencils import candidates, key, unkey, fmt, f0, t2, melchior_ok, csima_sawyer_ok, debruijn_erdos_ok
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "verifier"))
from verify import verify, Reject


def load(path):
    p = os.path.join(ROOT, path)
    return json.load(open(p)) if os.path.exists(p) else {}


def classify(n):
    certs = load("data/certificates/n%d.json" % n) or []
    real = {}
    for c in certs:
        verify(c)                                   # raises if a certificate is bad
        real[tuple(sorted(c["type"], reverse=True))] = c
    comb = load("runs/comb_%d.json" % n)
    sat = load("runs/sat_%d.json" % n)
    orient = {}
    for src in ("runs/orient_%d.json" % n, "runs/sat_orient_%d.json" % n):
        for k, v in load(src).items():
            if v.get("status") in ("YES", "NO"):
                prev = orient.get(k)
                assert prev is None or prev == v["status"], ("orientability disagreement", n, k)
                orient[k] = v["status"]
    excl = load("data/exclusions.json").get(str(n), {})
    proofs = {}
    import glob
    for pf in glob.glob(os.path.join(ROOT, "data", "proofs", "n%d_*.json" % n)):
        pr = json.load(open(pf))
        if pr.get("verdict", "").startswith("NOT REALIZABLE"):
            proofs[key(tuple(sorted(pr["type"], reverse=True)))] = os.path.relpath(pf, ROOT).replace(os.sep, "/")
    rows = []
    for T in candidates(n):
        k = key(T)
        row = {"type": list(T), "f0": f0(n, T), "t2": t2(n, T)}
        c = comb.get(k, {}).get("status"); s = sat.get(k, {}).get("status")
        if c in ("YES", "NO") and s in ("YES", "NO"):
            assert c == s, ("comb/SAT disagreement", n, k)
        comb_status = c if c in ("YES", "NO") else s
        row["linear_space"] = comb_status
        if T in real:
            row["verdict"] = "real"; row["field_d"] = real[T]["d"]
            assert comb_status != "NO", ("certificate for a type without linear space?!", n, k)
        elif comb_status == "NO":
            row["verdict"] = "no-linear-space"
        elif n <= 2:
            row["verdict"] = "real"
        elif not melchior_ok(n, T):
            row["verdict"] = "melchior"
        elif not csima_sawyer_ok(n, T):
            row["verdict"] = "csima-sawyer"
        elif not debruijn_erdos_ok(n, T):
            row["verdict"] = "debruijn-erdos"
        elif orient.get(k) == "NO":
            row["verdict"] = "non-orientable"
        elif k in excl:
            row["verdict"] = excl[k]["kind"]; row["reference"] = excl[k]["reference"]; row["statement"] = excl[k]["statement"]
        elif k in proofs:
            row["verdict"] = "non-realizable-proved"; row["reference"] = proofs[k]
            row["statement"] = "every orientable linear space of this type has an exact Groebner-basis certificate that any realization carries an extra collinearity"
        else:
            row["verdict"] = "open"
            if orient.get(k) == "YES":
                row["orientable"] = True
        if comb_status is None and row["verdict"] not in ("real",):
            row["note"] = "linear-space status not computed"
        rows.append(row)
    return rows


def summary(n, rows):
    cnt = Counter(r["verdict"] for r in rows)
    a = len(rows)
    comb_yes = sum(1 for r in rows if r["linear_space"] == "YES" or (r["linear_space"] is None and r["verdict"] == "real"))
    comb_unknown = sum(1 for r in rows if r["linear_space"] is None and r["verdict"] != "real")
    c = cnt["real"]; op = cnt["open"]
    vals = sorted({r["f0"] for r in rows if r["verdict"] == "real"})
    d = len(vals)
    open_vals = sorted({r["f0"] for r in rows if r["verdict"] == "open"} - set(vals))
    return {"n": n, "a": a, "b": comb_yes if comb_unknown == 0 else [comb_yes, comb_yes + comb_unknown],
            "c": c if op == 0 else [c, c + op], "d": d if not open_vals else [d, d + len(open_vals)],
            "verdicts": dict(cnt), "f0_values": vals, "f0_undecided": open_vals}


if __name__ == "__main__":
    nmax = int(sys.argv[1])
    os.makedirs(os.path.join(ROOT, "data", "results"), exist_ok=True)
    seqs = {"a": [], "b": [], "c": [], "d": []}
    for n in range(1, nmax + 1):
        rows = classify(n)
        with open(os.path.join(ROOT, "data", "results", "classification_n%d.json" % n), "w") as f:
            json.dump(rows, f, indent=0); f.write("\n")
        s = summary(n, rows)
        for q in "abcd":
            seqs[q].append(s[q])
        print(n, {q: s[q] for q in "abcd"}, s["verdicts"], ("undecided f0: %s" % s["f0_undecided"]) if s["f0_undecided"] else "")
        if n == 1:   # one line: no intersection points; the empty type
            pass
    print("a:", seqs["a"]); print("b:", seqs["b"]); print("c:", seqs["c"]); print("d:", seqs["d"])
    with open(os.path.join(ROOT, "data", "results", "sequences.json"), "w") as f:
        json.dump(seqs, f, indent=1)
