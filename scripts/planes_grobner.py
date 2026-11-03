"""Groebner-basis certificates that certain paving matroids of rank 4 have no realization over any field of
characteristic 0 (in particular no arrangement of real planes).

A matroid is given by its ground set {0, ..., n-1} and its list of dependent 4-sets (all of rank 3; there are no
lines on three planes).  {0, 1, 2, 3} must be a basis; its vectors are fixed to the unit vectors.  An entry
(j, i) of vector j >= 4 is zero if replacing e_i by v_j gives a dependent set, and nonzero otherwise; the
nonzero entries on a spanning tree of the bipartite pattern graph are set to 1 (scaling of the vectors and of the
coordinates).  The ideal of the dependent 4-sets, saturated by the product of the remaining variables and of the
determinant of one further set that must be a basis, is shown to contain 1.

usage: python scripts/planes_grobner.py
"""

import itertools

import networkx as nx
import sympy as sp

CASES = {
    # the dual Fano matroid F7*: complements of the lines of the Fano plane
    "F7*": (7, [[3, 4, 5, 6], [1, 2, 5, 6], [1, 2, 3, 4], [0, 2, 4, 6], [0, 2, 3, 5], [0, 1, 4, 5], [0, 1, 3, 6]]),
    # the two matroids of type  lines {}, points 4{}^11  (n = 8) without a Fano or dual Fano minor
    "A8": (8, [[0, 1, 6, 7], [0, 2, 4, 7], [0, 2, 5, 6], [0, 3, 4, 6], [0, 3, 5, 7], [1, 2, 4, 6], [1, 2, 5, 7],
               [1, 3, 4, 7], [1, 3, 5, 6], [2, 3, 4, 5], [4, 5, 6, 7]]),
    "B8": (8, [[0, 1, 4, 7], [0, 1, 5, 6], [0, 2, 4, 6], [0, 2, 5, 7], [0, 3, 4, 5], [0, 3, 6, 7], [1, 2, 3, 7],
               [1, 2, 4, 5], [1, 3, 4, 6], [2, 3, 5, 6], [4, 5, 6, 7]]),
}


def certificate(n, quads):
    deps = {tuple(sorted(q)) for q in quads}
    assert (0, 1, 2, 3) not in deps
    V = [[sp.Integer(int(i == j)) for i in range(4)] for j in range(4)]
    for j in range(4, n):
        row = []
        for i in range(4):
            S = tuple(sorted([k for k in range(4) if k != i] + [j]))
            row.append(sp.Integer(0) if S in deps else sp.Symbol(f"x{j}_{i}"))
        V.append(row)
    g = nx.Graph()
    for j in range(4, n):
        for i in range(4):
            if V[j][i] != 0:
                g.add_edge(("r", j), ("c", i))
    sub = {}
    for comp in nx.connected_components(g):
        for a, b in nx.bfs_edges(g.subgraph(comp), next(iter(sorted(comp)))):
            j, i = (a[1], b[1]) if a[0] == "r" else (b[1], a[1])
            sub[V[j][i]] = 1
    V = [[x.subs(sub) for x in row] for row in V]
    xs = sorted({s for row in V for x in row for s in x.free_symbols}, key=str)
    det = lambda S: sp.expand(sp.Matrix([V[i] for i in S]).det())  # noqa: E731
    eqs = [d for d in (det(S) for S in deps) if d != 0]
    t = sp.Symbol("t")
    for S in itertools.combinations(range(n), 4):
        if S in deps:
            continue
        d = det(S)
        if d == 0:
            return f"the normalization already forces the basis {S} to be dependent"
        G = sp.groebner(eqs + [t * sp.prod(xs) * d - 1], *xs, t, order="grevlex")
        if list(G.exprs) == [1]:
            return f"1 lies in the ideal saturated by the variables and det{S}"
    return None


if __name__ == "__main__":
    for name, (n, quads) in CASES.items():
        print(name, ":", certificate(n, quads) or "NO CERTIFICATE")
