# Exact analysis of the pencil set {5, 3^10} for n = 10 (dual: 5 points Q0..Q4 in general position,
# the 10 lines Q_aQ_b grouped in 5 pairs of disjoint lines, each pair meeting at X_i, all X_i collinear).
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
# bivariate polynomials: dict (i,j)->int  meaning x^i y^j
def padd(p, q, s=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + s*v
        if r[k] == 0: del r[k]
    return r
def pmul(p, q):
    r = {}
    for (a, b), u in p.items():
        for (c, d), v in q.items():
            k = (a+c, b+d); r[k] = r.get(k, 0) + u*v
    return {k: v for k, v in r.items() if v}
def const(c): return {(0,0): c} if c else {}
X_ = {(1,0): 1}; Y_ = {(0,1): 1}; ONE = const(1)
def cross(a, b):
    return (padd(pmul(a[1],b[2]), pmul(a[2],b[1]), -1), padd(pmul(a[2],b[0]), pmul(a[0],b[2]), -1), padd(pmul(a[0],b[1]), pmul(a[1],b[0]), -1))
def det3(a, b, c): 
    cr = cross(b, c)
    return padd(padd(pmul(a[0], cr[0]), pmul(a[1], cr[1])), pmul(a[2], cr[2]))
Q = [(ONE, {}, {}), ({}, ONE, {}), ({}, {}, ONE), (ONE, ONE, ONE), (X_, Y_, ONE)]
Xs = []
for i in range(5):
    L1 = cross(Q[i], Q[(i+1)%5]); L2 = cross(Q[(i+2)%5], Q[(i+4)%5])
    Xs.append(cross(L1, L2))
F = [det3(Xs[a], Xs[b], Xs[c]) for a, b, c in combinations(range(5), 3)]
F = [f for f in F if f]
print("equations", len(F), "max total degree", max(max(i+j for i,j in f) for f in F))
# univariate in y with coefficients polys in x
def as_y(f):
    dy = max(j for i, j in f); co = [dict() for _ in range(dy+1)]
    for (i, j), v in f.items(): co[j][i] = v
    return co
def ev_x(cx, x): return sum(Fr(v) * x**i for i, v in cx.items())
def det_frac(M):
    M = [row[:] for row in M]; n = len(M); d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c+1, n):
            f = M[r][c] / M[c][c]
            if f: M[r] = [M[r][k] - f*M[c][k] for k in range(n)]
    return d
def sylvester(a, b):  # a,b lists of coeffs low->high
    a = a[:]; b = b[:]
    while a and a[-1] == 0: a.pop()
    while b and b[-1] == 0: b.pop()
    m, n = len(a)-1, len(b)-1
    if m < 0 or n < 0: return Fr(0)
    if m == 0 and n == 0: return Fr(1)
    N = m + n; M = []
    for i in range(n): M.append([Fr(0)]*i + a[::-1] + [Fr(0)]*(N - m - 1 - i))
    for i in range(m): M.append([Fr(0)]*i + b[::-1] + [Fr(0)]*(N - n - 1 - i))
    return det_frac(M)
def resultant_poly(f, g, deg):
    fy, gy = as_y(f), as_y(g)
    xs = list(range(-deg//2-3, deg//2+4))[:deg+2]
    vals = [sylvester([ev_x(c, Fr(x)) for c in fy], [ev_x(c, Fr(x)) for c in gy]) for x in xs]
    # Newton interpolation -> coefficients
    n = len(xs); coef = vals[:]
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (xs[i] - xs[i-j])
    poly = [Fr(0)]
    for i in range(n-1, -1, -1):
        # poly = poly*(x - xs[i]) + coef[i]
        new = [Fr(0)]*(len(poly)+1)
        for k, c in enumerate(poly):
            new[k+1] += c; new[k] -= c*xs[i]
        new[0] += coef[i]; poly = new
    while len(poly) > 1 and poly[-1] == 0: poly.pop()
    return poly
def pgcd(a, b):
    def trim(p):
        p = p[:]
        while len(p) > 1 and p[-1] == 0: p.pop()
        return p
    a, b = trim(a), trim(b)
    while b != [0] and any(b):
        # a mod b
        a = a[:]
        while len(a) >= len(b) and any(a):
            f = a[-1] / b[-1]; sh = len(a) - len(b)
            for k in range(len(b)): a[k+sh] -= f*b[k]
            a = trim(a)
            if len(a) < len(b) or not any(a): break
        a, b = b, trim(a)
    return [c / a[-1] for c in a]
G = None
for i in range(1, min(len(F), 5)):
    R = resultant_poly(F[0], F[i], 80)
    G = R if G is None else pgcd(G, R)
print("gcd degree in x:", len(G)-1)
roots = np.roots([float(c) for c in G[::-1]])
print("roots of gcd (x):", np.round(roots, 6))
# for each real root solve for y numerically from F[0](x,y)=0 and check all equations + nondegeneracy
def evalf(f, x, y): return sum(v * x**i * y**j for (i, j), v in f.items())
def evX(P, x, y): return np.array([evalf(c, x, y) for c in P], complex)
sols = []
for xr in roots:
    fy = as_y(F[0]); cy = [sum(v * xr**i for i, v in c.items()) for c in fy]
    for yr in np.roots(cy[::-1]):
        if max(abs(evalf(f, xr, yr)) for f in F) > 1e-6: continue
        q = [evX(P, xr, yr) for P in Q]; X = [evX(P, xr, yr) for P in Xs]
        def nrm(v): return v / np.linalg.norm(v)
        deg = any(abs(np.linalg.det(np.array([nrm(q[a]), nrm(q[b]), nrm(q[c])]))) < 1e-8 for a, b, c in combinations(range(5), 3))
        deg = deg or any(np.linalg.norm(np.cross(nrm(X[a]), nrm(X[b]))) < 1e-8 for a, b in combinations(range(5), 2))
        sols.append((xr, yr, "degenerate" if deg else "GOOD"))
for s in sols: print(np.round(s[0], 6), np.round(s[1], 6), s[2])
print("---- debug")
for i, f in enumerate(F): print(i, sorted(f.items()))
for i in range(len(F)):
    for j in range(i+1, len(F)):
        R = resultant_poly(F[i], F[j], 30)
        print(i, j, "deg", len(R)-1, "zero" if not any(R) else "", np.round(np.roots([float(c) for c in R[::-1]]),5) if any(R) and len(R)>1 else "")
