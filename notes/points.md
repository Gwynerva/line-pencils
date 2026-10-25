# How many intersection points can n lines have?

Working notes (stage I). Everything here is about an arrangement $\mathcal A$ of $n$ lines in the real
projective plane (equivalently: $n$ lines in the affine plane, no two parallel; see `notes/setting.md`).
$t_k(\mathcal A)$ is the number of points lying on exactly $k$ lines, $f_0 = \sum_k t_k$ the number of
intersection points, and the *multiplicity* $m(\mathcal A) = \max\{k : t_k > 0\}$ the size of the largest pencil.

Two identities are used throughout:

$$\sum_{k\ge 2} \binom k2\, t_k = \binom n2, \qquad\qquad
f_0 = \binom n2 - \sum_{k\ge 3}\Big(\binom k2 - 1\Big) t_k .$$

The second one says: a pencil of $k$ lines "loses" $\binom k2 - 1$ points compared with general position.
We call $\ell(\mathcal A) = \binom n2 - f_0$ the **loss**. The possible losses of one pencil are
$0, 2, 5, 9, 14, 20, \dots$ ($k = 2, 3, 4, 5, 6, 7, \dots$).

Let $V(n) \subseteq \{1, \dots, \binom n2\}$ be the set of values of $f_0$ over all arrangements of $n$ lines
and $d(n) = |V(n)|$. (This is the dual of Grünbaum's problem on the number of lines determined by $n$
points; Erdős 1972, Salamon–Erdős 1988.)

## 1. The top of the range

**Theorem 1.** For every $n \ge 3$: $\binom n2 - 1 \notin V(n)$ and $\binom n2 - 3 \notin V(n)$, while
$\binom n2, \binom n2 - 2 \in V(n)$, and $\binom n2 - 4 \in V(n)$ for $n \ge 4$.

*Proof.* The loss is a sum of numbers from $\{2, 5, 9, 14, \dots\}$, and $1$ and $3$ are not such sums.
General position gives loss $0$; one triple point (three lines through a point, the rest generic) gives
loss $2$; one quadruple point or two triple points give loss $4$ (for $n \ge 4$). $\square$

(Grünbaum observed this; Erdős 1972 quotes it. Every integer $\ge 4$ is a sum of $2$s and $5$s, which is
why the top of $V(n)$ is a solid block once $n$ is large enough to host the required pencils.)

## 2. The bottom of the range

**Lemma 2 (large pencils).** Let $m = m(\mathcal A)$.
* $m = n$: $f_0 = 1$.
* $m = n-1$: $f_0 = n$.
* $m = n-2$: $f_0 \in \{2n-4,\ 2n-2\}$, and both occur for every $n \ge 4$.

*Proof.* Let $P$ be the point of multiplicity $m$ and call the $n-m$ lines not through $P$ *free*.
A free line meets the $m$ lines through $P$ in $m$ distinct points, none equal to $P$.
For $m = n-1$ this gives $1 + (n-1) = n$ points. For $m = n-2$ let $A, B$ be the free lines:
the points are $P$, the $n-2$ points $A \cap L$, the $n-2$ points $B \cap L$ ($L$ through $P$), and $A \cap B$.
Two points $A\cap L$ and $B \cap L'$ coincide only if $L = L'$ (distinct lines through $P$ meet only at $P \notin A$),
and $A \cap L = B \cap L$ iff $A \cap B \in L$, in which case $A\cap B$ is that same point. So
$f_0 = 1 + 2(n-2) + 1 - 2\,[A\cap B \text{ lies on a line through } P] \in \{2n-2, 2n-4\}$. $\square$

**Lemma 3 (spoke bound).** Let $m = m(\mathcal A) \ge 2$ and $b = n - m$. Then
$$ f_0 \;\ge\; 1 + G(n, b), $$
where $G(n,b)$ is the minimum of $\sum_{i=1}^{m} g_i$ over integers $g_1, \dots, g_m \ge 1$ such that
$\sum_i c(g_i) \le \binom b2$, and $c(g)$ is the least value of $\sum_j \binom{s_j}2$ over all ways of
writing $b = s_1 + \dots + s_g$ with $1 \le s_j \le m - 1$ ($c(g) = \infty$ if no such way exists).
In particular (Kelly–Moser 1958, Lemma 4.1) $f_0 \ge 1 + mb - \binom b2$.

