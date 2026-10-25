# Exact projective geometry over the integers (dual picture):
# a configuration of n points in RP^2 <-> n lines; a line through k of the points <-> a k-fold pencil.
from math import gcd
import random

def norm(v):
    g = gcd(gcd(abs(v[0]),abs(v[1])),abs(v[2]))
    if g == 0: return None
    v = (v[0]//g, v[1]//g, v[2]//g)
    for c in v:
        if c != 0:
            if c < 0: v = (-v[0],-v[1],-v[2])
            break
    return v

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def blocks(P):
    """All lines spanned by the points, as sorted tuples of point indices."""
    n = len(P)
    cov = [0]*n
    res = []
    for i in range(n):
        for j in range(i+1,n):
            if cov[i]>>j & 1: continue
            L = cross(P[i],P[j])
            on = [k for k in range(n) if dot(L,P[k])==0]
            m = 0
            for k in on: m |= 1<<k
            for k in on: cov[k] |= m
            res.append(tuple(on))
    return res

def signature(P):
    """Multiset of pencil sizes >=3 (the user's notation, 2s omitted), sorted desc."""
    P = [norm(p) for p in P]
    if any(p is None for p in P) or len(set(P)) < len(P): return None
    return tuple(sorted((len(b) for b in blocks(P) if len(b)>=3), reverse=True))
