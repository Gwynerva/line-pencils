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
# non-realizability certificates (Rabinowitsch cofactors), data/proofs/n*.json
# ----------------------------------------------------------------------------
# A class of such a file is a linear space (blocks on the points 0..n-1), a projective frame f0..f3, a list of
# non-collinear triples T_1..T_r and polynomials h_T, h claimed to satisfy
#     1 = sum_T h_T * d_T + h * (t * g - 1),     g = d_{T_1} * ... * d_{T_r},
# where d_T is the determinant of the three points of T in the chart below and the sum is over triples T inside
# blocks.  Every d_T with T inside a block vanishes on a realization, so if the identity holds, every point of the
# variety of the collinearities has g = 0: one of the T_i is collinear as well.  Hence no realization over C (and
# a fortiori over R) has exactly the collinearities of the blocks.
#
# Chart (a realization can be moved there by a projective map, which preserves collinearity):
#     f0 = (1:0:0), f1 = (0:1:0), f2 = (0:0:1), f3 = (1:1:1);
#     a point p of the block through f0 and f1 (other than f0, f1) is (q_p : 1 : 0)  [it lies on the line z = 0
#     and differs from f0];  every other point is (x_p : y_p : 1)  [it is off the line f0 f1].
# The verifier rebuilds the d_T itself from the blocks; the stored "equations" are not used.  Polynomials are
# dicts {exponent tuple: Fraction}; the identity is checked by exact expansion.
from fractions import Fraction
from itertools import combinations


def p_add(a, b):
    c = dict(a)
    for m, x in b.items():
        y = c.get(m, 0) + x
        if y:
            c[m] = y
        else:
            c.pop(m, None)
    return c


def p_mul(a, b):
    c = {}
    for m1, x1 in a.items():
        for m2, x2 in b.items():
            m = tuple(i + j for i, j in zip(m1, m2))
            y = c.get(m, 0) + x1 * x2
            if y:
                c[m] = y
            else:
                c.pop(m, None)
    return c


def p_scale(a, s):
    return {m: x * s for m, x in a.items()} if s else {}


def p_const(c, nv):
    return {(0,) * nv: Fraction(c)} if c else {}


def p_var(i, nv):
    return {tuple(int(j == i) for j in range(nv)): Fraction(1)}


