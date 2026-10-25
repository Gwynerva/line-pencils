"""The band theorem for pencil types (notes/bands.md).

Let an arrangement of n lines have a largest pencil of exactly m = n - k lines, through P, and let A' be the
arrangement of the other k lines (none passes through P).  Removing the pencil shows that the type of the whole
arrangement is
        {m}  U  { mu'(p) + eps_p : p an intersection point of A' },      eps_p in {0, 1},
where mu' is the multiplicity in A' and eps_p = 1 iff a pencil line passes through p ("p is absorbed").
Conversely every realizable type T' of k lines and every set S of its points with |S| <= m is realized with
largest pencil m, provided m >= k + 1: put P in general position with respect to A', join P to the points of S,
add m - |S| generic lines through P.

Consequences used here:
  (a) UPPER BOUND, valid for every n: a type whose largest entry is m = n - k is realizable only if the rest of the
      type is in BAND(k) = { absorb(T', S) : T' realizable type of k lines, S subset of its points }.
  (b) CONSTRUCTION: if the rest of the type is absorb(T', S) with |S| <= m and m >= k + 1, an exact rational
      certificate is produced from a rational certificate of T' (lines of A' + pencil lines through a rational P).

usage: python scripts/bands.py N            # classify open types of n lines by (a), construct certificates by (b)
       python scripts/bands.py --table K    # print N(k) = |BAND(k)| for k <= K
"""
import itertools, json, os, random, sys
from collections import Counter
from fractions import Fraction as Fr
from math import comb
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "verifier"))
from pencils import t2, fmt, key
from verify import verify, Reject


def real_types(k):
    """realizable types of k lines with a certificate (as tuples); k <= 2: the empty type"""
    if k <= 2:
        return {(): None}
    fn = os.path.join(ROOT, "data", "certificates", "n%d.json" % k)
    out = {}
    for c in json.load(open(fn)):
        out[tuple(sorted(c["type"], reverse=True))] = c
    return out


def absorb_patterns(k, T):
    """all (result type, S-description) obtainable from T' = T by absorbing a sub-multiset of points.
    S is described by counts a_j of absorbed points of multiplicity j."""
    full = Counter(list(T) + [2] * t2(k, T))
    keys = sorted(full)
    for choice in itertools.product(*[range(full[j] + 1) for j in keys]):
        m = []
        for j, a in zip(keys, choice):
            m += [j + 1] * a + [j] * (full[j] - a)
        yield tuple(sorted((x for x in m if x >= 3), reverse=True)), dict(zip(keys, choice))


def band(k):
    """BAND(k): dict result-type -> (T', absorption counts) with the smallest |S|"""
    out = {}
    for T in real_types(k):
        for res, a in absorb_patterns(k, T):
            size = sum(a.values())
            if res not in out or size < out[res][2]:
                out[res] = (T, a, size)
    return out


