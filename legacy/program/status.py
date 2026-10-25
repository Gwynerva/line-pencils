import json, os, sys
from math import comb, ceil
from cands import candidates
from db import load
def t2(n, s): return comb(n,2) - sum(comb(k,2) for k in s)
def melchior_ok(n, s):
    if s == (n,): return True
    return t2(n,s) >= 3 + sum(k-3 for k in s if k >= 4)
def cs_ok(n, s):
    if s == (n,) or n < 8: return True
    return 13*t2(n,s) >= 6*n
def debruijn_ok(n, s):
    if s == (n,): return True
    return t2(n,s) + len(s) >= n
if __name__ == "__main__":
    db = load()
    for n in range(3, int(sys.argv[1])+1):
        cs = candidates(n)
        a = [s for s in cs if melchior_ok(n,s)]
        b = [s for s in a if cs_ok(n,s)]
        c = [s for s in b if debruijn_ok(n,s)]
        have = set(db.get(n,{}))
        rest = [s for s in c if s not in have]
        print(n, "arith", len(cs), "melchior", len(a), "CS", len(b), "dBE", len(c), "realized", len(have), "open", len(rest))
