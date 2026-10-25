"""Exact isomorphism classes of the linear spaces listed by the engine (mode 5 output).

usage: python scripts/dedupe_enum.py N ENUMFILE OUT.json
Groups the labelled linear spaces by a cheap invariant, then verifies isomorphism inside each group with
networkx's VF2 on the point-block incidence graph (bipartite, with block sizes as labels).  Writes one
representative per isomorphism class with the size of its class.
"""
import json, sys, os
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from find_examples import invariant

n = int(sys.argv[1]); fn = sys.argv[2]; out = sys.argv[3]


def graph(blocks):
    G = nx.Graph()
    for i in range(n):
        G.add_node(("p", i), kind=0)
    for j, B in enumerate(blocks):
        G.add_node(("b", j), kind=len(B))
        for p in B:
            G.add_edge(("p", p), ("b", j))
    return G


def iso(G1, G2):
    return GraphMatcher(G1, G2, node_match=lambda a, b: a["kind"] == b["kind"]).is_isomorphic()


classes = {}   # invariant -> list of [blocks, graph, count]
total = 0
for line in open(fn):
    if not line.startswith("ORIENTABLE"):
        continue
    total += 1
    blocks = [sorted(map(int, b.split(","))) for b in line.split()[1:]]
    inv = invariant(n, blocks)
    G = graph(blocks)
    lst = classes.setdefault(inv, [])
    for rep in lst:
        if iso(rep[1], G):
            rep[2] += 1
            break
    else:
        lst.append([blocks, G, 1])
reps = [{"blocks": r[0], "labelled_count": r[2]} for lst in classes.values() for r in lst]
json.dump({"n": n, "source": fn, "labelled_total": total, "classes": reps}, open(out, "w"), indent=1)
print("labelled orientable linear spaces:", total, "; isomorphism classes:", len(reps), [r["labelled_count"] for r in reps])
