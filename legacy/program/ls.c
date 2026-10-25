/*
 * ls.c — exhaustive search for linear spaces (= combinatorial "pencil configurations")
 *
 * Dual picture: n points (= the n lines of the original problem); "blocks" = lines
 * through >=3 of the points (= pencils of >=3 original lines). Every pair of points
 * lies on exactly one line; pairs not covered by a big block are 2-point lines
 * (= ordinary intersection points).
 *
 * Input lines on stdin:   n mode seconds k1 k2 ... km      (k_i >= 3, the pencil sizes)
 *   mode 0: does ANY linear space with these pencils exist?   (combinatorial filter)
 *   mode 1: does an ORIENTABLE one exist?  (orientable = admits a chirotope; every real
 *           line arrangement gives one, so "no" proves real non-realizability)
 *   mode 2: like 1, but count all labelled spaces found and how many are orientable
 * Output: one line per query:  YES|NO|TIMEOUT [count info] [blocks of an example]
 *
 * Search: always cover the lexicographically smallest uncovered pair {p,q}: either it is a
 * 2-point line, or it starts a block of a still-needed size k with k-2 further points.
 * Symmetry: points with no decided pair are interchangeable -> they are used in increasing
 * order. Pruning (modes 1,2): when all pairs through points 0..P-1 are decided, all triples
 * containing such a point are known (collinear or not); the 3-term Grassmann-Pluecker
 * relations centred at those points must be satisfiable — checked with a small XOR+NAE solver.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 16
#define MAXT 560          /* C(16,3) */
#define W 9               /* 64-bit words for MAXT bits */
#define MAXL 200

typedef struct { uint64_t b[W]; } bs;

static int n, mode;
static int cnt[MAXN + 1], t2rem;
static int pl[MAXN][MAXN];
static uint32_t lmask[MAXL];
static int nlines;
static int touched[MAXN];
static int tri[MAXN][MAXN][MAXN];
static int ntri;
static long long nodes, leaves, orientable_leaves;
static double deadline;
static int timed_out;
static int found;
static uint32_t best_lines[MAXL]; static int best_nlines;

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }

static inline void bs_clear(bs *x) { memset(x, 0, sizeof(bs)); }
static inline void bs_set(bs *x, int i) { x->b[i >> 6] |= 1ULL << (i & 63); }
static inline int bs_get(const bs *x, int i) { return (x->b[i >> 6] >> (i & 63)) & 1; }
static int NW = W;
static inline void bs_xor(bs *x, const bs *y) { for (int i = 0; i < NW; i++) x->b[i] ^= y->b[i]; }
static inline int bs_zero(const bs *x) { for (int i = 0; i < NW; i++) if (x->b[i]) return 0; return 1; }
static inline int bs_par_and(const bs *x, const bs *y) { uint64_t s = 0; for (int i = 0; i < NW; i++) s ^= x->b[i] & y->b[i]; return __builtin_parityll(s); }
static inline int bs_andnot_zero(const bs *x, const bs *y) { for (int i = 0; i < NW; i++) if (x->b[i] & ~y->b[i]) return 0; return 1; }

/* ---------------- chirotope solver ---------------- */
/* status of triple (sorted a<b<c): -1 undecided, 0 collinear, 1 non-collinear */
static int tri_status(int a, int b, int c) {
    int l = pl[a][b];
    if (l < 0) l = pl[a][c];
    if (l < 0) l = pl[b][c];
    if (l < 0) return -1;
    uint32_t m = lmask[l];
    return ((m >> a) & 1) && ((m >> b) & 1) && ((m >> c) & 1) ? 0 : 1;
}

static int parity3(int a, int b, int c) { int p = 0; if (a > b) p ^= 1; if (a > c) p ^= 1; if (b > c) p ^= 1; return p; }
static void sort3(int *a, int *b, int *c) { int t; if (*a > *b) { t = *a; *a = *b; *b = t; } if (*b > *c) { t = *b; *b = *c; *c = t; } if (*a > *b) { t = *a; *a = *b; *b = t; } }

/* chi(a,b,c): returns -1 if zero, else var index; *par gets permutation parity */
static int chi(int a, int b, int c, int *par) {
    int x = a, y = b, z = c; sort3(&x, &y, &z);
    int s = tri_status(x, y, z);
    if (s < 0) { fprintf(stderr, "undecided triple used\n"); exit(1); }
    if (s == 0) return -1;
    *par = parity3(a, b, c);
    return tri[x][y][z];
}

