# Orientability test for a simple rank-3 matroid (= linear space on n "points").
# A real realization gives a chirotope chi(a,b,c)=sign det, so NON-orientable => NOT realizable over R.
# We search for a chirotope satisfying the 3-term Grassmann-Pluecker relations
# (Bjorner-Las Vergnas-Sturmfels-White-Ziegler, Thm 3.6.2): for every a and x1..x4,
#  { chi(a x1 x2)chi(a x3 x4), -chi(a x1 x3)chi(a x2 x4), chi(a x1 x4)chi(a x2 x3) }
# either contains both +1 and -1, or is {0}.
from itertools import combinations
import sys

def perm_parity(t):
    # parity of permutation sorting t (len 3)
    a,b,c = t; p = 0
    if a>b: p^=1
    if a>c: p^=1
    if b>c: p^=1
    return p

def orientable(n, blocks, want=False, limit=None):
    """blocks: lines with >=3 points (2-point lines implicit). Returns (bool, chirotope or None)."""
    col = set()
    for B in blocks:
        for t in combinations(sorted(B),3): col.add(t)
    var = {}
    for t in combinations(range(n),3):
        if t not in col: var[t] = len(var)
    N = len(var)
    def chi(a,b,c):
        t = tuple(sorted((a,b,c)))
        if t in col: return None
        return (var[t], perm_parity((a,b,c)))
    # affine forms over GF(2): (mask, const). start: each var is free
    # Collect constraints
    xors = []   # (mask, const) meaning parity(mask&x) == const
    naes = []   # list of 3 (mask,const) terms, not all equal
    for a in range(n):
        others = [x for x in range(n) if x!=a]
        for x1,x2,x3,x4 in combinations(others,4):
            terms = []
            for (p,q,r,s,neg) in ((x1,x2,x3,x4,0),(x1,x3,x2,x4,1),(x1,x4,x2,x3,0)):
                u = chi(a,p,q); w = chi(a,r,s)
                if u is None or w is None: terms.append(None); continue
                terms.append(((1<<u[0]) ^ (1<<w[0]), u[1]^w[1]^neg))
            nz = [t for t in terms if t is not None]
            if len(nz) == 0: continue
            if len(nz) == 1: return (False, "single nonzero GP term: not a matroid?")
            if len(nz) == 2:
                (m1,c1),(m2,c2) = nz
                xors.append((m1^m2, c1^c2^1))
            else:
                naes.append(nz)
    # normalization (WLOG by reorientation + global sign)
    basis = None
    for t in combinations(range(n),3):
        if t not in col: basis = t; break
    a,b,c = basis
    fix = [(var[basis], 0)]
    for e in range(n):
        if e in basis: continue
        u = chi(a,b,e)
        if u is None: u = chi(a,c,e)
        fix.append((u[0], u[1]))   # chi(...) = + means var parity == perm parity
    for v,p in fix: xors.append((1<<v, p))
    # Gaussian elimination
    pivots = {}  # pivot var -> (mask, const) row with that pivot as lowest... use dict elimination
    rows = []
    for m,cst in xors:
        for pv,(pm,pc) in pivots.items():
            if m>>pv & 1: m ^= pm; cst ^= pc
        if m == 0:
            if cst: return (False, None)   # inconsistent linear system
            continue
        pv = m.bit_length()-1
        # eliminate pv from existing rows
        for q,(qm,qc) in list(pivots.items()):
            if qm>>pv & 1: pivots[q] = (qm^m, qc^cst)
        pivots[pv] = (m,cst)
    # express each variable as affine form of free vars
    free = [v for v in range(N) if v not in pivots]
    fidx = {v:i for i,v in enumerate(free)}
    def form_of_var(v):
        if v in pivots:
            m,cst = pivots[v]
            m2 = 0
            mm = m & ~(1<<v)
            while mm:
                low = mm & -mm; w = low.bit_length()-1; mm ^= low
                m2 |= 1<<fidx[w]
            return (m2, cst)
        return (1<<fidx[v], 0)
    vf = [form_of_var(v) for v in range(N)]
    def conv(m,cst):
        r=0; mm=m
        while mm:
            low = mm & -mm; w = low.bit_length()-1; mm ^= low
            fm,fc = vf[w]; r ^= fm; cst ^= fc
        return (r,cst)
    cons = []
    for nz in naes:
        cs = [conv(m,c) for m,c in nz]
        # constant check
        if all(m==0 for m,_ in cs):
            if cs[0][1]==cs[1][1]==cs[2][1]: return (False, None)
            continue
        cons.append(cs)
    F = len(free)
    # DPLL over free vars with propagation
    # index constraints by var
    occ = [[] for _ in range(F)]
    for i,cs in enumerate(cons):
        allm = cs[0][0]|cs[1][0]|cs[2][0]
        mm = allm
        while mm:
            low = mm & -mm; occ[low.bit_length()-1].append(i); mm ^= low
    assigned = 0; val = 0
    nodes = [0]
    def ev(form, assigned, val):
        m,c = form
        if m & ~assigned: return None
        return (bin(m & val).count("1") & 1) ^ c
    def propagate(assigned, val, stack):
        while stack:
            v = stack.pop()
            for i in occ[v]:
                cs = cons[i]
                vals = [ev(f,assigned,val) for f in cs]
                unk = [j for j in range(3) if vals[j] is None]
                if not unk:
                    if vals[0]==vals[1]==vals[2]: return None
                elif len(unk)==1:
                    k = [j for j in range(3) if j!=unk[0]]
                    if vals[k[0]]==vals[k[1]]:
                        m,c = cs[unk[0]]
                        rest = m & ~assigned
                        if rest & (rest-1) == 0:  # single unknown var -> forced
                            w = rest.bit_length()-1
                            need = 1 ^ vals[k[0]]   # must differ
                            cur = (bin(m & val & assigned).count("1") & 1) ^ c
                            bitv = need ^ cur
                            assigned |= 1<<w
                            if bitv: val |= 1<<w
                            stack.append(w)
        return (assigned, val)
    order = sorted(range(F), key=lambda v: -len(occ[v]))
    def dpll(assigned, val):
        nodes[0]+=1
        if limit and nodes[0]>limit: raise TimeoutError
        # pick unassigned var
        for v in order:
            if not (assigned>>v & 1): break
        else:
            return (assigned, val)
        for b in (0,1):
            a2 = assigned | (1<<v); v2 = val | (b<<v)
            r = propagate(a2, v2, [v])
            if r is None: continue
            res = dpll(*r)
            if res: return res
        return None
    # initial check of fully-determined constraints (those with no free vars handled above)
    res = dpll(0,0)
    if res is None: return (False, None)
    if not want: return (True, None)
    assigned, val = res
    chis = {}
    for t,v in var.items():
        m,c = vf[v]
        chis[t] = (bin(m & val).count("1")&1) ^ c
    return (True, chis)

