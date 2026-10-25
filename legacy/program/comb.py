# Combinatorial feasibility: can blocks of given sizes (>=3) be packed on n points
# so that any two blocks share at most one point?  (= partial linear space; the
# remaining pairs become 2-point lines).  Exhaustive backtracking with symmetry breaking.
import sys
from math import comb
sys.setrecursionlimit(10000)

def feasible(n, sizes, want_solution=False, node_limit=None):
    sizes = sorted(sizes, reverse=True)
    m = len(sizes)
    if sum(comb(k,2) for k in sizes) > comb(n,2): return (False, None)
    if m == 0: return (True, [])
    if sizes[0] > n: return (False, None)
    paired = [0]*n          # bitmask of partners already sharing a block
    cap = [n-1]*n
    blocks = []
    nodes = [0]
    # blocks of equal size placed in lexicographic order of their sorted tuples
    def slots_ok(idx):
        need = sum(sizes[idx:])
        have = sum(c//2 for c in cap)
        return need <= have
    def place(idx, prev_same):
        nodes[0] += 1
        if node_limit and nodes[0] > node_limit: raise TimeoutError
        if idx == m: return True
        if not slots_ok(idx): return False
        k = sizes[idx]
        # build block element by element, increasing order
        cur = []
        lower = prev_same  # tuple of previous block of same size or None
        def build(start, mask):
            if len(cur) == k:
                t = tuple(cur)
                if lower is not None and t <= lower: return False
                for a in cur:
                    paired[a] |= mask & ~(1<<a); cap[a] -= (k-1)
                blocks.append(t)
                ok = place(idx+1, t if idx+1 < m and sizes[idx+1]==k else None)
                if ok: return True
                blocks.pop()
                for a in cur:
                    paired[a] &= ~(mask & ~(1<<a)); cap[a] += (k-1)
                return False
            need = k - len(cur)
            for p in range(start, n - need + 1):
                if cap[p] < k-1: continue
                if paired[p] & mask: continue
                # lexicographic pruning for first element
                if lower is not None and len(cur)==0 and p < lower[0]: continue
                cur.append(p)
                if build(p+1, mask | (1<<p)): return True
                cur.pop()
                # symmetry: the first block is canonical
                if idx == 0: return False
            return False
        if idx == 0:
            t = tuple(range(k)); mask = (1<<k)-1
            for a in t: paired[a] |= mask & ~(1<<a); cap[a] -= (k-1)
            blocks.append(t)
            return place(1, t if m>1 and sizes[1]==k else None)
        return build(0, 0)
    ok = place(0, None)
    return (ok, [list(b) for b in blocks] if ok else None)

if __name__ == "__main__":
    from cands import candidates
    import time
    for n in range(1, int(sys.argv[1])+1):
        t0=time.time()
        cs = candidates(n)
        good = [c for c in cs if feasible(n, c)[0]]
        print(n, len(cs), len(good), f"{time.time()-t0:.1f}s", flush=True)

def enumerate_all(n, sizes, callback):
    """Call callback(blocks) for every packing (up to the symmetry breaking used above).
    callback returns True to stop."""
    sizes = sorted(sizes, reverse=True)
    m = len(sizes)
    if m == 0:
        callback([]); return
    paired = [0]*n; cap = [n-1]*n; blocks = []
    stop = [False]
    def place(idx, prev_same):
        if stop[0]: return
        if idx == m:
            if callback([list(b) for b in blocks]): stop[0] = True
            return
        if sum(sizes[idx:]) > sum(c//2 for c in cap): return
        k = sizes[idx]; cur = []; lower = prev_same
        def build(start, mask):
            if stop[0]: return
            if len(cur) == k:
                t = tuple(cur)
                if lower is not None and t <= lower: return
                for a in cur: paired[a] |= mask & ~(1<<a); cap[a] -= (k-1)
                blocks.append(t)
                place(idx+1, t if idx+1 < m and sizes[idx+1]==k else None)
                blocks.pop()
                for a in cur: paired[a] &= ~(mask & ~(1<<a)); cap[a] += (k-1)
                return
            need = k - len(cur)
            for p in range(start, n-need+1):
                if cap[p] < k-1 or paired[p] & mask: continue
                if lower is not None and len(cur)==0 and p < lower[0]: continue
                cur.append(p); build(p+1, mask|(1<<p)); cur.pop()
        build(0,0)
    k = sizes[0]; t = tuple(range(k)); mask=(1<<k)-1
    if k > n: return
    for a in t: paired[a] |= mask & ~(1<<a); cap[a] -= (k-1)
    blocks.append(t)
    place(1, t if m>1 and sizes[1]==k else None)
