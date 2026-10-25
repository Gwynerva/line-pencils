# Construct exact point pools that are rich in collinearities.
from fractions import Fraction as Fr
import math
from pool import Pool, from_frac, rat, with_intersections

# ---------- elliptic curves in Tate normal form with a rational torsion point ----------
# E: y^2 + (1-c)xy - b y = x^3 - b x^2 ,  P = (0,0)
def ec_ops(a1, a2, a3, a4, a6):
    O = None
    def neg(P):
        if P is None: return None
        x, y = P
        return (x, -y - a1*x - a3)
    def addp(P, Q):
        if P is None: return Q
        if Q is None: return P
        x1, y1 = P; x2, y2 = Q
        if x1 == x2:
            if y1 + y2 + a1*x2 + a3 == 0: return None
            lam = (3*x1*x1 + 2*a2*x1 + a4 - a1*y1) / (2*y1 + a1*x1 + a3)
        else:
            lam = (y2 - y1) / (x2 - x1)
        nu = y1 - lam*x1
        x3 = lam*lam + a1*lam - a2 - x1 - x2
        y3 = -(lam + a1)*x3 - nu - a3
        return (x3, y3)
    return addp, neg

def tate_multiples(b, c, N):
    b = Fr(b); c = Fr(c)
    addp, neg = ec_ops(1 - c, -b, -b, Fr(0), Fr(0))
    P = (Fr(0), Fr(0)); Q = None; pts = []
    for k in range(N):
        pts.append(Q)
        Q = addp(Q, P)
    if Q is not None: return None        # P does not have order dividing N
    if any(pts[k] is None for k in range(1, N)): return None   # smaller order
    return pts

def kubert(N, t):
    t = Fr(t)
    if N == 7:  b, c = t**3 - t**2, t**2 - t
    elif N == 8: b, c = (2*t-1)*(t-1), (2*t-1)*(t-1)/t
    elif N == 9: c = t**2*(t-1); b = c*(t**2 - t + 1)
    elif N == 10:
        c = (2*t**3 - 3*t**2 + t) / (t - (t-1)**2)
        b = c * t**2 / (t - (t-1)**2)
    elif N == 12:
        c = (3*t**2 - 3*t + 1)*(t - 2*t**2) / (t-1)**3
        b = c * (-2*t**2 + 2*t - 1) / (t-1)
    else: raise ValueError
    return b, c

def torsion_points(N, t):
    b, c = kubert(N, t)
    pts = tate_multiples(b, c, N)
    if pts is None: return None
    out = []
    for P in pts:
        if P is None: out.append(from_frac(((0,0),(1,0),(0,0))))
        else: out.append(from_frac(((P[0],0),(P[1],0),(1,0))))
    return out

# ---------- regular polygons, affinely normalised so coordinates lie in Q(sqrt d) ----------
# vertex k: (T_k(c), U_{k-1}(c)) with c = cos(2 pi/m); T,U Chebyshev polynomials.
class QD:
    """a + b sqrt(d) with Fractions"""
    def __init__(s, a, b=0, d=0): s.a = Fr(a); s.b = Fr(b); s.d = d
    def __add__(s, o): o = o if isinstance(o, QD) else QD(o, 0, s.d); return QD(s.a+o.a, s.b+o.b, s.d)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, QD) else QD(o, 0, s.d); return QD(s.a-o.a, s.b-o.b, s.d)
    def __rsub__(s, o): return QD(o, 0, s.d) - s
    def __mul__(s, o):
        o = o if isinstance(o, QD) else QD(o, 0, s.d)
        return QD(s.a*o.a + s.d*s.b*o.b, s.a*o.b + s.b*o.a, s.d)
    __rmul__ = __mul__
    def pair(s): return (s.a, s.b)

def cos_field(m):
    # returns (d, cos(2pi/m) as QD)
    if m == 3: return 0, QD(Fr(-1,2))
    if m == 4: return 0, QD(0)
    if m == 6: return 0, QD(Fr(1,2))
    if m == 5: return 5, QD(Fr(-1,4), Fr(1,4), 5)
    if m == 10: return 5, QD(Fr(1,4), Fr(1,4), 5)
    if m == 8: return 2, QD(0, Fr(1,2), 2)
    if m == 12: return 3, QD(0, Fr(1,2), 3)
    raise ValueError

