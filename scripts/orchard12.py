"""Exclude the type {3^20} for 12 lines by an exhaustive orientability check.

Dually, a type {3^20} of 12 lines is a linear space on 12 points with 20 blocks of size 3 and
t_2 = 66 - 60 = 6 uncovered pairs.  Every point lies on (11 - d)/2 triples, where d is the number
of uncovered pairs at the point, so d is odd; as the d's sum to 12, every d equals 1: the uncovered
pairs form a perfect matching F.  Adding a new point oo and the six blocks {oo} + e (e in F) gives a
Steiner triple system of order 13, and conversely deleting a point of an STS(13) gives such a
linear space.  There are exactly two STS(13) up to isomorphism (Colbourn-Rosa, Triple Systems), so
the linear spaces of type {3^20} are the point-deleted STS(13), one per orbit of the automorphism
group on points.

This script
  1. finds both STS(13) by Stinson's hill-climbing (distinguished by the number of Pasch
     configurations, 13 for the cyclic system and 8 for the other),
  2. deletes every point and keeps one linear space per isomorphism class (exact canonical form by
     brute force over relabellings is too slow, so a certified test is used: networkx graph
     isomorphism of the point-block incidence graphs),
  3. decides orientability of each class, and of every one of the 26 point deletions, with the SAT
     encoding of scripts/sat_orient.py.  Result: none is orientable, so {3^20} is not realizable.

usage: python scripts/orchard12.py [OUT.json]
"""
import json, os, random, sys
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def stinson(v, rng):
    """Random STS(v) by Stinson's hill-climbing."""
    live = {x: set(y for y in range(v) if y != x) for x in range(v)}   # uncovered partners
    other = {}                                                          # (x,y) -> z for blocks
    blocks = set()
    nb = v * (v - 1) // 6
    while len(blocks) < nb:
        x = rng.choice([p for p in range(v) if live[p]])
        y, z = rng.sample(sorted(live[x]), 2)
        if z in live[y]:
            blocks.add(frozenset((x, y, z)))
        else:
            w = other[(y, z)]
            old = frozenset((y, z, w))
            blocks.discard(old)
            for a, b in ((y, w), (z, w)):
                live[a].add(b); live[b].add(a); other.pop((a, b), None); other.pop((b, a), None)
            other.pop((y, z), None); other.pop((z, y), None)
            live[y].add(z); live[z].add(y)
            blocks.add(frozenset((x, y, z)))
        for a, b in ((x, y), (x, z), (y, z)):
            live[a].discard(b); live[b].discard(a)
        c = {x, y, z}
        for a, b in ((x, y), (x, z), (y, z)):
            (t,) = c - {a, b}
            other[(a, b)] = t; other[(b, a)] = t
    return [tuple(sorted(B)) for B in blocks]


def pasch(blocks):
    bs = [set(B) for B in blocks]
    cnt = 0
    for quad in combinations(range(len(bs)), 4):
        pts = set().union(*(bs[i] for i in quad))
        if len(pts) == 6 and all(len(bs[i] & bs[j]) == 1 for i, j in combinations(quad, 2)):
            cnt += 1
    return cnt


def check_sts(v, blocks):
    pairs = set()
    for B in blocks:
        for p in combinations(B, 2):
            assert p not in pairs
            pairs.add(p)
    assert len(pairs) == v * (v - 1) // 2


def incidence(n, blocks):
    import networkx as nx
    g = nx.Graph()
    g.add_nodes_from(("p", i) for i in range(n))
    for j, B in enumerate(blocks):
        for i in B:
            g.add_edge(("p", i), ("b", j))
    nx.set_node_attributes(g, {u: u[0] for u in g.nodes}, "kind")
    return g


def main():
    import networkx as nx
    from networkx.algorithms.isomorphism import categorical_node_match
    from sat_orient import orientable_fixed
    out = sys.argv[1] if len(sys.argv) > 1 else None
    rng = random.Random(2026)
    systems = {}
    tries = 0
    while len(systems) < 2 and tries < 20000:
        tries += 1
        S = stinson(13, rng)
        check_sts(13, S)
        systems.setdefault(pasch(S), S)
    assert sorted(systems) == [8, 13], systems.keys()
    match = categorical_node_match("kind", None)
    classes = []
    for pc, S in sorted(systems.items()):
        for oo in range(13):
            rest = [B for B in S if oo not in B]
            relabel = {p: i for i, p in enumerate(q for q in range(13) if q != oo)}
            L = sorted(tuple(sorted(relabel[p] for p in B)) for B in rest)
            assert len(L) == 20
            g = incidence(12, L)
            if any(nx.is_isomorphic(g, h, node_match=match) for _, _, h, _ in classes):
                continue
            classes.append((pc, oo, g, L))
    # soundness does not rest on the isomorphism test: every point deletion is checked
    for pc, S in sorted(systems.items()):
        for oo in range(13):
            rest = [B for B in S if oo not in B]
            relabel = {p: i for i, p in enumerate(q for q in range(13) if q != oo)}
            L = [[relabel[p] for p in B] for B in rest]
            assert not orientable_fixed(12, L), (pc, oo)
    print("all 26 point deletions of the two STS(13) are non-orientable")
    res = []
    for pc, oo, g, L in classes:
        ok = orientable_fixed(12, [list(B) for B in L])
        res.append({"sts13_pasch": pc, "deleted_point": oo, "blocks": [list(B) for B in L], "orientable": bool(ok)})
        print("STS(13) with %d Pasch, delete point %d: orientable = %s" % (pc, oo, ok), flush=True)
    print("%d isomorphism classes of linear spaces of type {3^20} on 12 points; orientable: %d"
          % (len(res), sum(r["orientable"] for r in res)))
    if out:
        json.dump({"type": [3] * 20, "n": 12, "classes": res}, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
