"""Lower bounds for the number of intersection points f_0 of an arrangement of n lines
whose maximal multiplicity (largest pencil) is m <= n-3.  Used in notes/points.md.

Three bounds are combined; each is proved in notes/points.md.

(S)  Spoke bound.  Let P be a point of multiplicity m, b = n - m the lines not through P.
     Every line not through P meets the m lines through P in m distinct points.  Counting
     the distinct points on the m lines through P other than P ("spokes") gives
         f_0 >= 1 + G(n, b),
     where G(n, b) = min sum_{i=1..m} g_i over integer g_i with
         sum_i c(g_i) <= C(b, 2),   c(g) = min { sum_j C(s_j, 2) : s_1+..+s_g = b, 1 <= s_j <= m-1 }.
     (g_i = number of distinct points on the i-th line through P other than P; the lines
     through such a point partition the b lines into g_i classes of size <= m-1; each class
     of size s uses C(s,2) of the C(b,2) pairs of the b lines, and every pair is used at most once.)
     The weaker closed form is Kelly-Moser's  f_0 >= 1 + m b - C(b, 2).

(M)  Melchior bound.  Melchior's inequality t_2 >= 3 + sum_{k>=4} (k-3) t_k, together with
     sum_k C(k,2) t_k = C(n,2) and t_k = 0 for k > m, gives
         f_0 >= (n(n-1) + 3m + 3) / (m + 3).

(H)  LP bound with Hirzebruch.  For m <= n-3 Hirzebruch's inequality
     t_2 + (3/4) t_3 >= n + sum_{k>=5} (k-4) t_k holds (complex arrangements with
     t_n = t_{n-1} = t_{n-2} = 0).  Minimising f_0 = sum t_k subject to the pair count,
     Melchior, Hirzebruch, t_m >= 1 and t_k >= 0 is a small linear program; its optimum is a
     valid lower bound.  The script extracts an exact rational dual certificate
     (non-negative multipliers) and re-verifies it with Fractions, so the bound is a proof.

usage: python scripts/f0_bounds.py [NMAX]      prints, for each n, the smallest f_0 the bounds allow
                                               when m <= n-3, and the certificates used.
"""
import sys
from fractions import Fraction as Fr
from math import comb, ceil


def c_min_pairs(b, g, m):
    """min sum C(s_j,2) over partitions of b into g parts, each in [1, m-1]; None if impossible."""
    if g > b or g * (m - 1) < b:
        return None
    q, r = divmod(b, g)
    return r * comb(q + 1, 2) + (g - r) * comb(q, 2)


def spoke_bound(n, m):
    """1 + G(n, b) with b = n - m  (dynamic programme over the m lines through P)."""
    b = n - m
    budget = comb(b, 2)
    opts = [(g, c_min_pairs(b, g, m)) for g in range(1, b + 1)]
    opts = [(g, c) for g, c in opts if c is not None]
    cur = {0: 0}
    for _ in range(m):
        nxt = {}
        for c0, s0 in cur.items():
            for g, c in opts:
                c1 = c0 + c
                if c1 <= budget and nxt.get(c1, 10 ** 9) > s0 + g:
                    nxt[c1] = s0 + g
        cur = nxt
    return 1 + min(cur.values())


def melchior_bound(n, m):
    return ceil(Fr(n * (n - 1) + 3 * m + 3, m + 3))


