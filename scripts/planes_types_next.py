"""Types of n planes without an isomorphism catalogue at level n.

Every simple matroid of rank <= 4 on n elements is a single-element extension of one on n - 1 elements (all of
which are in runs/planes_matroids_n{n-1}.json).  This script generates all these extensions as labelled matroids,
groups them by local type and, for each type, tries to realize its members until one succeeds.  Types without a
realization are reported with all their (labelled) matroids, which are then reduced up to isomorphism.

usage: python scripts/planes_types_next.py n     (writes runs/planes_types_n{n}.json, adds to the certificates)
"""

import json
import random
import sys

sys.path.insert(0, "scripts")
import planes_matroids as pm  # noqa: E402
import planes_realize as pr  # noqa: E402
import planes_types as pt  # noqa: E402


def main(n):
    prev = pm.load(f"runs/planes_matroids_n{n - 1}.json")[n - 1]
    groups = {}
    count = 0
    for flats in prev:
        cands = []
        if max(flats) < 4:
            cands.append(pm.coloop_extension(n - 1, flats))
        for L in pm.linear_subclasses(n - 1, flats):
            cands.append(pm.extension(n - 1, flats, L))
        for c in cands:
            count += 1
            groups.setdefault(pt.local_type(n, c), []).append(c)
    print(f"n={n}: {count} labelled extensions, {len(groups)} local types (b)", flush=True)
    rng = random.Random(7)
    certs, unresolved = {}, {}
    sizes_b, sizes_c, f0_b, f0_c, f01_b, f01_c = set(), set(), set(), set(), set(), set()
    ess_b, ess_c = set(), set()
    inc_b, inc_c = pt.GraphClasses(), set()
    for t, ms in groups.items():
        rep = ms[0]
        assert pm.is_matroid(n, rep)
        s = pt.size_type(n, rep)
        f = pt.f_vector(n, rep)
        sizes_b.add(s)
        f0_b.add(f[0])
        f01_b.add(f)
        if max(rep) == 4:
            ess_b.add(t)
        incs = {inc_b.add(pt.incidence_graph(n, m)) for m in ms}
        order = list(range(len(ms)))
        rng.shuffle(order)
        found = None
        for j in order[:40]:
            v = pr.realize(n, ms[j], tries=60, seed=j)
            if v is not None:
                found = (j, v)
                break
        if found is None:
            unresolved[t] = ms
            continue
        j, v = found
        certs[t] = v
        sizes_c.add(s)
        f0_c.add(f[0])
        f01_c.add(f)
        inc_c.add(inc_b.add(pt.incidence_graph(n, ms[j])))
        if max(rep) == 4:
            ess_c.add(t)
    print(f"  local: b={len(groups)} c(certified)={len(certs)}; essential b={len(ess_b)} c={len(ess_c)}")
    print(f"  size:  b={len(sizes_b)} c>={len(sizes_c)};  f0 values b={len(f0_b)} c>={len(f0_c)};"
          f"  (f0,f1) b={len(f01_b)} c>={len(f01_c)}")
    print(f"  incidence classes b={sum(len(v) for v in inc_b.reps.values())} c>={len(inc_c)}")
    print(f"  f0 values: {sorted(f0_b)}")
    for t, ms in unresolved.items():
        print(f"  UNRESOLVED {pt.fmt_local(t)}: {len(ms)} labelled matroids, ranks {sorted({max(m) for m in ms})}")
    with open("runs/planes_certificates.json") as fh:
        allc = json.load(fh)
    allc[str(n)] = [{"type": {"lines": list(t[0]), "points": [[m, list(tau)] for m, tau in t[1]]}, "planes": v}
                    for t, v in certs.items()]
    with open("runs/planes_certificates.json", "w") as fh:
        json.dump(allc, fh, indent=0)
    out = {"unresolved": [{"type": pt.fmt_local(t), "matroids": [{str(k): sorted(s) for k, s in m.items()} for m in ms]}
                          for t, ms in unresolved.items()],
           "f0_values": sorted(f0_b)}
    with open(f"runs/planes_types_n{n}.json", "w") as fh:
        json.dump(out, fh)


if __name__ == "__main__":
    main(int(sys.argv[1]))
