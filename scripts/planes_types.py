"""Types of plane arrangements, computed from the intersection lattice (flats of a simple matroid of rank <= 4).

Lines of the arrangement are the flats of rank 2, points the flats of rank 3 (the whole ground set counts when the
rank is 2 or 3: all planes through one line, or through one point).  For a flat X, |X| is the number of planes
containing it.

  size_type(n, flats)      (line sizes >= 3, point sizes >= 4)                        -- multisets
  local_type(n, flats)     (line sizes >= 3, [(m, tau)] for points on m >= 4 planes)  -- tau = planar pencil type
                                                                                         of the planes through P
  incidence_graph(n, flats) special lines and points with sizes, and which line passes through which point
"""

import networkx as nx


def popcount(x):
    return bin(x).count("1")


def lines_points(flats):
    return sorted(flats.get(2, ())), sorted(flats.get(3, ()))


def size_type(n, flats):
    L, P = lines_points(flats)
    return (tuple(sorted((popcount(x) for x in L if popcount(x) >= 3), reverse=True)),
            tuple(sorted((popcount(p) for p in P if popcount(p) >= 4), reverse=True)))


def local_tau(p, L):
    return tuple(sorted((popcount(x) for x in L if x & p == x and popcount(x) >= 3), reverse=True))


def local_type(n, flats):
    L, P = lines_points(flats)
    pts = sorted(((popcount(p), local_tau(p, L)) for p in P if popcount(p) >= 4), reverse=True)
    return (size_type(n, flats)[0], tuple(pts))


def f_vector(n, flats):
    L, P = lines_points(flats)
    return len(P), len(L)


def incidence_graph(n, flats):
    L, P = lines_points(flats)
    g = nx.Graph()
    sl = [x for x in L if popcount(x) >= 3]
    sp = [p for p in P if popcount(p) >= 4]
    for x in sl:
        g.add_node(("l", x), lab=("l", popcount(x)))
    for p in sp:
        g.add_node(("p", p), lab=("p", popcount(p), local_tau(p, L)))
        for x in sl:
            if x & p == x:
                g.add_edge(("l", x), ("p", p))
    return g


class GraphClasses:
    """Isomorphism classes of labelled incidence graphs."""

    def __init__(self):
        self.reps = {}

    def add(self, g):
        k = (tuple(sorted(str(d["lab"]) for _, d in g.nodes(data=True))), g.number_of_edges(),
             nx.weisfeiler_lehman_graph_hash(g, node_attr="lab"))
        nm = nx.algorithms.isomorphism.categorical_node_match("lab", None)
        for j, h in enumerate(self.reps.get(k, [])):
            if nx.is_isomorphic(g, h, node_match=nm):
                return (k, j)
        self.reps.setdefault(k, []).append(g)
        return (k, len(self.reps[k]) - 1)


def fmt_multiset(t):
    out = []
    i = 0
    while i < len(t):
        j = i
        while j < len(t) and t[j] == t[i]:
            j += 1
        out.append(str(t[i]) + (f"^{j - i}" if j - i > 1 else ""))
        i = j
    return "{" + ", ".join(out) + "}"


def fmt_size(t):
    return f"lines {fmt_multiset(t[0])}, points {fmt_multiset(t[1])}"


def fmt_local(t):
    pts = []
    for m, tau in t[1]:
        pts.append(f"{m}{fmt_multiset(tau)}")
    return f"lines {fmt_multiset(t[0])}, points [" + ", ".join(pts) + "]"
