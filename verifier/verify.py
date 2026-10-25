#!/usr/bin/env python3
"""Exact verifier for realizability certificates of pencil types.

A certificate claims: "these n lines in the real projective plane form an
arrangement of pencil type T".  This program recomputes the type from the
coordinates with exact arithmetic and compares.  Nothing else is trusted.

CERTIFICATE FORMAT (JSON)
-------------------------
{
  "n": 10,
  "type": [5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],      # pencil sizes >= 3 (any order)
  "d": 5,                                          # coordinates live in Q(sqrt d); d = 0 means Q
  "lines": [ [[a0,a1],[b0,b1],[c0,c1]], ... ],     # n lines, each  a x + b y + c z = 0,
                                                   # every coefficient p = [p0,p1] means p0 + p1*sqrt(d)
  "source": "free text: how the example was found"  # optional, ignored
}
Integers are arbitrary-precision; a certificate over Q uses d = 0 and p1 = 0.

ARITHMETIC
----------
Elements of Q(sqrt d) are pairs of Python integers (p0, p1) = p0 + p1*sqrt(d).
We only add, subtract and multiply, so denominators never appear (coordinates
are projective, hence may be scaled to integers).  The single fact we rely on:

    if d is a positive integer that is not a perfect square, then
    p0 + p1*sqrt(d) = 0  with integers p0, p1  implies  p0 = p1 = 0.

(Proof: otherwise sqrt(d) = -p0/p1 would be rational, contradicting that d is
not a square.)  Hence the test "is this expression zero?" is decided exactly by
comparing the two integer components with zero.  For d = 0 we require p1 = 0
everywhere and the elements are plain integers.

WHAT IS CHECKED
---------------
1.  d is 0 or a non-square positive integer; every coefficient is an integer pair.
2.  Every line is a non-zero vector (otherwise it is not a line).
3.  All n lines are pairwise distinct as projective lines, i.e. no two coefficient
    vectors are proportional.  Two vectors u, v are proportional iff their cross
    product u x v vanishes, and the cross product is computed exactly.
4.  For every pair of lines i < j, the intersection point P = L_i x L_j is
    computed exactly, and the pencil through P is the set of ALL lines L_k with
    L_k . P = 0.  (This is the maximal set of lines through P; it is never built by
    merging pairs.)  Two pairs lying in the same pencil produce the same set, so the
    distinct sets are exactly the intersection points of the arrangement, and the
    size of each set is the number of lines through that point.
5.  Sanity: the sizes s of the distinct pencils satisfy sum C(s,2) = C(n,2), i.e.
    every pair of lines is counted in exactly one pencil.
6.  The multiset of pencil sizes >= 3 equals the claimed type.

Everything is done in the projective plane.  An affine picture with no two
lines parallel is obtained by choosing as line at infinity any line that misses
all the (finitely many) intersection points.

USAGE
-----
    python verifier/verify.py FILE.json [FILE2.json ...]     # each file: a list of certificates
    python verifier/verify.py --self-test                     # built-in tests (see test_verify.py)
Exit status 0 iff every certificate verifies and all self-tests pass.
"""
import json
import sys
from math import comb, isqrt
from collections import Counter


# ----------------------------------------------------------------------------
# arithmetic in Z[sqrt d]   (elements: tuples (p0, p1))
# ----------------------------------------------------------------------------
def is_field_ok(d):
    """d = 0 (rationals) or a positive integer that is not a perfect square."""
    return isinstance(d, int) and not isinstance(d, bool) and (d == 0 or (d > 1 and isqrt(d) ** 2 != d))