*Proof.* Let $P$ be a point of multiplicity $m$, $L_1, \dots, L_m$ the lines through $P$, and let $g_i$ be the
number of points on $L_i$ other than $P$. These $1 + \sum g_i$ points are distinct ($L_i \cap L_j = \{P\}$),
so $f_0 \ge 1 + \sum_i g_i$. Every free line meets $L_i$ at one of its $g_i$ points, so the $g_i$ points
partition the $b$ free lines into $g_i$ classes; a class of size $s$ is a point of multiplicity $s + 1 \le m$,
so $s \le m-1$, and the $\binom s2$ pairs of free lines in the class meet at that point. Distinct points
account for disjoint sets of pairs, hence $\sum_i \sum_{\text{classes}} \binom s2 \le \binom b2$.
Minimising gives $G(n,b)$. The closed form follows from $\binom s2 \ge s - 1$: $\sum_i (b - g_i) \le \binom b2$. $\square$

**Lemma 4 (Melchior bound).** If $\mathcal A$ is not a pencil and $m = m(\mathcal A)$, then
$$ f_0 \;\ge\; \frac{n(n-1) + 3m + 3}{m + 3}. $$

*Proof.* Melchior's inequality (Melchior 1940/41; valid for every arrangement of real lines that is not a pencil):
$t_2 \ge 3 + \sum_{k \ge 4} (k-3)\, t_k$. Substituting $t_2 = \binom n2 - \sum_{k\ge3} \binom k2 t_k$ gives
$\sum_{k \ge 3} \big(\binom k2 + k - 3\big) t_k \le \binom n2 - 3$. The loss is $\sum_{k\ge3}(\binom k2 - 1)t_k$, and
$$\frac{\binom k2 - 1}{\binom k2 + k - 3} = \frac{(k-2)(k+1)}{(k-2)(k+3)} = \frac{k+1}{k+3}$$
is increasing in $k$, so with $t_k = 0$ for $k > m$:
loss $\le \frac{m+1}{m+3}\big(\binom n2 - 3\big)$, i.e. $f_0 \ge \binom n2 - \frac{m+1}{m+3}(\binom n2 - 3) = \frac{2\binom n2 + 3(m+1)}{m+3}$. $\square$

**Lemma 5 (Hirzebruch bound).** If $m(\mathcal A) \le n - 3$ then
$t_2 + \tfrac34 t_3 \ge n + \sum_{k \ge 5} (k - 4)\, t_k$.

This is (a weakening of) Hirzebruch's inequality for arrangements of $n$ lines in the complex projective plane with
$t_n = t_{n-1} = t_{n-2} = 0$; the standard form has coefficients $2k - 9 \ge k - 4$ (Hirzebruch 1983, §3.1 and
"Remarks added in proof"; see Pokora 2021, Remark 14, and `notes/literature_followup.md`). A real arrangement is a
complex one.

**Theorem 6.** Let $n \ge 13$. If $m(\mathcal A) \le n - 3$ then $f_0(\mathcal A) \ge 2n - 2$. Consequently
$$ V(n) \cap [1, 2n-2] \;=\; \{\,1,\ n,\ 2n-4,\ 2n-2\,\} \qquad (n \ge 13). $$

*Proof.* The second statement follows from the first and Lemma 2. For the first, fix $m \le n-3$ and $b = n - m \ge 3$
and take the largest of the three lower bounds: Lemma 3 ($1 + G(n,b)$), Lemma 4, and the linear-programming bound
$\min \sum_k t_k$ subject to $\sum_k \binom k2 t_k = \binom n2$, Melchior, Lemma 5, $t_k \ge 0$, $t_k = 0$ for $k > m$,
$t_m \ge 1$. All three are computed by `scripts/f0_bounds.py`; for the LP the script extracts an exact rational dual
certificate (non-negative multipliers $\beta, \gamma, \delta$ for Melchior, Hirzebruch, $t_m \ge 1$ and a free $\alpha$
for the pair identity with $\sum_k t_k \ge \alpha\binom n2 + 3\beta + n\gamma + \delta$ coefficientwise) and re-verifies it
in exact arithmetic, so the printed bound is a proof.

