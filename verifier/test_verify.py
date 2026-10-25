"""Tests for verify.py: known configurations must pass, corrupted certificates must be rejected.

Run:  python verifier/verify.py --self-test     or     python -m unittest verifier.test_verify
"""
import copy, os, random, sys, unittest
from fractions import Fraction as F
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify import verify, Reject, cross


def Q(*ints):
    """a line (or point) with integer coefficients, as the certificate format wants it"""
    return [[int(c), 0] for c in ints]


def join(p, q):
    """exact line through two integer points (x:y:z) -> integer triple"""
    x = cross(tuple((c, 0) for c in p), tuple((c, 0) for c in q), 0)
    return tuple(c[0] for c in x)


def pappus_cert():
    """Dual Pappus: the 9 points of a Pappus configuration, read as lines.  Type {3^9}, n = 9.

    A = (0,0),(1,0),(2,0) and B = (0,1),(1,1),(3,1); the three cross-joins A_iB_j ∩ A_jB_i are
    (1/2,1/2), (6/5,2/5), (5/3,1/3), collinear by Pappus.  (With B3 = (2,1) an extra triple appears.)"""
    pts = [(0, 0, 1), (1, 0, 1), (2, 0, 1), (0, 1, 1), (1, 1, 1), (3, 1, 1), (1, 1, 2), (6, 2, 5), (5, 1, 3)]
    return {"n": 9, "d": 0, "type": [3] * 9, "lines": [Q(*p) for p in pts], "source": "test: dual Pappus"}


def desargues_cert():
    """Dual Desargues 10_3: two triangles in perspective from O; the three axis points are collinear."""
    O, A, A2, B, B2, C, C2 = (0, 0, 1), (1, 0, 1), (2, 0, 1), (0, 1, 1), (0, 2, 1), (1, 2, 1), (3, 6, 1)
    P = join(join(A, B), join(A2, B2)); R = join(join(B, C), join(B2, C2)); S = join(join(C, A), join(C2, A2))
    pts = [O, A, A2, B, B2, C, C2, P, R, S]
    return {"n": 10, "d": 0, "type": [3] * 10, "lines": [Q(*p) for p in pts], "source": "test: dual Desargues"}


