"""Arithmetic sieve for local types of n planes: count pairs (lambda, pi) allowed by the two counting identities.

lambda: multiset of line sizes k, 3 <= k <= n;  pi: multiset of points (m, tau), 4 <= m <= n, tau a multiset of
pencil sizes 3 <= p <= m - 1 with sum C(p,2) <= C(m,2).  Conditions (pairs and triples of planes):
    sum_lambda C(k,2) <= C(n,2),
    sum_lambda C(k,3) + sum_pi [C(m,3) - sum_tau C(p,3)] <= C(n,3).
usage: python scripts/planes_arith.py N
"""

import sys
from functools import lru_cache
from math import comb


def taus(m):
    out = []

    def rec(maxp, left, cur):
        out.append(tuple(cur))
        for p in range(min(maxp, m - 1), 2, -1):
            if comb(p, 2) <= left:
                rec(p, left - comb(p, 2), cur + [p])
    rec(m - 1, comb(m, 2), [])
    return out


def a(n):
    weights = [comb(m, 3) - sum(comb(p, 3) for p in t) for m in range(4, n + 1) for t in taus(m)]

    @lru_cache(None)
    def points(i, budget):  # multisets of point kinds i.. with total triple weight <= budget
        if i == len(weights):
            return 1
        tot = 0
        c = 0
        while c * weights[i] <= budget:
            tot += points(i + 1, budget - c * weights[i])
            c += 1
        return tot

    total = 0

    def lines(maxk, pairs, triples):
        nonlocal total
        total += points(0, triples)
        for k in range(maxk, 2, -1):
            if comb(k, 2) <= pairs and comb(k, 3) <= triples:
                lines(k, pairs - comb(k, 2), triples - comb(k, 3))
    lines(n, comb(n, 2), comb(n, 3))
    return total


if __name__ == "__main__":
    print([a(n) for n in range(1, int(sys.argv[1]) + 1)])