* For $n = 13, 14, 15, 16$ the table in §2.1 lists, for every $m \le n-3$, a bound $\ge 2n - 2$.
* For $17 \le n \le 120$ the script checks that Lemmas 3 and 4 alone suffice for every $m \le n - 3$ (`check_range`).
* For $n \ge 36$ an explicit argument: if $b \le (2n-9)/3$ then Kelly–Moser's form of Lemma 3 gives
  $f_0 \ge 1 + mb - \binom b2 \ge 2n-2$, because $1 + (n-b)b - \binom b2 - (2n-2) = n(b-2) - \tfrac{3b^2 - b - 6}{2} \ge 0$
  as soon as $n \ge \tfrac{3b^2 - b - 6}{2(b-2)} = \tfrac32 b + \tfrac52 + \tfrac{4}{2b-4}$, which holds when $n \ge \tfrac32 b + \tfrac92$,
  i.e. when $b \le (2n-9)/3$. If $b > (2n-9)/3$ then $m < (n+9)/3$ and Lemma 4 gives
  $f_0 \ge \frac{n(n-1)}{m+3} > \frac{3n(n-1)}{n+18} \ge 2n-2$, the last inequality being $n^2 - 37n + 36 \ge 0$, true for $n \ge 36$.
  (The overlap $17 \le n \le 120$ between the numerical check and this argument is deliberate.) $\square$

**Corollary 7.** $2n - 3 \in V(n)$ if and only if $n \le 11$.

*Proof.* For $n \ge 13$: Theorem 6. For $n = 12$: $2n-3 = 21$; the three admissible types with $f_0 = 21$ that pass the
combinatorial sieve, $\{4^9\}$, $\{5^2, 4^3, 3^6\}$, $\{5^3, 3^9\}$, are not realizable ($\{4^9\}$: dual Hesse configuration,
`data/exclusions.json`; the other two: no orientable linear space, `runs/orient_12.json`). For $6 \le n \le 11$ certificates
exist (`data/certificates/`): $\{3^5\}$, $\{4^2\}$ ($n = 7$); $\{4, 3^5\}$, $\{5, 3^3\}$ ($n = 8$); $\{4, 3^8\}$, $\{5, 3^6\}$, $\{4^3, 3^3\}$ ($n = 9$);
$\{5, 4, 3^7\}$, $\{4^4, 3^4\}$ ($n = 10$); $\{4^4, 3^8\}$ ($n = 11$); $\{3^3\}$ ($n = 6$, $f_0 = 9$). For $n = 4, 5$ the value $2n - 3$
is $5$ resp. $7$, both excluded by Theorem 1. $\square$

**Remarks.** (i) The part "$f_0 \in \{1, n\}$ or $f_0 \ge 2n-4$" of Theorem 6 is Elliott's theorem (Elliott 1967,
Theorem 3; conjectured by Kelly–Moser 1958, who proved it for $n \ge 27$ and $n = 10$), valid for all $n \ge 10$.
Our Theorem 6 adds the value $2n-3$ to the list of excluded values from $n = 13$ on (Salamon–Erdős 1988 have
$m_4 = 2n-2$ for all sufficiently large $n$ with no explicit threshold); the proof above is self-contained apart
from the classical inequalities of Melchior and Hirzebruch.
(ii) The bounds give more for larger $n$: the minimum over $m \le n-3$ of the best bound is $27 = 2n-1$ for
$n = 14$, $29 = 2n-1$ for $n = 15$, $32 = 2n$ for $n = 16$, $36 = 2n+2$ for $n = 17$. Hence for $n = 17$ the values
$2n-1, 2n, 2n+1$ are **not** in $V(17)$; see §4.

### 2.1 Bound table for $n = 13, \dots, 16$

(Generated by `python -c "import f0_bounds as F; print(F.table(13,16))"` in `scripts/`.)