def p_det3(u, v, w):
    """det of the 3x3 matrix with columns u, v, w (3-vectors of polynomials)"""
    out = {}
    for (i, j, k), s in (((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1), ((0, 2, 1), -1), ((1, 0, 2), -1), ((2, 1, 0), -1)):
        out = p_add(out, p_scale(p_mul(p_mul(u[i], v[j]), w[k]), s))
    return out


def parse_poly(raw, nv):
    if not isinstance(raw, list):
        raise Reject("a polynomial must be a list of terms")
    out = {}
    for term in raw:
        if not (isinstance(term, list) and len(term) == 2 and isinstance(term[0], str) and isinstance(term[1], list)
                and len(term[1]) == nv and all(isinstance(e, int) and not isinstance(e, bool) and e >= 0 for e in term[1])):
            raise Reject("bad term %r" % (term,))
        try:
            c = Fraction(term[0])
        except (ValueError, ZeroDivisionError):
            raise Reject("bad coefficient %r" % (term[0],))
        out = p_add(out, {tuple(term[1]): c})
    return out


def check_linear_space(n, blocks, claimed_type):
    if not (isinstance(blocks, list) and all(isinstance(B, list) for B in blocks)):
        raise Reject("blocks must be a list of lists")
    sets = []
    for B in blocks:
        if not (len(B) >= 3 and len(set(B)) == len(B) and all(isinstance(p, int) and 0 <= p < n for p in B)):
            raise Reject("bad block %r" % (B,))
        sets.append(frozenset(B))
    for A, B in combinations(sets, 2):
        if len(A & B) > 1:
            raise Reject("blocks %s and %s share two points" % (sorted(A), sorted(B)))
    if Counter(len(B) for B in sets) != Counter(claimed_type):
        raise Reject("block sizes %s do not match the type %s" % (sorted(map(len, sets), reverse=True), claimed_type))
    return sets


def verify_rabinowitsch(n, claimed_type, cls):
    """Check one class of a non-realizability proof file.  Returns the number of cofactor terms or raises Reject."""
    try:
        blocks, frame, triples, cof = cls["blocks"], cls["frame"], cls["triples"], cls["cofactors"]
    except (KeyError, TypeError) as e:
        raise Reject("missing field %s" % e)
    sets = check_linear_space(n, blocks, claimed_type)
    def in_block(T):
        return any(set(T) <= B for B in sets)
    if not (isinstance(frame, list) and len(set(frame)) == 4 and all(isinstance(p, int) and 0 <= p < n for p in frame)):
        raise Reject("bad frame %r" % (frame,))
    if any(in_block(T) for T in combinations(frame, 3)):
        raise Reject("three frame points are collinear in the linear space")
    f0, f1, f2, f3 = frame
    blk01 = next((B for B in sets if f0 in B and f1 in B), frozenset((f0, f1)))
    names = []
    for p in range(n):
        if p not in frame:
            names += ["q%d" % p] if p in blk01 else ["x%d" % p, "y%d" % p]
    names.append("t")
    if cof.get("variables") != names:
        raise Reject("variables %r, expected %r" % (cof.get("variables"), names))
    nv = len(names)
    idx = {v: i for i, v in enumerate(names)}
    one, zero = p_const(1, nv), {}
    P = {f0: (one, zero, zero), f1: (zero, one, zero), f2: (zero, zero, one), f3: (one, one, one)}
    for p in range(n):
        if p not in P:
            P[p] = (p_var(idx["q%d" % p], nv), one, zero) if p in blk01 else \
                   (p_var(idx["x%d" % p], nv), p_var(idx["y%d" % p], nv), one)
    def det(T):
        a, b, c = sorted(T)
        return p_det3(P[a], P[b], P[c])
    def triple(T):
        if not (isinstance(T, list) and len(T) == 3 and len(set(T)) == 3 and all(isinstance(p, int) and 0 <= p < n for p in T)):
            raise Reject("bad triple %r" % (T,))
        return tuple(sorted(T))
    if not (isinstance(triples, list) and triples):
        raise Reject("no triples")
    g = one
    for T in triples:
        if in_block(triple(T)):
            raise Reject("triple %r is collinear in the linear space" % (T,))
        g = p_mul(g, det(triple(T)))
    tg1 = p_add(p_mul(p_var(idx["t"], nv), g), p_const(-1, nv))
    total = p_mul(parse_poly(cof["h_rabinowitsch"], nv), tg1)
    terms = len(cof["h_rabinowitsch"])
    for entry in cof["h"]:
        T = triple(entry["triple"])
        if not in_block(T):
            raise Reject("cofactor for %r, which is not inside a block" % (T,))
        total = p_add(total, p_mul(parse_poly(entry["poly"], nv), det(T)))
        terms += len(entry["poly"])
    if total != one:
        raise Reject("the identity 1 = sum h_T d_T + h (t g - 1) fails (%d terms remain)" % len(p_add(total, p_const(-1, nv))))
    return terms


def verify_proof_file(doc):
    """A proof file: {"n", "type", "classes": [...]}.  Every class must pass verify_rabinowitsch."""
    n, claimed_type = doc["n"], doc["type"]
    return [verify_rabinowitsch(n, claimed_type, c) for c in doc["classes"]]


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
    if argv[0] == "--algebraic":
        bad = 0
        for fn in argv[1:]:
            doc = json.load(open(fn))
            try:
                terms = verify_proof_file(doc)
                print("OK %s: type %s, %d classes, each not realizable (cofactor identity holds; %s terms)"
                      % (fn, doc["type"], len(terms), terms))
            except Reject as e:
                bad += 1
                print("REJECT %s: %s" % (fn, e))
        return 1 if bad else 0
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