def pentagon_cert():
    """{5, 3^10} with 10 lines: a regular pentagram (5 lines) plus its 5 axes of symmetry.  Needs sqrt 5.

    Vertices V_k = (T_k(c), U_{k-1}(c)) with c = cos(2*pi/5) = (-1 + sqrt 5)/4 and Chebyshev
    polynomials T, U: this is an affine image of the regular pentagon with coordinates in Q(sqrt 5)."""
    def qmul(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
    def qsub(x, y): return (x[0] - y[0], x[1] - y[1])
    c = (F(-1, 4), F(1, 4)); one = (F(1), F(0)); zero = (F(0), F(0)); two_c = (c[0] * 2, c[1] * 2)
    T = [one, c]; U = [one, two_c]
    for _ in range(2, 6):
        T.append(qsub(qmul(two_c, T[-1]), T[-2])); U.append(qsub(qmul(two_c, U[-1]), U[-2]))
    V = [(T[k], zero if k == 0 else U[k - 1]) for k in range(5)]

    def through(p, q):
        pv = (p[0], p[1], one); qv = (q[0], q[1], one)
        return [qsub(qmul(pv[1], qv[2]), qmul(pv[2], qv[1])),
                qsub(qmul(pv[2], qv[0]), qmul(pv[0], qv[2])),
                qsub(qmul(pv[0], qv[1]), qmul(pv[1], qv[0]))]

    def clear(vec):
        den = 1
        for e in vec:
            for f in e:
                den = den * f.denominator // gcd(den, f.denominator)
        return [[int(f * den) for f in e] for e in vec]

    lines = [through(V[k], V[(k + 2) % 5]) for k in range(5)] + [through((zero, zero), V[k]) for k in range(5)]
    return {"n": 10, "d": 5, "type": [5] + [3] * 10, "lines": [clear(L) for L in lines], "source": "test: pentagram + axes"}


def near_pencil(n):
    return {"n": n, "d": 0, "type": [n - 1], "lines": [Q(1, k, 0) for k in range(n - 1)] + [Q(0, 0, 1)]}


def general_position(n, seed=1):
    rng = random.Random(seed)
    while True:
        lines = [Q(rng.randint(-50, 50), rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(n)]
        c = {"n": n, "d": 0, "type": [], "lines": lines}
        try:
            if verify(c) == []:
                return c
        except Reject:
            continue


def independent_type(cert):
    """A second, deliberately different computation of the type, used only to judge the tests:
    3x3 determinants over Q(sqrt d) with Fractions, collinear triples grouped by their lines."""
    d = cert["d"]
    def m(x, y): return (x[0] * y[0] + d * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
    def a(x, y): return (x[0] + y[0], x[1] + y[1])
    def s_(x, y): return (x[0] - y[0], x[1] - y[1])
    L = [[(F(c[0]), F(c[1])) for c in line] for line in cert["lines"]]
    def det(p, q, r):
        t1 = m(p[0], s_(m(q[1], r[2]), m(q[2], r[1])))
        t2 = m(p[1], s_(m(q[0], r[2]), m(q[2], r[0])))
        t3 = m(p[2], s_(m(q[0], r[1]), m(q[1], r[0])))
        return a(s_(t1, t2), t3)
    n = cert["n"]
    from itertools import combinations
    # for each pair the set of lines concurrent with it
    groups = set()
    for i, j in combinations(range(n), 2):
        S = {i, j}
        for k in range(n):
            if k not in S and det(L[i], L[j], L[k]) == (0, 0):
                S.add(k)
        groups.add(frozenset(S))
    return sorted((len(S) for S in groups if len(S) >= 3), reverse=True)


def proportional(u, v):
    """u = c*v for a rational c (enough for the tests: only integer rescalings occur)."""
    return all(u[i][0] * v[j][0] == u[j][0] * v[i][0] and u[i][1] * v[j][1] == u[j][1] * v[i][1] and u[i][0] * v[j][1] == u[j][1] * v[i][0] for i in range(3) for j in range(3))


class Accept(unittest.TestCase):
    def test_pappus(self):
        self.assertEqual(verify(pappus_cert()), [3] * 9)

    def test_desargues(self):
        self.assertEqual(verify(desargues_cert()), [3] * 10)

    def test_pentagon_sqrt5(self):
        self.assertEqual(verify(pentagon_cert()), [5] + [3] * 10)

    def test_pencil_and_near_pencil(self):
        self.assertEqual(verify(near_pencil(7)), [6])
        self.assertEqual(verify({"n": 5, "d": 0, "type": [5], "lines": [Q(1, k, 0) for k in range(5)]}), [5])

    def test_general_position(self):
        self.assertEqual(verify(general_position(8)), [])

    def test_type_order_irrelevant(self):
        c = pentagon_cert(); c["type"] = [3] * 5 + [5] + [3] * 5
        self.assertEqual(verify(c), [5] + [3] * 10)

    def test_fano_coordinates_over_Q_lose_a_triple(self):
        # the 7 non-zero vectors of GF(2)^3, read over Q, give {3^6}: the triple (1,1,0),(1,0,1),(0,1,1) is not concurrent over Q
        lines = [Q(*v) for v in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]]
        self.assertEqual(verify({"n": 7, "d": 0, "type": [3] * 6, "lines": lines}), [3] * 6)
        with self.assertRaises(Reject):
            verify({"n": 7, "d": 0, "type": [3] * 7, "lines": lines})


class RejectBad(unittest.TestCase):
    def assertRejects(self, cert, msg=None):
        with self.assertRaises(Reject, msg=msg):
            verify(cert)

    def test_wrong_type(self):
        c = pappus_cert(); c["type"] = [3] * 8
        self.assertRejects(c)
        c = pappus_cert(); c["type"] = [4] + [3] * 7
        self.assertRejects(c)

    def test_every_single_number_changed(self):
        """Changing any one integer of a configuration: the verifier must reject, unless the change
        merely rescales a line, or the changed configuration genuinely still has the claimed type
        (which happens occasionally; an independent determinant computation is the judge)."""
        accepted = 0
        for base in (pappus_cert(), desargues_cert(), pentagon_cert()):
            for i in range(base["n"]):
                for j in range(3):
                    for part in (0, 1):
                        c = copy.deepcopy(base)
                        c["lines"][i][j][part] += 1
                        try:
                            verify(c)
                        except Reject:
                            continue
                        accepted += 1
                        if proportional(c["lines"][i], base["lines"][i]):
                            continue
                        self.assertEqual(independent_type(c), sorted(base["type"], reverse=True),
                                         "perturbed certificate accepted: %s line %d coord %d part %d" % (base["source"], i, j, part))
        self.assertLess(accepted, 8)   # the vast majority of perturbations must be rejected

    def test_duplicate_line(self):
        c = pappus_cert(); c["lines"][3] = [[2 * x for x in e] for e in c["lines"][0]]
        self.assertRejects(c)

    def test_zero_line(self):
        c = pappus_cert(); c["lines"][0] = Q(0, 0, 0)
        self.assertRejects(c)

    def test_bad_field(self):
        for d in (4, 9, 1, -5, 2.0, "5", True, None):
            c = pentagon_cert(); c["d"] = d
            self.assertRejects(c, "d=%r" % (d,))

    def test_float_or_bool_coordinates(self):
        c = pappus_cert(); c["lines"][0][0] = [0.5, 0]
        self.assertRejects(c)
        c = pappus_cert(); c["lines"][0][0] = [True, 0]
        self.assertRejects(c)

    def test_wrong_n(self):
        c = pappus_cert(); c["n"] = 8
        self.assertRejects(c)
        c = pappus_cert(); c["lines"].append(Q(7, 11, 13));
        self.assertRejects(c)

    def test_pentagon_needs_sqrt5(self):
        # the same integer pairs read in Q(sqrt 2) or Q(sqrt 7): the pentagram concurrences disappear
        for d in (2, 7):
            c = pentagon_cert(); c["d"] = d
            self.assertRejects(c)

    def test_random_fuzz(self):
        rng = random.Random(7)
        for _ in range(300):
            base = rng.choice((pappus_cert(), desargues_cert(), pentagon_cert()))
            i = rng.randrange(base["n"]); j = rng.randrange(3); part = rng.randrange(2) if base["d"] else 0
            orig = copy.deepcopy(base["lines"][i])
            base["lines"][i][j][part] += rng.choice((-3, -2, -1, 1, 2, 3))
            try:
                verify(base)
            except Reject:
                continue
            if not proportional(base["lines"][i], orig):
                self.assertEqual(independent_type(base), sorted(base["type"], reverse=True), "fuzzed certificate accepted")


if __name__ == "__main__":
    unittest.main()