def polygon_pool_points(m, center=True, infinity=True, extra_intersections=0):
    d, c = cos_field(m)
    T = [QD(1,0,d), c]; U = [QD(1,0,d), 2*c]   # T_0,T_1 ; U_0,U_1
    for k in range(2, m+2):
        T.append(2*c*T[-1] - T[-2]); U.append(2*c*U[-1] - U[-2])
    verts = []
    for k in range(m):
        x = T[k]
        y = QD(0,0,d) if k == 0 else U[k-1]
        verts.append((x, y))
    pts = [from_frac((x.pair(), y.pair(), (1,0))) for x, y in verts]
    if center: pts.append(from_frac(((0,0),(0,0),(1,0))))
    if infinity:
        for i in range(m):
            for j in range(i+1, m):
                dx = verts[i][0] - verts[j][0]; dy = verts[i][1] - verts[j][1]
                pts.append(from_frac((dx.pair(), dy.pair(), (0,0))))
    return d, pts

def grid_points(m, dmax=2):
    pts = [rat(x, y) for x in range(m) for y in range(m)]
    for a in range(-dmax, dmax+1):
        for b in range(0, dmax+1):
            if (a, b) != (0, 0) and math.gcd(abs(a), b) == 1 and (b > 0 or a > 0):
                pts.append(rat(a, b, 0))
    return pts

def tri_lattice(r):
    pts = [rat(a, b) for a in range(-r, r+1) for b in range(-r, r+1) if abs(a)+abs(b)+abs(a+b) <= 2*r]
    pts += [rat(1,0,0), rat(0,1,0), rat(1,-1,0), rat(1,1,0), rat(2,-1,0), rat(1,-2,0)]
    return pts

def cusp_points(m):
    pts = [rat(t, t**3) for t in range(-m, m+1)]
    return pts

def all_pools(rng=None, big=False):
    pools = []
    for N, ts in ((9, [2, 3, Fr(1,2), -1, Fr(3,2)]), (10, [2, 3, Fr(1,2), Fr(3,2)]), (12, [2, 3, Fr(3,2), Fr(1,3)]), (8, [2, 3, Fr(1,3)]), (7, [2, 3])):
        for t in ts:
            try:
                tp = torsion_points(N, t)
            except ZeroDivisionError:
                tp = None
            if tp is None: continue
            pools.append(Pool(tp, f"E{N}_t{t}"))
            pools.append(Pool(with_intersections(tp, 0, maxadd=60, minrich=3, rng=rng), f"E{N}_t{t}+X"))
            break
    for m in (5, 6, 8, 10, 12, 3, 4):
        d, pts = polygon_pool_points(m)
        pools.append(Pool(pts, f"poly{m}", d))
        if m in (5, 6, 8):
            pools.append(Pool(with_intersections(pts, d, maxadd=40, minrich=3, rng=rng), f"poly{m}+X", d))
    pools.append(Pool(grid_points(3), "grid3"))
    pools.append(Pool(grid_points(4), "grid4"))
    pools.append(Pool(grid_points(5, 3), "grid5"))
    pools.append(Pool(tri_lattice(2), "tri2"))
    pools.append(Pool(tri_lattice(3), "tri3"))
    pools.append(Pool(cusp_points(5), "cusp5"))
    pools.append(Pool(with_intersections(cusp_points(4), 0, maxadd=40, rng=rng), "cusp4+X"))
    return pools

if __name__ == "__main__":
    import random
    for N in (7, 8, 9, 10, 12):
        for t in (2, 3, Fr(1,2), Fr(3,2), Fr(1,3), -1):
            try: tp = torsion_points(N, t)
            except ZeroDivisionError: tp = None
            print(N, t, "ok" if tp else "fail", Pool(tp, "x").rich() if tp else "")
            if tp: break
    for m in (5, 8, 10, 12, 6):
        d, pts = polygon_pool_points(m)
        P = Pool(pts, "p", d)
        print("poly", m, len(P.pts), P.rich()[:12])