| n | m | spoke | Melchior | LP (Melchior+Hirzebruch) | best | 2n-2 | LP certificate (alpha; beta_Mel, delta_tm, gamma_Hir) |
|---|---|---|---|---|---|---|---|
| 13 | 3 | 16 | 28 | 28 | 28 | 24 |  |
| 13 | 4 | 13 | 25 | 25 | 25 | 24 |  |
| 13 | 5 | 19 | 22 | 24 | 24 | 24 | 5/24, 7/24, 0, 1/2 |
| 13 | 6 | 24 | 20 | 23 | 24 | 24 |  |
| 13 | 7 | 28 | 18 | 23 | 28 | 24 |  |
| 13 | 8 | 31 | 17 | 22 | 31 | 24 |  |
| 13 | 9 | 31 | 16 | 22 | 31 | 24 |  |
| 13 | 10 | 28 | 15 | 22 | 28 | 24 |  |
| 14 | 3 | 19 | 33 | 33 | 33 | 26 |  |
| 14 | 4 | 17 | 29 | 29 | 29 | 26 |  |
| 14 | 5 | 19 | 25 | 27 | 27 | 26 | 5/24, 7/24, 0, 1/2 |
| 14 | 6 | 24 | 23 | 27 | 27 | 26 | 4/21, 5/21, 0, 4/7 |
| 14 | 7 | 29 | 21 | 26 | 29 | 26 |  |
| 14 | 8 | 34 | 19 | 25 | 34 | 26 |  |
| 14 | 9 | 36 | 18 | 25 | 36 | 26 |  |
| 14 | 10 | 35 | 17 | 24 | 35 | 26 |  |
| 14 | 11 | 31 | 16 | 24 | 31 | 26 |  |
| 15 | 3 | 19 | 37 | 37 | 37 | 28 |  |
| 15 | 4 | 17 | 33 | 33 | 33 | 28 |  |
| 15 | 5 | 20 | 29 | 31 | 31 | 28 |  |
| 15 | 6 | 25 | 26 | 30 | 30 | 28 | 4/21, 5/21, 0, 4/7 |
| 15 | 7 | 29 | 24 | 29 | 29 | 28 |  |
| 15 | 8 | 36 | 22 | 28 | 36 | 28 |  |
| 15 | 9 | 40 | 20 | 28 | 40 | 28 |  |
| 15 | 10 | 41 | 19 | 27 | 41 | 28 |  |
| 15 | 11 | 39 | 18 | 27 | 39 | 28 |  |
| 15 | 12 | 34 | 17 | 26 | 34 | 28 |  |
| 16 | 3 | 22 | 42 | 42 | 42 | 30 |  |
| 16 | 4 | 17 | 37 | 37 | 37 | 30 |  |
| 16 | 5 | 20 | 33 | 34 | 34 | 30 |  |
| 16 | 6 | 26 | 29 | 33 | 33 | 30 | 4/21, 5/21, 0, 4/7 |
| 16 | 7 | 32 | 27 | 32 | 32 | 30 |  |
| 16 | 8 | 37 | 25 | 31 | 37 | 30 |  |
| 16 | 9 | 43 | 23 | 31 | 43 | 30 |  |
| 16 | 10 | 46 | 21 | 30 | 46 | 30 |  |
| 16 | 11 | 46 | 20 | 29 | 46 | 30 |  |
| 16 | 12 | 43 | 19 | 29 | 43 | 30 |  |
| 16 | 13 | 37 | 18 | 28 | 37 | 30 |  |

The LP certificates are read as follows. For $n = 13$, $m = 5$ the multipliers are
$\alpha = 5/24$ (pair identity), $\beta = 7/24$ (Melchior), $\gamma = 1/2$ (Hirzebruch), $\delta = 0$:
for $k = 2, 3, 4, 5$ the coefficient $\alpha\binom k2 + \beta\,\mathrm{mel}_k + \gamma\,\mathrm{hir}_k$
(with $\mathrm{mel} = (1, 0, -1, -2)$, $\mathrm{hir} = (1, \tfrac34, 0, -1)$) equals $1, 1, \tfrac{23}{24}, 1$, all $\le 1$, hence
$$ f_0 = \sum_k t_k \;\ge\; \tfrac{5}{24}\cdot 78 + \tfrac{7}{24}\,(t_2 - t_4 - 2t_5) + \tfrac12\,(t_2 + \tfrac34 t_3 - t_5)
\;\ge\; \tfrac{5}{24}\cdot 78 + \tfrac{7}{24}\cdot 3 + \tfrac12 \cdot 13 = 23.625, $$
so $f_0 \ge 24$. All other rows that need the LP are verified the same way by the script.


## 3. Exact values of $d(n)$ for $n \le 13$

Let $A_n$ be the set of arithmetically admissible types for $n$ lines. For every type $T \in A_n$ with $f_0(T) = v$ we
either have a verified certificate (`data/certificates/n{n}.json`, checked by `verifier/verify.py`) or a proof of
non-realizability (Melchior, Csima–Sawyer, de Bruijn–Erdős, no linear space, no orientable linear space;
`data/results/`). $v \in V(n)$ iff some type with $f_0 = v$ has a certificate.