#define MAXROWS 30000
#define MAXNAE 60000
static bs rows[MAXROWS]; static int rowc[MAXROWS]; static int nrows;
static int nae_v[MAXNAE][3][2]; static int nae_c[MAXNAE][3]; static int nnae;

/* after elimination */
static int pivot_of_var[MAXT];   /* row index or -1 */
static int free_idx[MAXT];       /* var -> free position or -1 */
static int nfree;
static bs vform[MAXT]; static int vconst[MAXT];
static bs fform[MAXNAE][3]; static int fconst[MAXNAE][3];
static int nf;
static int *occ[MAXT]; static int occn[MAXT], occcap[MAXT];
static bs asg, val;
static int order_[MAXT];
static long long sat_nodes, n_checks, n_checks_fail; static double t_check;

static int add_row(bs *r, int c) {
    if (nrows >= MAXROWS) { fprintf(stderr, "too many rows\n"); exit(1); }
    rows[nrows] = *r; rowc[nrows] = c; nrows++; return 0;
}

static inline int evalf(int i, int j) { /* -1 unknown */
    if (!bs_andnot_zero(&fform[i][j], &asg)) return -1;
    return bs_par_and(&fform[i][j], &val) ^ fconst[i][j];
}

static int stackv[MAXT * 4];
static int propagate(int sp) {
    while (sp > 0) {
        int v = stackv[--sp];
        for (int t = 0; t < occn[v]; t++) {
            int i = occ[v][t];
            int e0 = evalf(i, 0), e1 = evalf(i, 1), e2 = evalf(i, 2);
            int e[3] = {e0, e1, e2};
            int unk = (e0 < 0) + (e1 < 0) + (e2 < 0);
            if (unk == 0) { if (e0 == e1 && e1 == e2) return 0; }
            else if (unk == 1) {
                int u = e0 < 0 ? 0 : (e1 < 0 ? 1 : 2);
                int k1 = (u + 1) % 3, k2 = (u + 2) % 3;
                if (e[k1] == e[k2]) {
                    /* count unknown vars of form u */
                    int w = -1, many = 0;
                    for (int q = 0; q < NW && !many; q++) {
                        uint64_t x = fform[i][u].b[q] & ~asg.b[q];
                        while (x) { int bit = __builtin_ctzll(x); x &= x - 1; if (w >= 0) { many = 1; break; } w = q * 64 + bit; }
                    }
                    if (!many && w >= 0) {
                        int need = 1 ^ e[k1];
                        int cur = bs_par_and(&fform[i][u], &val) ^ fconst[i][u]; /* w currently 0 in val */
                        bs_set(&asg, w);
                        if (need ^ cur) bs_set(&val, w);
                        stackv[sp++] = w;
                    }
                }
            }
        }
    }
    return 1;
}

static int dpll(void) {
    sat_nodes++;
    if ((sat_nodes & 1023) == 0 && now() > deadline) { timed_out = 1; return 0; }
    int v = -1;
    for (int t = 0; t < nfree; t++) if (!bs_get(&asg, order_[t])) { v = order_[t]; break; }
    if (v < 0) return 1;
    for (int b = 0; b < 2; b++) {
        bs sa = asg, sv = val;
        bs_set(&asg, v); if (b) bs_set(&val, v);
        stackv[0] = v;
        if (propagate(1) && dpll()) return 1;
        asg = sa; val = sv;
        if (timed_out) return 0;
    }
    return 0;
}

