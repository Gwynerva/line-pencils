"""Sub-arrangements of sections of the 4-dimensional mirror arrangements (A4, D4, B4, F4, H4).

The reflection hyperplanes of a root system in R^4 cut a 3-dimensional subspace W in planes through 0, that is,
in lines of P(W) = RP^2: with an orthonormal basis B of W the line of the mirror with normal r is B^T r.  Mirrors
that contain W are dropped, mirrors that give the same line are merged.  Sections used: W = u^perp for u a root
(the restriction of the arrangement to a mirror; for H4 this is an arrangement of 31 lines) or a 1-dimensional
flat (a direction contained in several mirrors), and with --wide also sums and differences of two such vectors:
symmetric directions give sections with many more coincidences than random ones.  The restriction of H4 to a
mirror is the arrangement of the 31 planes perpendicular to the symmetry axes of the icosahedron (15 + 10 + 6).

For a target type T on n lines, subsets of n lines of a section are grown from its rich points: for each pencil
size k of T (largest first) a point of the section with at least k lines is chosen and k of its lines are added.
A subset of exactly type T is turned into an exact certificate by scripts/targeted.py (realize.py's
snap_to_rationals and exactify, which recognises a + b sqrt(d)), kept only if verifier/verify.py accepts it.

Found this way: {4^9} for 13 lines, 13 of the 31 planes perpendicular to the symmetry axes of the icosahedron
(over Q(sqrt 5)); for 12 lines the same type is impossible (Proposition C3).  Reproduce with
    python scripts/mirror_sections.py 13 "4,4,4,4,4,4,4,4,4" --seed 1 --tries 60000      (about 20 s)

usage: python scripts/mirror_sections.py N "k1,k2,..;.." [--system H4] [--tries 3000] [--seed 3] [--wide] [--add]
       python scripts/mirror_sections.py N open [...]       (every type that is open in data/results)
"""
import argparse, itertools, json, os, random, sys, time
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from pencils import unkey, fmt

PHI = (1 + 5 ** 0.5) / 2


def _even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0:
            out.append(tuple(v[p[i]] for i in range(4)))
    return out


def roots(system):
    """unit normals of the mirrors (one per mirror)"""
    E = np.eye(4)
    D4 = [E[i] + s * E[j] for i, j in itertools.combinations(range(4), 2) for s in (1, -1)]
    halves = [np.array(s) / 2 for s in itertools.product((1, -1), repeat=4)]
    if system == "A4":
        Q = np.linalg.qr(np.vstack([np.ones(5), np.eye(5)[:4]]).T)[0][:, 1:5]
        R = [Q.T @ (np.eye(5)[i] - np.eye(5)[j]) for i, j in itertools.combinations(range(5), 2)]
    elif system == "D4":
        R = D4
    elif system == "B4":
        R = list(E) + D4
    elif system == "F4":
        R = list(E) + D4 + halves
    elif system == "H4":
        R = list(E) + halves
        for s in itertools.product((1, -1), repeat=3):
            R += [np.array(p) / 2 for p in _even_perms((s[0] * PHI, s[1] * 1.0, s[2] / PHI, 0.0))]
    out = []
    for v in R:
        v = np.array(v, float) / np.linalg.norm(v)
        if all(abs(abs(np.dot(v, w)) - 1) > 1e-9 for w in out):
            out.append(v)
    return out


def flats(R, rng, k=60):
    """directions contained in at least 4 mirrors"""
    out = []
    for _ in range(4000):
        A = np.array(rng.sample(R, 3))
        if np.linalg.matrix_rank(A, 1e-9) < 3:
            continue
        v = np.linalg.svd(A)[2][-1]
        if sum(1 for r in R if abs(np.dot(r, v)) < 1e-9) >= 4 and all(abs(abs(np.dot(v, w)) - 1) > 1e-9 for w in out):
            out.append(v)
            if len(out) >= k:
                break
    return out


def section(R, u):
    """lines of RP^2 cut by the mirrors on W = u^perp"""
    B = np.linalg.svd((u / np.linalg.norm(u)).reshape(1, 4))[2][1:].T
    L = []
    for r in R:
        l = B.T @ r
        if np.linalg.norm(l) < 1e-9:
            continue
        l = l / np.linalg.norm(l)
        if all(np.linalg.norm(np.cross(l, m)) > 1e-9 for m in L):
            L.append(l)
    return L