# ------------------------------------------------------------------ exact construction (rational certificates)
def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def construct(n, k, T, counts, rng, tries=200):
    """certificate for {m} U absorb(T, S) with m = n - k, from a rational certificate of T (returns None if the
    certificate of T is not rational or the construction fails)."""
    m = n - k
    if k <= 2:
        lines = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0))][:k]
    else:
        c = real_types(k)[T]
        if c["d"] != 0:
            return None
        lines = [tuple(Fr(x[0]) for x in L) for L in c["lines"]]
    # intersection points of A' with multiplicities
    pts = {}
    for i, j in itertools.combinations(range(k), 2):
        X = cross(lines[i], lines[j])
        # normalise
        g = next(x for x in X if x != 0)
        X = tuple(x / g for x in X)
        pts.setdefault(X, set()).update((i, j))
    points = [(X, len(S)) for X, S in pts.items()]
    need = dict(counts)                     # multiplicity -> how many points of that multiplicity to absorb
    for _ in range(tries):
        P = (Fr(rng.randint(-60, 60)), Fr(rng.randint(-60, 60)), Fr(1))
        # choose S: for each multiplicity j, the first need[j] points (any choice works for the type)
        S = []
        ok = True
        for j, a in need.items():
            cand = [X for X, mu in points if mu == j]
            if len(cand) < a:
                ok = False; break
            S += cand[:a]
        if not ok:
            return None
        new = [cross(P, X) for X in S]
        while len(new) < m:
            R = (Fr(rng.randint(-60, 60)), Fr(rng.randint(-60, 60)), Fr(1))
            new.append(cross(P, R))
        allL = lines + new
        def clear(L):
            den = 1
            for x in L:
                den = den * x.denominator // __import__("math").gcd(den, x.denominator)
            v = [int(x * den) for x in L]
            g = 0
            for x in v:
                g = __import__("math").gcd(g, abs(x))
            return [[x // max(g, 1), 0] for x in v]
        cert = {"n": n, "type": sorted(list(T and absorb_result(k, T, counts) or absorb_result(k, T, counts)), reverse=True),
                "d": 0, "lines": [clear(L) for L in allL],
                "source": "band construction: pencil of %d lines through a generic point + %d-line arrangement of type %s, absorbing %s" % (m, k, fmt(T), counts)}
        cert["type"] = sorted([m] + list(absorb_result(k, T, counts)), reverse=True)
        try:
            verify(cert)
            return cert
        except Reject:
            continue
    return None


def absorb_result(k, T, counts):
    full = Counter(list(T) + [2] * t2(k, T))
    out = []
    for j in sorted(full):
        a = counts.get(j, 0)
        out += [j + 1] * a + [j] * (full[j] - a)
    return tuple(sorted((x for x in out if x >= 3), reverse=True))


if __name__ == "__main__":
    if sys.argv[1] == "--table":
        K = int(sys.argv[2])
        for k in range(0, K + 1):
            print("k = %2d: N(k) = %d  (stable for n >= %d)" % (k, len(band(k)), k + comb(k, 2)))
        sys.exit(0)
    n = int(sys.argv[1])
    rows = json.load(open(os.path.join(ROOT, "data", "results", "classification_n%d.json" % n)))
    rng = random.Random(1)
    excluded = {}; built = []
    fn = os.path.join(ROOT, "data", "certificates", "n%d.json" % n)
    certs = json.load(open(fn)) if os.path.exists(fn) else []
    have = {tuple(sorted(c["type"], reverse=True)) for c in certs}
    bands = {}
    for r in rows:
        if r["verdict"] != "open" or not r["type"]:
            continue
        T = tuple(r["type"]); m = T[0]; k = n - m
        if k not in bands:
            bands[k] = band(k)
        rest = tuple(T[1:])
        if rest not in bands[k]:
            excluded[key(T)] = {"kind": "theorem", "statement": "largest pencil has %d = n-%d lines; removing it leaves %d lines, and %s is not obtainable from any realizable type of %d lines by absorbing points (band theorem)" % (m, k, k, fmt(rest), k),
                                "reference": "notes/bands.md"}
        else:
            Tp, counts, size = bands[k][rest]
            if size <= m and m >= k + 1 and T not in have:
                c = construct(n, k, Tp, counts, rng)
                if c is not None:
                    certs.append(c); have.add(T); built.append(T)
    certs.sort(key=lambda c: (-sum(c["type"]), c["type"]))
    with open(fn, "w") as f:
        json.dump(certs, f, separators=(",", ":")); f.write("\n")
    ex = json.load(open(os.path.join(ROOT, "data", "exclusions.json")))
    ex.setdefault(str(n), {}).update(excluded)
    json.dump(ex, open(os.path.join(ROOT, "data", "exclusions.json"), "w"), indent=1)
    print("n=%d: %d open types excluded by the band theorem, %d new certificates constructed" % (n, len(excluded), len(built)))
    print("constructed:", [fmt(T) for T in built][:20])
