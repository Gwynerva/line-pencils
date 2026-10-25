"""Extend certified arrangements by one line through as many existing intersection points as possible.

For an arrangement of n lines with f_0 points, a new line through the intersection points p_1..p_j (which must
be collinear on a line that is not one of the n) gives an arrangement of n+1 lines with
        f_0' = f_0 + n - sum_i mu(p_i)
points.  We enumerate all "rich" lines (through >= 2 intersection points, exact arithmetic in Z[sqrt d]),
record the attainable f_0' values with a verified certificate for each new value, and optionally all new types.

usage: python scripts/extend.py N [--values v1,v2,...] [--out FILE]
Reads data/certificates/n{N}.json, writes certificates of N+1 lines for the requested values (or for every
new f_0 value) to FILE (default data/certificates/extended_n{N+1}.json, a list of certificates).
"""
import argparse, itertools, json, os, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "verifier")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
from verify import verify, Reject, cross, dot, is_zero, vec_is_zero, pencils_of
from pencils import f0 as f0_of, fmt


def extend_one(cert, want=None):
    """yield (f0_new, certificate) for every rich line of the arrangement (and single-point / generic lines)"""
    n, d = cert["n"], cert["d"]
    L = [tuple((c[0], c[1]) for c in line) for line in cert["lines"]]
    pens = pencils_of(L, d)
    pts = []
    for S in pens:
        i, j = sorted(S)[:2]
        P = cross(L[i], L[j], d)
        pts.append((P, frozenset(S)))
    f0 = len(pts)
    seen = set()
    results = {}
    for a, b in itertools.combinations(range(len(pts)), 2):
        Pa, Sa = pts[a]; Pb, Sb = pts[b]
        if Sa & Sb:
            continue                           # the two points lie on a common arrangement line
        ell = cross(Pa, Pb, d)
        on = [k for k, (P, S) in enumerate(pts) if is_zero(dot(ell, P, d))]
        keyl = frozenset(on)
        if keyl in seen:
            continue
        seen.add(keyl)
        if any(is_zero(dot(ell, P, d)) and False for P, S in pts):
            pass
        # the new line must differ from all arrangement lines: it does, since it contains two points not on a common line
        sigma = sum(len(pts[k][1]) for k in on)
        v = f0 + n - sigma
        if want is not None and v not in want:
            continue
        if v in results:
            continue
        lines = cert["lines"] + [[[c[0], c[1]] for c in ell]]
        c2 = {"n": n + 1, "d": d, "lines": lines, "type": [], "source": "extension of an %d-line certificate by a line through %d intersection points" % (n, len(on))}
        try:
            verify(c2)
        except Reject as e:
            msg = str(e)
            if "type mismatch" not in msg:
                continue
            got = msg.split("recomputed ")[1]
            c2["type"] = json.loads(got)
            try:
                verify(c2)
            except Reject:
                continue
        assert f0_of(n + 1, tuple(c2["type"])) == v, (v, c2["type"])
        results[v] = c2
    return f0, results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("--values", default=None); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    n = a.n
    want = set(int(x) for x in a.values.split(",")) if a.values else None
    certs = json.load(open(os.path.join(ROOT, "data", "certificates", "n%d.json" % n)))
    found = {}
    for i, c in enumerate(certs):
        f0, res = extend_one(c, want)
        for v, c2 in res.items():
            if v not in found:
                found[v] = c2
                print("f0 = %d  from type %s + line; new type %s" % (v, fmt(tuple(c["type"])), fmt(tuple(c2["type"]))), flush=True)
        if want is not None and want <= set(found):
            break
    out = a.out or os.path.join(ROOT, "data", "certificates", "extended_n%d.json" % (n + 1))
    with open(out, "w") as f:
        json.dump([found[v] for v in sorted(found)], f, separators=(",", ":"))
    print("values attained for n = %d:" % (n + 1), sorted(found))