def rich_points(L):
    pts = set()
    for a, b in itertools.combinations(range(len(L)), 2):
        c = np.cross(L[a], L[b]); c /= np.linalg.norm(c)
        pts.add(frozenset(k for k in range(len(L)) if abs(np.dot(L[k], c)) < 1e-9))
    return [p for p in pts if len(p) >= 3]


def search(L, P, T, n, tries, rng):
    from targeted import pencils, type_of
    for it in range(tries):
        S = set()
        if it % 2:                 # walk through the rich points in random order, taking k lines where they fit
            for p in rng.sample(P, len(P)):
                ks = [k for k in set(T) if k <= len(p)]
                if ks:
                    q = set(rng.sample(sorted(p), rng.choice(ks)))
                    if len(S | q) <= n:
                        S |= q
                if len(S) == n:
                    break
        for k in (T if not it % 2 else ()):
            big = [p for p in P if len(p) >= k]
            if not big:
                break
            p = rng.choice(big)
            S |= set(rng.sample(sorted(p), k))
            if len(S) >= n:
                break
        while len(S) < n:
            S.add(rng.randrange(len(L)))
        if len(S) != n:
            continue
        sub = np.array([L[i] for i in sorted(S)])
        p = pencils(sub)
        if p is not None and type_of(p) == T:
            return sub
    return None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("types")
    ap.add_argument("--system", default="H4"); ap.add_argument("--tries", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=3); ap.add_argument("--add", action="store_true")
    ap.add_argument("--wide", action="store_true", help="also sections by sums and differences of two roots / flats (slow)")
    a = ap.parse_args()
    N = a.n
    if a.types == "open":
        cls = json.load(open(os.path.join(ROOT, "data", "results", "classification_n%d.json" % N)))
        targets = [tuple(r["type"]) for r in cls if r["verdict"] == "open"]
    else:
        targets = [tuple(sorted(unkey(s), reverse=True)) for s in a.types.split(";")]
    from targeted import certificate
    rng = random.Random(a.seed)
    R = roots(a.system)
    sections_ = [("mirror %d" % i, r) for i, r in enumerate(R)] + [("flat %d" % i, f) for i, f in enumerate(flats(R, rng))]
    # symmetric ("beautiful") directions: sums and differences of two roots, and of a root and a flat
    if a.wide:
        F = flats(R, random.Random(a.seed + 1))
        sections_ += [("r%d+r%d" % (i, j), R[i] + s * R[j]) for i, j in itertools.combinations(range(len(R)), 2) for s in (1, -1)]
        sections_ += [("r%d+f%d" % (i, j), R[i] + s * F[j]) for i in range(len(R)) for j in range(len(F)) for s in (1, -1)]
    seen = set(); pools = []
    for label, u in sections_:
        if np.linalg.norm(u) < 1e-9:
            continue
        L = section(R, u)
        if len(L) < N:
            continue
        P = rich_points(L)
        sig = (len(L), tuple(sorted(len(p) for p in P)))
        if sig not in seen:
            seen.add(sig); pools.append((label, L, P))
    print("%s: %d mirrors, %d distinct sections with >= %d lines" % (a.system, len(R), len(pools), N), flush=True)
    t0 = time.time()
    for T in targets:
        for label, L, P in pools:
            sub = search(L, P, T, N, a.tries, rng)
            if sub is None:
                continue
            cert = certificate(sub, T)
            print("[%.0fs] %s: %s, %d of its %d lines -> %s" % (time.time() - t0, fmt(T), label, N, len(L),
                  "certificate over Q(sqrt %d)" % cert["d"] if cert and cert["d"] else "rational certificate" if cert else "no exact certificate"), flush=True)
            if cert:
                cert["source"] = "subarrangement of a section of the %s mirror arrangement (scripts/mirror_sections.py) + exact reconstruction" % a.system
                if a.add:
                    from find_examples import add_certificate
                    print("   ", "added" if add_certificate(cert) else "already present")
                break
        else:
            print("[%.0fs] %s: not found" % (time.time() - t0, fmt(T)), flush=True)