/* Check satisfiability of GP relations with centres in [0,P) (or all if P>=n). */
static int orient_check_(int P);
static int orient_check(int P) { double t = now(); n_checks++; int r = orient_check_(P); if (!r) n_checks_fail++; t_check += now() - t; return r; }
static int orient_check_(int P) {
    nrows = 0; nnae = 0;
    int centres = P >= n ? n : P;
    if (centres < 1) return 1;
    for (int a = 0; a < n; a++) {
        int is_centre = a < centres;
        int oth[MAXN], no = 0;
        for (int x = 0; x < n; x++) if (x != a) oth[no++] = x;
        for (int i1 = 0; i1 < no; i1++) for (int i2 = i1 + 1; i2 < no; i2++)
        for (int i3 = i2 + 1; i3 < no; i3++) for (int i4 = i3 + 1; i4 < no; i4++) {
            int x1 = oth[i1], x2 = oth[i2], x3 = oth[i3], x4 = oth[i4];
            if (!is_centre) {
                int xs[4] = {x1, x2, x3, x4}, dec = 1;
                for (int u = 0; u < 4 && dec; u++) for (int w = u + 1; w < 4; w++) {
                    int A = a, B = xs[u], C = xs[w]; sort3(&A, &B, &C);
                    if (tri_status(A, B, C) < 0) { dec = 0; break; }
                }
                if (!dec) continue;
            }
            int pr[3][5] = {{x1, x2, x3, x4, 0}, {x1, x3, x2, x4, 1}, {x1, x4, x2, x3, 0}};
            int tv[3][2], tc[3], nzc = 0, nzi[3];
            for (int t = 0; t < 3; t++) {
                int p1, p2;
                int u = chi(a, pr[t][0], pr[t][1], &p1);
                int w = chi(a, pr[t][2], pr[t][3], &p2);
                if (u < 0 || w < 0) { tv[t][0] = -1; continue; }
                tv[t][0] = u; tv[t][1] = w; tc[t] = p1 ^ p2 ^ pr[t][4];
                nzi[nzc++] = t;
            }
            if (nzc == 0) continue;
            if (nzc == 1) return 0;  /* impossible in a genuine linear space */
            if (nzc == 2) {
                bs r; bs_clear(&r);
                int s = nzi[0], t = nzi[1];
                r.b[tv[s][0] >> 6] ^= 1ULL << (tv[s][0] & 63);
                r.b[tv[s][1] >> 6] ^= 1ULL << (tv[s][1] & 63);
                r.b[tv[t][0] >> 6] ^= 1ULL << (tv[t][0] & 63);
                r.b[tv[t][1] >> 6] ^= 1ULL << (tv[t][1] & 63);
                add_row(&r, tc[s] ^ tc[t] ^ 1);
            } else {
                if (nnae >= MAXNAE) { fprintf(stderr, "too many nae\n"); exit(1); }
                for (int t = 0; t < 3; t++) { nae_v[nnae][t][0] = tv[t][0]; nae_v[nnae][t][1] = tv[t][1]; nae_c[nnae][t] = tc[t]; }
                nnae++;
            }
        }
    }
    /* normalisation: chi(0,1,c)=+ ; chi(0,1,e)=+ or chi(0,c,e)=+ */
    {
        int c = -1;
        for (int x = 2; x < n; x++) if (tri_status(0, 1, x) == 1) { c = x; break; }
        if (c >= 0) {
            bs r; int p;
            int v = chi(0, 1, c, &p); bs_clear(&r); bs_set(&r, v); add_row(&r, p);
            for (int e = 2; e < n; e++) {
                if (e == c) continue;
                int vv = chi(0, 1, e, &p);
                if (vv < 0) vv = chi(0, c, e, &p);
                bs_clear(&r); bs_set(&r, vv); add_row(&r, p);
            }
        }
    }
    /* Gauss-Jordan */
    for (int v = 0; v < ntri; v++) pivot_of_var[v] = -1;
    int rank = 0;
    for (int v = 0; v < ntri; v++) {
        int sel = -1;
        for (int r = rank; r < nrows; r++) if (bs_get(&rows[r], v)) { sel = r; break; }
        if (sel < 0) continue;
        bs tmp = rows[sel]; rows[sel] = rows[rank]; rows[rank] = tmp;
        int tc = rowc[sel]; rowc[sel] = rowc[rank]; rowc[rank] = tc;
        for (int r = 0; r < nrows; r++) if (r != rank && bs_get(&rows[r], v)) { bs_xor(&rows[r], &rows[rank]); rowc[r] ^= rowc[rank]; }
        pivot_of_var[v] = rank; rank++;
    }
    for (int r = rank; r < nrows; r++) if (rowc[r]) return 0;  /* 0 = 1 */
    nfree = 0;
    for (int v = 0; v < ntri; v++) free_idx[v] = -1;
    for (int v = 0; v < ntri; v++) if (pivot_of_var[v] < 0) free_idx[v] = nfree++;
    if (nfree > MAXT) exit(2);
    for (int v = 0; v < ntri; v++) {
        bs_clear(&vform[v]); vconst[v] = 0;
        if (pivot_of_var[v] < 0) { bs_set(&vform[v], free_idx[v]); continue; }
        int r = pivot_of_var[v];
        vconst[v] = rowc[r];
        for (int w = 0; w < ntri; w++) if (w != v && bs_get(&rows[r], w)) {
            if (free_idx[w] < 0) { fprintf(stderr, "not reduced\n"); exit(1); }
            bs_set(&vform[v], free_idx[w]);
        }
    }
    nf = 0;
    for (int i = 0; i < nnae; i++) {
        int allconst = 1;
        for (int t = 0; t < 3; t++) {
            bs f = vform[nae_v[i][t][0]]; bs_xor(&f, &vform[nae_v[i][t][1]]);
            fform[nf][t] = f; fconst[nf][t] = nae_c[i][t] ^ vconst[nae_v[i][t][0]] ^ vconst[nae_v[i][t][1]];
            if (!bs_zero(&f)) allconst = 0;
        }
        if (allconst) { if (fconst[nf][0] == fconst[nf][1] && fconst[nf][1] == fconst[nf][2]) return 0; continue; }
        nf++;
    }
    for (int v = 0; v < nfree; v++) occn[v] = 0;
    for (int i = 0; i < nf; i++) {
        bs u; bs_clear(&u);
        for (int t = 0; t < 3; t++) for (int q = 0; q < NW; q++) u.b[q] |= fform[i][t].b[q];
        for (int q = 0; q < NW; q++) { uint64_t x = u.b[q]; while (x) { int bit = __builtin_ctzll(x); x &= x - 1; int v = q * 64 + bit;
            if (occn[v] >= occcap[v]) { occcap[v] = occcap[v] ? occcap[v] * 2 : 64; occ[v] = realloc(occ[v], sizeof(int) * occcap[v]); }
            occ[v][occn[v]++] = i; } }
    }
    for (int v = 0; v < nfree; v++) order_[v] = v;
    /* sort by occurrence desc (simple insertion sort) */
    for (int i = 1; i < nfree; i++) { int x = order_[i], j = i - 1; while (j >= 0 && occn[order_[j]] < occn[x]) { order_[j + 1] = order_[j]; j--; } order_[j + 1] = x; }
    bs_clear(&asg); bs_clear(&val);
    return dpll();
}

