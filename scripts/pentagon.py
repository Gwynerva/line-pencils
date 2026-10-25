"""Exact analysis of the type {5, 3^10} for ten lines (dual: ten points, one 5-point line L, ten 3-point lines).

Step 1 (proved in docs/theorems.md): the five points off L, X_1..X_5, are in general position, and every one of the
ten lines X_jX_k passes through one of the five points Q_i of L, two through each Q_i.  So Q_i corresponds to a
pair of disjoint edges of K_5, and the five pairs partition the edge set.  (Counting shows each vertex is missed
by exactly one pair; we do not even need that.)

Step 2 (this script): enumerate all such partitions, reduce them modulo relabelling of X_1..X_5, and for each
class solve exactly the condition "the five points Q_i are collinear" with X_1, X_2, X_3, X_4 as projective frame
and X_5 = (x : y : 1) unknown.  Non-degenerate solutions (no three X's collinear, the Q_i distinct) are listed
with their field of definition.

Result (printed): every non-degenerate real solution is an affine image of the regular pentagon and needs sqrt(5).
"""
import itertools, sys
import sympy as sp

V = range(5)
edges = [frozenset(e) for e in itertools.combinations(V, 2)]
pairs = [frozenset((e, f)) for e, f in itertools.combinations(edges, 2) if not (e & f)]   # disjoint edge pairs (15)

# all ways to pick 5 disjoint-edge pairs that partition the 10 edges
parts = []
for combo in itertools.combinations(pairs, 5):
    used = [e for p in combo for e in p]
    if len(set(used)) == 10:
        parts.append(frozenset(combo))
print("partitions of E(K5) into 5 pairs of disjoint edges:", len(parts))

# orbits under S_5
def relabel(part, perm):
    return frozenset(frozenset(frozenset(perm[v] for v in e) for e in p) for p in part)
seen = set(); classes = []
for part in parts:
    if part in seen:
        continue
    orbit = {relabel(part, perm) for perm in itertools.permutations(V)}
    seen |= orbit
    classes.append((part, len(orbit)))
print("isomorphism classes:", [(len(c[0]), c[1]) for c in classes])

x, y = sp.symbols("x y")
X = {0: sp.Matrix([1, 0, 0]), 1: sp.Matrix([0, 1, 0]), 2: sp.Matrix([0, 0, 1]), 3: sp.Matrix([1, 1, 1]), 4: sp.Matrix([x, y, 1])}
def line(p, q): return X[p].cross(X[q])
def meet(l1, l2): return l1.cross(l2)

for part, size in classes:
    Q = []
    for p in part:
        e, f = tuple(p)
        (a, b), (c, d) = tuple(e), tuple(f)
        Q.append(meet(line(a, b), line(c, d)))
    eqs = [sp.expand(sp.Matrix.hstack(Q[i], Q[j], Q[k]).det()) for i, j, k in itertools.combinations(range(5), 3)]
    eqs = [e for e in eqs if e != 0]
    G = sp.groebner(eqs, x, y, order="lex")
    sols = sp.solve(list(G), [x, y], dict=True)
    print("\nclass (orbit size %d):" % size, sorted((tuple(sorted(e)), tuple(sorted(f))) for e, f in part))
    for s in sols:
        xv, yv = s[x], s[y]
        X5 = sp.Matrix([xv, yv, 1])
        degenerate = any(sp.simplify(sp.Matrix.hstack(X[i], X[j], X5).det()) == 0 for i, j in itertools.combinations(range(4), 2))
        Qs = [sp.simplify(q.subs(s)) for q in Q]
        distinct = all(sp.simplify(Qs[i].cross(Qs[j]).norm() ** 2) != 0 for i, j in itertools.combinations(range(5), 2))
        print("  X5 = (%s : %s : 1)  degenerate=%s  Q's distinct=%s  real=%s" % (xv, yv, degenerate, distinct, (sp.im(xv) == 0 and sp.im(yv) == 0)))
    if not sols:
        print("  no solutions (the five Q_i are never collinear)")
