"""Simple matroids of rank <= 4 on n elements, up to isomorphism.

An arrangement of n distinct planes in RP^3 has as intersection lattice a simple matroid of rank <= 4 on the n
planes (rank of a set = dimension of the span of the normal vectors).  This module enumerates all such matroids
for small n by single-element extensions (Crapo): every simple matroid M on n elements arises from the simple
matroid M \\ e on n - 1 elements, either as a coloop extension or from a nonempty modular cut, and modular cuts
correspond bijectively to linear subclasses of hyperplanes (Oxley, Matroid Theory, 2nd ed., Section 7.2).

A matroid is stored by its flats: a dict rank -> frozenset of bitmasks.  Every catalogued matroid is checked
against the flat axioms (is_matroid); completeness is checked against the counts of Mayhew and Royle (OEIS A058733).

usage: python scripts/planes_matroids.py N    -> writes runs/planes_matroids_n{N}.json (all n <= N)
"""

import json
import os
import sys
from itertools import combinations

import networkx as nx


def popcount(x):
    return bin(x).count("1")


def is_matroid(n, flats):
    """Flat axioms: E is a flat, flats are closed under intersection, and for every flat F the flats covering F
    partition E \\ F; ranks increase by one along covers."""
    E = (1 << n) - 1
    r = max(flats)
    if flats[r] != {E} or flats[0] != {0}:
        return False
    allf = {F: k for k, s in flats.items() for F in s}
    for F in allf:
        for G in allf:
            if (F & G) not in allf:
                return False
    for F, k in allf.items():
        if F == E:
            continue
        covers = [G for G, kg in allf.items() if kg == k + 1 and G & F == F]
        seen = 0
        for G in covers:
            d = G & ~F
            if d & seen:
                return False
            seen |= d
        if seen != E & ~F:
            return False
        # nothing strictly between F and a cover of higher rank
        for G, kg in allf.items():
            if G != F and G & F == F and kg <= k:
                return False
    return True


def coloop_extension(n, flats):
    e = 1 << n
    new = {}
    for k, s in flats.items():
        for F in s:
            new.setdefault(k, set()).add(F)
            new.setdefault(k + 1, set()).add(F | e)
    return {k: frozenset(v) for k, v in new.items()}


def linear_subclasses(n, flats):
    """All linear subclasses L of the hyperplanes such that the extension is simple."""
    r = max(flats)
    H = sorted(flats[r - 1])
    idx = {h: i for i, h in enumerate(H)}
    if r < 2:
        return
    # for every flat X of rank r-2: the hyperplanes containing it
    groups = []
    for X in flats[r - 2]:
        groups.append([idx[h] for h in H if h & X == X])
    on = [[] for _ in H]  # groups containing hyperplane i
    for g, members in enumerate(groups):
        for i in members:
            on[i].append(g)
    m = len(H)
    state = [None] * m  # True in L, False out of L

    def ok_group(g):
        mem = groups[g]
        ins = sum(1 for i in mem if state[i] is True)
        outs = sum(1 for i in mem if state[i] is False)
        return not (ins >= 2 and outs >= 1)

    def propagate(stack):
        changed = []
        while stack:
            i = stack.pop()
            for g in on[i]:
                mem = groups[g]
                ins = sum(1 for j in mem if state[j] is True)
                outs = sum(1 for j in mem if state[j] is False)
                if ins >= 2:
                    if outs:
                        return changed, False
                    for j in mem:
                        if state[j] is None:
                            state[j] = True
                            changed.append(j)
                            stack.append(j)
        return changed, True

    E = (1 << n) - 1

    def simple(L):
        # element x is parallel to the new one iff every hyperplane through x is in L
        for x in range(n):
            b = 1 << x
            if all(L[i] for i, h in enumerate(H) if h & b):
                return False
        return True

    def rec(i):
        if i == m:
            L = [s is True for s in state]
            if simple(L):
                yield frozenset(H[j] for j in range(m) if L[j])
            return
        if state[i] is not None:
            yield from rec(i + 1)
            return
        for val in (False, True):
            state[i] = val
            changed, good = propagate([i]) if val else ([], all(ok_group(g) for g in on[i]))
            if good:
                yield from rec(i + 1)
            for j in changed:
                state[j] = None
            state[i] = None

    yield from rec(0)