def mul(x, y, d):
    return (x[0] * y[0] + d * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def is_zero(x):
    return x[0] == 0 and x[1] == 0


def cross(u, v, d):
    """u x v for 3-vectors over Z[sqrt d]."""
    return (sub(mul(u[1], v[2], d), mul(u[2], v[1], d)),
            sub(mul(u[2], v[0], d), mul(u[0], v[2], d)),
            sub(mul(u[0], v[1], d), mul(u[1], v[0], d)))


def dot(u, v, d):
    return add(add(mul(u[0], v[0], d), mul(u[1], v[1], d)), mul(u[2], v[2], d))


def vec_is_zero(u):
    return all(is_zero(c) for c in u)


# ----------------------------------------------------------------------------
# the verifier
# ----------------------------------------------------------------------------
class Reject(Exception):
    pass


def parse_element(p, d):
    ok = isinstance(p, list) and len(p) == 2 and all(isinstance(c, int) and not isinstance(c, bool) for c in p)
    if not ok:
        raise Reject("coefficient is not a pair of integers: %r" % (p,))
    if d == 0 and p[1] != 0:
        raise Reject("d = 0 but a coefficient has a non-zero sqrt part: %r" % (p,))
    return (p[0], p[1])


def pencils_of(lines, d):
    """All pencils (maximal concurrent sets of lines) as a set of frozensets of indices.

    lines: list of 3-vectors over Z[sqrt d], non-zero and pairwise non-proportional.
    """
    n = len(lines)
    pencils = set()
    for i in range(n):
        for j in range(i + 1, n):
            P = cross(lines[i], lines[j], d)            # the intersection point, exact
            # all lines through P (a maximal concurrent set, computed from scratch)
            S = frozenset(k for k in range(n) if is_zero(dot(lines[k], P, d)))
            assert i in S and j in S                     # L_i . (L_i x L_j) = 0 identically
            pencils.add(S)
    return pencils


def verify(cert):
    """Return the recomputed type (sizes >= 3, non-increasing) or raise Reject."""
    try:
        n = cert["n"]; d = cert["d"]; claimed = cert["type"]; raw = cert["lines"]
    except (KeyError, TypeError) as e:
        raise Reject("missing field %s" % e)
    if not is_field_ok(d):
        raise Reject("d = %r is not 0 or a non-square positive integer" % (d,))
    if not (isinstance(n, int) and n >= 1 and isinstance(raw, list) and len(raw) == n):
        raise Reject("n = %r but %s lines given" % (n, len(raw) if isinstance(raw, list) else "?"))
    lines = []
    for L in raw:
        if not (isinstance(L, list) and len(L) == 3):
            raise Reject("a line must have 3 coefficients: %r" % (L,))
        v = tuple(parse_element(c, d) for c in L)
        if vec_is_zero(v):
            raise Reject("zero vector is not a line")
        lines.append(v)
    for i in range(n):
        for j in range(i + 1, n):
            if vec_is_zero(cross(lines[i], lines[j], d)):
                raise Reject("lines %d and %d coincide" % (i, j))
    sizes = sorted((len(S) for S in pencils_of(lines, d)), reverse=True)
    if sum(comb(s, 2) for s in sizes) != comb(n, 2):
        raise Reject("internal: pairs not partitioned by pencils")   # cannot happen; kept as a guard
    got = [s for s in sizes if s >= 3]
    if not (isinstance(claimed, list) and all(isinstance(k, int) for k in claimed)):
        raise Reject("type must be a list of integers")
    if Counter(got) != Counter(claimed):
        raise Reject("type mismatch: claimed %s, recomputed %s" % (sorted(claimed, reverse=True), got))
    return got


# ----------------------------------------------------------------------------
# command line
# ----------------------------------------------------------------------------
def main(argv):
    if argv and argv[0] == "--self-test":
        import unittest, os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import test_verify
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_verify)
        r = unittest.TextTestRunner(verbosity=1).run(suite)
        return 0 if r.wasSuccessful() else 1
    if not argv:
        print(__doc__); return 2
    total = bad = 0
    per_n = Counter(); seen = {}
    for fn in argv:
        certs = json.load(open(fn))
        if isinstance(certs, dict):
            certs = [certs]
        for idx, c in enumerate(certs):
            total += 1
            try:
                got = verify(c)
            except Reject as e:
                bad += 1
                print("REJECT %s[%d] n=%s type=%s: %s" % (fn, idx, c.get("n"), c.get("type"), e))
                continue
            k = (c["n"], tuple(got))
            if k in seen:
                print("NOTE duplicate certificate for n=%d type %s (%s and %s[%d])" % (k[0], list(k[1]), seen[k], fn, idx))
            seen[k] = "%s[%d]" % (fn, idx)
            per_n[c["n"]] += 1
    print("verified %d certificates, %d rejected" % (total, bad))
    print("distinct realizable types per n:", {n: len({t for (m, t) in seen if m == n}) for n in sorted(per_n)})
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