if __name__ == "__main__":
    fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    print("Fano", orientable(7,fano)[0])
    # Moebius-Kantor 8_3: points Z8, lines {i, i+1, i+3}
    mk = [tuple(sorted({i%8,(i+1)%8,(i+3)%8})) for i in range(8)]
    print("MK", orientable(8,mk)[0])
    # Pappus: points 0..8
    pappus = [(0,1,2),(3,4,5),(6,7,8),(0,4,8),(0,5,7),(1,3,8),(1,5,6),(2,3,7),(2,4,6)]
    # check linear space
    print("Pappus", orientable(9,pappus)[0])
    # AG(2,3)
    pts = [(x,y) for x in range(3) for y in range(3)]
    idx = {p:i for i,p in enumerate(pts)}
    lines=set()
    for p in pts:
        for d in [(1,0),(0,1),(1,1),(1,2)]:
            L = tuple(sorted(idx[((p[0]+k*d[0])%3,(p[1]+k*d[1])%3)] for k in range(3)))
            lines.add(L)
    print("AG(2,3)", len(lines), orientable(9,sorted(lines))[0])
    # 3x3 grid real: rows, cols, 2 diagonals
    g = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    print("grid", orientable(9,g)[0])
    # non-Pappus: Pappus minus the line (6,7,8)
    print("non-Pappus", orientable(9,[l for l in pappus if l!=(6,7,8)])[0])
