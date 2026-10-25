"""Shared helpers: arithmetic candidates, classical necessary conditions, formatting.

A *type* is written as a tuple of pencil sizes k >= 3 in non-increasing order,
e.g. (5, 3, 3) for {5, 3^2, 2^...}.  Double points are implicit:
    t2 = C(n,2) - sum C(k,2).
"""
from math import comb


def candidates(n):
    """All multisets of integers k in [3, n] with sum C(k,2) <= C(n,2) (non-increasing tuples)."""
    tot = comb(n, 2)
    out = []

    def rec(maxk, budget, cur):
        out.append(tuple(cur))
        for k in range(min(maxk, n), 2, -1):
            c = comb(k, 2)
            if c <= budget:
                cur.append(k)
                rec(k, budget - c, cur)
                cur.pop()

    rec(n, tot, [])
    return out


def t2(n, s):
    return comb(n, 2) - sum(comb(k, 2) for k in s)


def f0(n, s):
    """Number of intersection points of an arrangement of type s."""
    return t2(n, s) + len(s)


def melchior_ok(n, s):
    """Melchior 1941: for a non-pencil arrangement, t2 >= 3 + sum_{k>=4} (k-3) t_k."""
    if s == (n,):
        return True
    return t2(n, s) >= 3 + sum(k - 3 for k in s if k >= 4)


def csima_sawyer_ok(n, s):
    """Csima-Sawyer 1993: t2 >= 6n/13 for n >= 8 unless the arrangement is a pencil
    (the only exception, the Kelly-Moser 7-line arrangement, has n = 7)."""
    if s == (n,) or n < 8:
        return True
    return 13 * t2(n, s) >= 6 * n


def debruijn_erdos_ok(n, s):
    """de Bruijn-Erdos 1948 (dual form): a non-pencil arrangement has at least n points."""
    if s == (n,):
        return True
    return f0(n, s) >= n


def theorem_ok(n, s):
    return melchior_ok(n, s) and csima_sawyer_ok(n, s) and debruijn_erdos_ok(n, s)


def fmt(s, n=None, with_twos=False):
    """{6, 4, 3^12} style string."""
    from collections import Counter
    c = Counter(s)
    parts = []
    for k in sorted(c, reverse=True):
        parts.append(f"{k}^{c[k]}" if c[k] > 1 else str(k))
    if with_twos and n is not None:
        m = t2(n, s)
        if m:
            parts.append(f"2^{m}" if m > 1 else "2")
    return "{" + ", ".join(parts) + "}"


def key(s):
    return ",".join(map(str, s))


def unkey(k):
    return tuple(int(x) for x in k.split(",")) if k else ()