| n | d(n) | V(n) | missing values and why |
|---|---|---|---|
| 1 | 1 | {0} (no intersection points) | — |
| 2 | 1 | {1} | — |
| 3 | 2 | {1, 3} | 2: loss 1 |
| 4 | 3 | {1, 4, 6} | 2, 3: dBE; 5: loss 1 |
| 5 | 5 | {1, 5, 6, 8, 10} | 2–4: dBE; 7, 9: Theorem 1 |
| 6 | 9 | {1, 6, 7, 8, 9, 10, 11, 13, 15} | 2–5: dBE; 12, 14: Theorem 1 |
| 7 | 13 | {1, 7, 9, 10, …, 17, 19, 21} | 2–6: dBE; 8: computation; 18, 20: Theorem 1 |
| 8 | 18 | {1, 8, 11, 12, …, 24, 26, 28} | 2–7: dBE; 9, 10: computation; 25, 27: Theorem 1 |
| 9 | 24 | {1, 9, 13, 14, …, 32, 34, 36} | 2–8: dBE; 10–12: computation; 33, 35: Theorem 1 |
| 10 | 30 | {1, 10, 16, 17, …, 41, 43, 45} | 2–9: dBE; 11–15: Elliott / computation; 42, 44: Theorem 1 |
| 11 | 38 | {1, 11, 18, 19, …, 51, 53, 55} | 2–10: dBE; 12–17: Elliott / computation; 52, 54: Theorem 1 |
| 12 | 46 | {1, 12, 20, 22, 23, …, 62, 64, 66} | 2–11: dBE; 13–19: Elliott / computation; 21: computation; 63, 65: Theorem 1 |
| 13 | 56 | {1, 13, 22, 24, 25, …, 74, 76, 78} | 2–12: dBE; 14–21: Elliott / Theorem 6; 23: Theorem 6 (also: all 81 types with $f_0=23$ are excluded, 69 by the combinatorial sieve, 12 by Melchior); 75, 77: Theorem 1 |

Here "dBE" is the de Bruijn–Erdős theorem ($f_0 \ge n$ unless $\mathcal A$ is a pencil; de Bruijn–Erdős 1948, dual
form), "computation" refers to the exhaustive classification of all types for that $n$. For $n = 13$ the
*positive* part (56 values attained) rests on the 597 verified certificates in `data/certificates/n13.json`,
which cover exactly the 56 values listed; the negative part uses only theorems plus the exhaustive run
`runs/comb_13_f23.json` (and `runs/sat_13_f23.json` for the two types on which the engine timed out).

So $d(n)$ for $n = 1, \dots, 13$ is
$$ 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56 . $$

## 4. Beyond $n = 13$

For $n = 12, 13$ the set $V(n)$ is $\{1, n, 2n-4\} \cup [2n-2, \binom n2 - 4] \cup \{\binom n2 - 2, \binom n2\}$, giving
$$ d(n) = \binom n2 - 2n + 4 = \frac{n^2 - 5n + 8}{2} \qquad (n = 12, 13). $$
This formula **cannot** persist: by Remark (ii) after Theorem 6, $2n-1, 2n, 2n+1 \notin V(17)$, so $d(17) \le \frac{17^2 - 85 + 8}{2} - 3 = 103$.
More generally Kelly–Moser's theorem (Kelly–Moser 1958, Theorem 4.1: if $m \le n - k$ and $n \ge \frac12(27k^2 - 33k + 11)$
then $f_0 \ge kn - \frac12(3k+2)(k-1)$) and the band analysis of Salamon–Erdős 1988 show that for large $n$ the values
below roughly $n^{3/2}$ come in separated "bands" $[k(n-k) - \binom k2 + 1,\ k(n-k) + \binom k2 + 1]$, $k = 0, 1, 2, \dots$,
each band (for $k \ge 3$) contributing $2\binom k2 - 1$ values, so that $d(n) = \binom n2 - \Theta(n^{3/2})$.

**Open question A.** Determine $d(14), d(15), d(16)$. Our bounds leave exactly the following undecided values:
$n = 14$: is $27 \in V(14)$? ($f_0 \ge 27$ is forced when $m \le 11$; $27$ would need a type with $m \le 11$.)
$n = 15$: $29$; $n = 16$: $32, 33$. (Values listed by `scripts/f0_bounds.py`.) Everything else in $[2n-2, \binom n2 - 4]$
is attained by explicit constructions for these $n$ (to be written up) or excluded.

**Open question B (Salamon–Erdős).** Find the smallest $n^*$ from which the large-$n$ description of $V(n)$ is exact.

## References (short; full list in `notes/references.md`)

de Bruijn–Erdős 1948; Melchior 1940/41; Kelly–Moser 1958; Elliott 1967; Erdős 1972; Grünbaum 1972; Hirzebruch 1983;
Salamon–Erdős 1988; Csima–Sawyer 1993; Pokora 2021.