def extension(n, flats, L):
    """Flats of the extension by element n for the modular cut of the linear subclass L."""
    r = max(flats)
    H = flats[r - 1]
    e = 1 << n
    allf = [(F, k) for k, s in flats.items() for F in s]
    cut = set()
    for F, k in allf:
        if all(h in L for h in H if h & F == F):
            cut.add(F)
    new = {}
    for F, k in allf:
        if F in cut:
            new.setdefault(k, set()).add(F | e)
        else:
            new.setdefault(k, set()).add(F)
            covers_in = any(G in cut for G, kg in allf if kg == k + 1 and G & F == F)
            if not covers_in:
                new.setdefault(k + 1, set()).add(F | e)
    return {k: frozenset(v) for k, v in new.items()}


def graph(n, flats):
    g = nx.Graph()
    r = max(flats)
    for x in range(n):
        g.add_node(("e", x), lab="e")
    for k in range(2, r):
        for F in flats[k]:
            g.add_node(("f", F), lab=f"f{k}")
            for x in range(n):
                if F >> x & 1:
                    g.add_edge(("e", x), ("f", F))
    g.graph["rank"] = r
    return g


def key(n, flats):
    r = max(flats)
    sizes = tuple(sorted((k, popcount(F)) for k in range(2, r) for F in flats[k]))
    prof = tuple(sorted(tuple(sorted((k, popcount(F)) for k in range(2, r) for F in flats[k] if F >> x & 1))
                        for x in range(n)))
    return (r, sizes, prof)


class Catalogue:
    def __init__(self):
        self.buckets = {}
        self.items = []

    def add(self, n, flats):
        """Insert unless isomorphic to a stored matroid; stored matroids are checked against the flat axioms."""
        k = key(n, flats)
        g = graph(n, flats)
        nm = nx.algorithms.isomorphism.categorical_node_match("lab", None)
        for j in self.buckets.get(k, []):
            if nx.is_isomorphic(g, self.items[j][1], node_match=nm):
                return False
        assert is_matroid(n, flats), flats
        self.buckets.setdefault(k, []).append(len(self.items))
        self.items.append((flats, g))
        return True


def enumerate_up_to(N, maxrank=4):
    """levels[n] = list of flats dicts of all simple matroids of rank <= maxrank on n elements."""
    levels = {1: [{0: frozenset([0]), 1: frozenset([1])}]}
    for n in range(2, N + 1):
        cat = Catalogue()
        for flats in levels[n - 1]:
            m = n - 1
            r = max(flats)
            cands = []
            if r < maxrank:
                cands.append(coloop_extension(m, flats))
            for L in linear_subclasses(m, flats):
                cands.append(extension(m, flats, L))
            for c in cands:
                cat.add(n, c)
        levels[n] = [f for f, _ in cat.items]
        by_rank = {}
        for f in levels[n]:
            by_rank[max(f)] = by_rank.get(max(f), 0) + 1
        print(f"n={n}: {len(levels[n])} simple matroids of rank <= {maxrank}, by rank {dict(sorted(by_rank.items()))}",
              flush=True)
    return levels


def dump(levels, path):
    out = {}
    for n, L in levels.items():
        out[n] = [{str(k): sorted(v) for k, v in f.items()} for f in L]
    with open(path, "w") as fh:
        json.dump(out, fh)


def load(path):
    with open(path) as fh:
        raw = json.load(fh)
    return {int(n): [{int(k): frozenset(v) for k, v in f.items()} for f in L] for n, L in raw.items()}


if __name__ == "__main__":
    N = int(sys.argv[1])
    levels = enumerate_up_to(N)
    os.makedirs("runs", exist_ok=True)
    dump(levels, f"runs/planes_matroids_n{N}.json")