/* ---------------- linear space search ---------------- */
static int stop_search;

static void record(void) { best_nlines = nlines; memcpy(best_lines, lmask, sizeof(uint32_t) * nlines); }

static void add_line(uint32_t m) {
    int id = nlines++;
    lmask[id] = m;
    for (int a = 0; a < n; a++) if ((m >> a) & 1) for (int b = 0; b < n; b++) if (b != a && ((m >> b) & 1)) { pl[a][b] = id; }
    for (int a = 0; a < n; a++) if ((m >> a) & 1) touched[a] += __builtin_popcount(m) - 1;
}
static void remove_line(void) {
    int id = --nlines; uint32_t m = lmask[id];
    for (int a = 0; a < n; a++) if ((m >> a) & 1) for (int b = 0; b < n; b++) if (b != a && ((m >> b) & 1)) pl[a][b] = -1;
    for (int a = 0; a < n; a++) if ((m >> a) & 1) touched[a] -= __builtin_popcount(m) - 1;
}

static void search(int lastP);

static void choose(int k, int p, int q, int start, int lastP, int nur0, int *U, int nU, int *blk, int bk) {
    if (stop_search) return;
    if (bk == k) {
        uint32_t m = 0; for (int i = 0; i < k; i++) m |= 1u << blk[i];
        cnt[k]--; add_line(m);
        search(lastP);
        remove_line(); cnt[k]++;
        return;
    }
    int need = k - bk;
    for (int r = start; r <= n - need; r++) {
        if (pl[p][r] >= 0 || pl[q][r] >= 0) continue;
        int ok = 1;
        for (int i = 2; i < bk; i++) if (pl[blk[i]][r] >= 0) { ok = 0; break; }
        if (!ok) continue;
        int nur = nur0;
        if (touched[r] == 0) {
            /* r must be the next untouched point in increasing order */
            if (nur >= nU || U[nur] != r) continue;
            nur++;
        }
        blk[bk] = r;
        choose(k, p, q, r + 1, lastP, nur, U, nU, blk, bk + 1);
        if (stop_search) return;
    }
}

