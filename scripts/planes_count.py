"""Count types of plane arrangements under the candidate definitions.

For every n: b = types of some simple matroid of rank <= 4 on n elements (combinatorially possible),
c = types of some matroid with an integer realization found by planes_realize.py.  Matroids without a realization
are listed with their types; a type is counted in c only if certified, and the listed leftovers must be decided by
hand (notes/planes.md).

Writes runs/planes_certificates.json (one realization per realizable local type; check it with planes_verify.py)
and runs/planes_summary_n{N}.json.

Usage: python scripts/planes_count.py N
"""

import json
import sys

sys.path.insert(0, "scripts")
import planes_matroids as pm  # noqa: E402
import planes_types as pt  # noqa: E402


def main(N):
    levels = pm.load(f"runs/planes_matroids_n{N}.json")
    with open(f"runs/planes_real_n{N}.json") as fh:
        real = {int(k): v for k, v in json.load(fh).items()}
    summary = {}
    certs = {}
    for n in sorted(levels):
        defs = {"size": [set(), set()], "local": [set(), set()], "incidence": [set(), set()], "matroid": [set(), set()],
                "f0": [set(), set()], "f1": [set(), set()], "f01": [set(), set()]}
        ess = {d: [set(), set()] for d in ("size", "local", "matroid")}
        gc = pt.GraphClasses()
        unresolved = []
        for i, flats in enumerate(levels[n]):
            ok = real[n][i] is not None
            f0, f1 = pt.f_vector(n, flats)
            t = {"size": pt.size_type(n, flats), "local": pt.local_type(n, flats),
                 "incidence": gc.add(pt.incidence_graph(n, flats)), "matroid": i,
                 "f0": f0, "f1": f1, "f01": (f0, f1)}
            if ok and t["local"] not in defs["local"][1]:
                certs.setdefault(n, []).append({"type": {"lines": list(t["local"][0]),
                                                          "points": [[m, list(tau)] for m, tau in t["local"][1]]},
                                                 "planes": real[n][i]})
            for d, v in t.items():
                defs[d][0].add(v)
                if ok:
                    defs[d][1].add(v)
            if max(flats) == 4:
                for d in ess:
                    ess[d][0].add(t[d])
                    if ok:
                        ess[d][1].add(t[d])
            if not ok:
                unresolved.append((i, max(flats), pt.fmt_local(t["local"])))
        row = {d: (len(b), len(c)) for d, (b, c) in defs.items()}
        row["essential"] = {d: (len(b), len(c)) for d, (b, c) in ess.items()}
        summary[n] = row
        print(f"n={n}: " + ", ".join(f"{d} b={v[0]} c={v[1]}" for d, v in row.items() if d != "essential"))
        print("      essential (rank 4): " + ", ".join(f"{d} b={b} c={c}" for d, (b, c) in row["essential"].items()))
        for u in unresolved:
            print(f"      unresolved matroid #{u[0]} (rank {u[1]}): {u[2]}")
        for d in ("size", "local"):
            miss = defs[d][0] - defs[d][1]
            for m in sorted(miss):
                print(f"      {d}-type with no certificate: {pt.fmt_size(m) if d == 'size' else pt.fmt_local(m)}")
    with open("runs/planes_certificates.json", "w") as fh:
        json.dump(certs, fh, indent=0)
    with open(f"runs/planes_summary_n{N}.json", "w") as fh:
        json.dump(summary, fh, indent=1)
    return summary


if __name__ == "__main__":
    main(int(sys.argv[1]))
