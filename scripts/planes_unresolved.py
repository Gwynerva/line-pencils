"""Decide the types that planes_types_next.py could not certify.

For each such type: reduce its labelled matroids up to isomorphism, then for each matroid look for an obstruction
that is preserved by real realizability:

  * a point whose planes form the Fano configuration (restriction to a rank-3 flat; Sylvester-Gallai),
  * a plane of the arrangement on which the others cut out the Fano configuration (contraction M/e: the
    simplification of M/e is the line arrangement cut out on the plane e),
  * seven planes forming the dual Fano matroid F7* (restriction; Proposition P of notes/planes.md),

and otherwise retry the constructive realization much harder.

usage: python scripts/planes_unresolved.py n
"""

import json
import sys
from itertools import combinations

sys.path.insert(0, "scripts")
import planes_matroids as pm  # noqa: E402
import planes_realize as pr  # noqa: E402

pc = pm.popcount


def restriction_fano(flats):
    """Rank-3 flat P (a point) whose rank-2 subflats form the Fano plane."""
    for P in flats.get(3, ()):
        if pc(P) != 7:
            continue
        blocks = [L for L in flats[2] if L & P == L]
        if len(blocks) == 7 and all(pc(b) == 3 for b in blocks):
            return f"the 7 planes {bits(P)} pass through one point and form the Fano configuration"
    return None


def contraction_fano(n, flats):
    r = max(flats)
    if r < 4:
        return None
    for e in range(n):
        b = 1 << e
        pts = [L for L in flats[2] if L & b]          # points of the section (lines in plane e)
        lines = [P for P in flats[3] if P & b]        # lines of the section (points in plane e)
        blocks = [[i for i, L in enumerate(pts) if L & P == L] for P in lines]
        if len(pts) == 7 and all(len(x) == 3 for x in blocks) and len(blocks) == 7:
            return f"the other planes cut plane {e} in a Fano configuration"
    return None


def restriction_dual_fano(n, flats):
    """Seven planes whose induced matroid is F7*: rank 4, no line on 3 of them, 7 points on 4 of them."""
    if max(flats) < 4:
        return None
    for S in combinations(range(n), 7):
        m = sum(1 << i for i in S)
        if any(pc(L & m) >= 3 for L in flats[2]):
            continue
        if any(pc(P & m) >= 5 for P in flats[3]):
            continue
        quads = [P & m for P in flats[3] if pc(P & m) == 4]
        if len(set(quads)) == 7:
            # rank 4 on S: S is not inside a point
            if not any(P & m == m for P in flats[3]):
                return f"the planes {list(S)} form the dual Fano configuration F7*"
    return None


def bits(x):
    return [i for i in range(x.bit_length()) if x >> i & 1]


def main(n):
    with open(f"runs/planes_types_n{n}.json") as fh:
        data = json.load(fh)
    report = []
    newcerts = []
    for entry in data["unresolved"]:
        ms = [{int(k): frozenset(v) for k, v in m.items()} for m in entry["matroids"]]
        cat = pm.Catalogue()
        for m in ms:
            cat.add(n, m)
        reps = [f for f, _ in cat.items]
        print(f"{entry['type']}: {len(ms)} labelled, {len(reps)} up to isomorphism")
        verdicts = []
        for k, f in enumerate(reps):
            why = restriction_fano(f) or contraction_fano(n, f) or restriction_dual_fano(n, f)
            if why is None:
                v = pr.realize(n, f, tries=3000, seed=11)
                if v is not None:
                    why = "REALIZED"
                    newcerts.append((entry["type"], v))
            print(f"   matroid {k}: {why or 'OPEN'}")
            verdicts.append(why)
        report.append({"type": entry["type"], "verdicts": verdicts})
    with open(f"runs/planes_unresolved_n{n}.json", "w") as fh:
        json.dump({"report": report, "new_certificates": newcerts}, fh, indent=1)


if __name__ == "__main__":
    main(int(sys.argv[1]))
