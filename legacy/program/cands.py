# Arithmetic candidates: multisets of pencil sizes k>=3 with sum C(k,2) <= C(n,2)
from math import comb
def candidates(n):
    tot = comb(n,2)
    out = []
    def rec(maxk, budget, cur):
        out.append(tuple(cur))
        for k in range(min(maxk, n), 2, -1):
            c = comb(k,2)
            if c <= budget:
                cur.append(k); rec(k, budget-c, cur); cur.pop()
    rec(n, tot, [])
    return out
if __name__ == "__main__":
    for n in range(1,16):
        print(n, len(candidates(n)))