static void search(int lastP) {
    if (stop_search) return;
    nodes++;
    if ((nodes & 4095) == 0 && now() > deadline) { timed_out = 1; stop_search = 1; return; }
    int p = -1, q = -1;
    for (int a = 0; a < n && p < 0; a++) for (int b = a + 1; b < n; b++) if (pl[a][b] < 0) { p = a; q = b; break; }
    if (p < 0) {
        leaves++;
        if (mode == 0) { found = 1; record(); stop_search = 1; return; }
        if (mode == 3) { if (!found) record(); found = 1; return; }
        if (mode == 4) { if (orient_check(n)) { orientable_leaves++; if (!found) record(); found = 1; stop_search = 1; } return; }
        int ok = orient_check(n);
        if (timed_out) { stop_search = 1; return; }
        if (ok) {
            orientable_leaves++;
            if (!found) record();
            found = 1;
            if (mode == 1) stop_search = 1;
        }
        return;
    }
    if ((mode == 1 || mode == 2) && p > lastP && p >= 2) {
        if (!orient_check(p)) { if (timed_out) stop_search = 1; return; }
        if (timed_out) { stop_search = 1; return; }
    }
    /* quick feasibility: remaining pairs must equal budget (always true) ; per-point check */
    int kmax = 0; for (int k = n; k >= 3; k--) if (cnt[k] > 0) { kmax = k; break; }
    int at_root = (nlines == 0);
    /* Option A: 2-point line */
    if (t2rem > 0 && !(at_root && kmax > 0)) {
        t2rem--; add_line((1u << p) | (1u << q));
        search(p > lastP ? p : lastP);
        remove_line(); t2rem++;
        if (stop_search) return;
    }
    /* Option B: block of size k */
    int U[MAXN], nU = 0;
    for (int x = 0; x < n; x++) if (touched[x] == 0 && x != p && x != q) U[nU++] = x;
    for (int k = n; k >= 3; k--) {
        if (cnt[k] <= 0) continue;
        if (at_root && k != kmax) continue;
        int blk[MAXN]; blk[0] = p; blk[1] = q;
        choose(k, p, q, q + 1, p > lastP ? p : lastP, 0, U, nU, blk, 2);
        if (stop_search) return;
    }
}

int main(void) {
    ntri = 0;
    for (int a = 0; a < MAXN; a++) for (int b = a + 1; b < MAXN; b++) for (int c = b + 1; c < MAXN; c++) tri[a][b][c] = -1;
    char line[4096];
    while (fgets(line, sizeof line, stdin)) {
        int ks[200], m = 0; double secs;
        char *s = line; int off;
        if (sscanf(s, "%d %d %lf%n", &n, &mode, &secs, &off) < 3) continue;
        s += off;
        while (sscanf(s, "%d%n", &ks[m], &off) == 1) { m++; s += off; }
        ntri = 0;
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) tri[a][b][c] = ntri++;
        NW = (ntri + 63) / 64;
        memset(cnt, 0, sizeof cnt);
        int pairs = n * (n - 1) / 2, used = 0, bad = 0;
        for (int i = 0; i < m; i++) { if (ks[i] < 3 || ks[i] > n) bad = 1; else { cnt[ks[i]]++; used += ks[i] * (ks[i] - 1) / 2; } }
        if (bad || used > pairs) { printf("NO arithmetic\n"); fflush(stdout); continue; }
        t2rem = pairs - used;
        for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) pl[a][b] = -1;
        memset(touched, 0, sizeof touched);
        nlines = 0; nodes = leaves = orientable_leaves = 0; n_checks = n_checks_fail = 0; t_check = 0; timed_out = 0; found = 0; stop_search = 0; sat_nodes = 0;
        deadline = now() + secs;
        if (n <= 2) { printf("YES\n"); fflush(stdout); continue; }
        search(-1);
        if (timed_out) printf("TIMEOUT");
        else printf(found ? "YES" : "NO");
        printf(" nodes=%lld leaves=%lld orientable=%lld checks=%lld fails=%lld tcheck=%.1f satnodes=%lld", nodes, leaves, orientable_leaves, n_checks, n_checks_fail, t_check, sat_nodes);
        if (found) {
            printf(" |");
            for (int i = 0; i < best_nlines; i++) if (__builtin_popcount(best_lines[i]) >= 3) {
                printf(" ");
                int first = 1;
                for (int a = 0; a < n; a++) if ((best_lines[i] >> a) & 1) { printf(first ? "%d" : ",%d", a); first = 0; }
            }
        }
        printf("\n"); fflush(stdout);
    }
    return 0;
}