def lp_bound(n, m, use_hirzebruch=True):
    """Exact LP lower bound on f_0 with a verified dual certificate.

    Primal (variables t_2..t_m >= 0):
        minimise  sum t_k
        s.t.  sum C(k,2) t_k = C(n,2)                               (pairs)
              t_2 - sum_{k>=4} (k-3) t_k >= 3                       (Melchior)
              t_2 + 3/4 t_3 - sum_{k>=5} (k-4) t_k >= n             (Hirzebruch, needs m <= n-3)
              t_m >= 1                                              (a point of multiplicity m exists)
    Returns (bound, certificate) where certificate = (alpha, beta, gamma, delta) are multipliers
    (alpha free, the others >= 0) with  sum t_k >= alpha*C(n,2) + 3*beta + n*gamma + delta  for every
    feasible t, verified coefficientwise with exact arithmetic.
    """
    import numpy as np
    from scipy.optimize import linprog
    ks = list(range(2, m + 1))
    pairs = [comb(k, 2) for k in ks]
    mel = [1 if k == 2 else -(k - 3) if k >= 4 else 0 for k in ks]
    hir = [1 if k == 2 else Fr(3, 4) if k == 3 else -(k - 4) if k >= 5 else 0 for k in ks]
    tm = [1 if k == m else 0 for k in ks]
    rows = [mel, tm] + ([hir] if use_hirzebruch else [])
    rhs = [3, 1] + ([n] if use_hirzebruch else [])
    # solve the dual numerically: max alpha*C(n,2) + sum rhs_i y_i  s.t. alpha*pairs_k + sum y_i rows_i,k <= 1, y >= 0
    A_ub = []; b_ub = []
    for j, k in enumerate(ks):
        A_ub.append([pairs[j]] + [float(r[j]) for r in rows]); b_ub.append(1.0)
    c = [-comb(n, 2)] + [-float(x) for x in rhs]
    bounds = [(None, None)] + [(0, None)] * len(rows)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    assert res.success
    y = [Fr(v).limit_denominator(10 ** 6) for v in res.x]
    # exact verification of the dual certificate
    for j, k in enumerate(ks):
        lhs = y[0] * pairs[j] + sum(y[i + 1] * rows[i][j] for i in range(len(rows)))
        assert lhs <= 1, (n, m, k, lhs)
    assert all(v >= 0 for v in y[1:])
    value = y[0] * comb(n, 2) + sum(y[i + 1] * rhs[i] for i in range(len(rows)))
    return ceil(value), value, y


def best_bound(n, m, verbose=False):
    s = spoke_bound(n, m); mb = melchior_bound(n, m)
    out = {"spoke": s, "melchior": mb}
    if m <= n - 3:
        lp, val, cert = lp_bound(n, m)
        out["lp_hirzebruch"] = lp; out["lp_value"] = val; out["lp_cert"] = cert
    return out


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    for n in range(8, nmax + 1):
        worst = None
        for m in range(3, n - 2):          # m <= n-3
            bb = best_bound(n, m)
            lb = max(bb["spoke"], bb["melchior"], bb.get("lp_hirzebruch", 0))
            if worst is None or lb < worst[0]:
                worst = (lb, m, bb)
        lb, m, bb = worst
        flag = "" if lb >= 2 * n - 2 else "   <-- not enough for 2n-2"
        print(f"n={n}: min over m<=n-3 of the bound = {lb} (at m={m}; spoke {bb['spoke']}, melchior {bb['melchior']}, "
              f"LP+Hirzebruch {bb.get('lp_hirzebruch')}); 2n-2 = {2*n-2}{flag}")


def table(n_lo, n_hi):
    """Markdown table: for each n and each m <= n-3, the bounds and which one reaches 2n-2."""
    rows = ["| n | m | spoke | Melchior | LP (Melchior+Hirzebruch) | best | 2n-2 | LP certificate (alpha; beta_Mel, delta_tm, gamma_Hir) |", "|---|---|---|---|---|---|---|---|"]
    for n in range(n_lo, n_hi + 1):
        for m in range(3, n - 2):
            bb = best_bound(n, m)
            best = max(bb["spoke"], bb["melchior"], bb["lp_hirzebruch"])
            need_lp = best >= 2 * n - 2 and max(bb["spoke"], bb["melchior"]) < 2 * n - 2
            cert = ", ".join(str(x) for x in bb["lp_cert"]) if need_lp else ""
            rows.append(f"| {n} | {m} | {bb['spoke']} | {bb['melchior']} | {bb['lp_hirzebruch']} | {best} | {2*n-2} | {cert} |")
    return "\n".join(rows)


def check_range(n_lo, n_hi):
    """True iff spoke+Melchior alone give f_0 >= 2n-2 for all m <= n-3 and all n in range."""
    bad = []
    for n in range(n_lo, n_hi + 1):
        for m in range(3, n - 2):
            if max(spoke_bound(n, m), melchior_bound(n, m)) < 2 * n - 2:
                bad.append((n, m))
    return bad
