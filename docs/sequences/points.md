---
description: "d(n): how many different numbers of crossing points n lines can have. Exact up to 13 lines, with a proof that 2n-3 points are impossible from 12 lines on."
---

# d(n): how many intersection points can n lines have?

**In one sentence:** $d(n)$ is the number of different possible numbers of intersection points of $n$ lines in the
plane, no two parallel. For four lines the possible numbers are 1, 4 and 6, so $d(4) = 3$.

The simplest version of the question counts only the intersection points. It already has a rich answer, and it
is the one sequence for which statements about all $n$ can be proved.

<div class="thm" markdown>
**Definition.** $V(n) = \{ f_0(\mathcal A) : \mathcal A \text{ an arrangement of } n \text{ lines}\}$ and $d(n) = \lvert V(n)\rvert$.
</div>

In the dual picture $V(n)$ is the set of numbers of lines determined by $n$ points of the plane; determining it
is **Grünbaum's problem**, posed in *Arrangements and Spreads*, attacked by Erdős in 1972 and solved for all
sufficiently large $n$ by Salamon and Erdős in 1988.[^erdos72][^se88] Their solution describes $V(n)$ completely
for $n \ge n^*$, with $n^*$ unknown ("likely to be small"). We determine $V(n)$ exactly for $n \le 13$ and prove one
piece of the large-$n$ structure from $n = 13$ on.

[^erdos72]: P. Erdős, On a problem of Grünbaum, *Canadian Mathematical Bulletin* 15 (1972), 23–25,
    [doi:10.4153/CMB-1972-005-4](https://doi.org/10.4153/CMB-1972-005-4).
[^se88]: P. Salamon, P. Erdős, The solution to a problem of Grünbaum, *Canadian Mathematical Bulletin* 31 (1988),
    129–138, [doi:10.4153/CMB-1988-020-2](https://doi.org/10.4153/CMB-1988-020-2).

## Terms

$d(n)$ for $n = 1, \dots, 13$: **1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56** (out of $\binom n2 = 0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78$ conceivable values).

All thirteen terms are <span class="status-computed">computer-verified</span> (the attained values by certificates,
the missing values by theorems or exhaustive computation); $d(13) = 56$ also follows from Theorem 3 below, whose proof
uses an exact computation for $13 \le n \le 35$ instead of the classification.

## The sets V(n)

| $n$ | $V(n)$ | missing values below $\binom n2$ and why |
|---|---|---|
| 3 | 1, 3 | 2 (loss 1) |
| 4 | 1, 4, 6 | 2, 3 (dBE); 5 |
| 5 | 1, 5, 6, 8, 10 | 2–4 (dBE); 7, 9 |
| 6 | 1, 6–11, 13, 15 | 2–5 (dBE); 12, 14 |
| 7 | 1, 7, 9–17, 19, 21 | 2–6 (dBE); 8 (computation); 18, 20 |
| 8 | 1, 8, 11–24, 26, 28 | 2–7 (dBE); 9, 10 (computation); 25, 27 |
| 9 | 1, 9, 13–32, 34, 36 | 2–8 (dBE); 10–12 (computation); 33, 35 |
| 10 | 1, 10, 16–41, 43, 45 | 2–9 (dBE); 11–15 (Elliott); 42, 44 |
| 11 | 1, 11, 18–51, 53, 55 | 2–10 (dBE); 12–17 (Elliott); 52, 54 |
| 12 | 1, 12, 20, 22–62, 64, 66 | 2–11 (dBE); 13–19 (Elliott); 21 (computation); 63, 65 |
| 13 | 1, 13, 22, 24–74, 76, 78 | 2–12 (dBE); 14–21 (Elliott); 23 (Theorem 3); 75, 77 |

"dBE" is the de Bruijn–Erdős theorem (an arrangement that is not a pencil has at least $n$ points), "Elliott" is
Elliott's theorem (no $n-1$ lines concurrent and $n \ge 10$ imply $f_0 \ge 2n-4$),[^elliott] the two top gaps are
Theorem 1, and "computation" means that every admissible type with that $f_0$ was shown non-realizable (see the
[realizable page](realizable.md) and `data/results/`).

[^elliott]: P. D. T. A. Elliott, On the number of circles determined by $n$ points, *Acta Mathematica Academiae
    Scientiarum Hungaricae* 18 (1967), 181–188, Theorem 3, [doi:10.1007/BF02020972](https://doi.org/10.1007/BF02020972).
    Conjectured by Kelly and Moser, who proved it for $n \ge 27$ and $n = 10$.

## Theorems

<div class="thm" markdown>
**Theorem 1 (the top).** <span class="status-proved">proved</span> For every $n \ge 3$, $\binom n2 - 1 \notin V(n)$ and
$\binom n2 - 3 \notin V(n)$, while $\binom n2$ and $\binom n2 - 2$ are in $V(n)$, and $\binom n2 - 4 \in V(n)$ for $n \ge 5$.
</div>
<div class="proof" markdown>
*Proof.* $f_0 = \binom n2 - \ell$ where the loss $\ell = \sum_{k\ge3}(\binom k2 - 1)t_k$ is a sum of numbers from
$\{2, 5, 9, 14, \dots\}$; $1$ and $3$ are not such sums. General position, one triple point, and two triple points give losses $0, 2, 4$;
two triple points need $n \ge 5$ lines. <span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Lemma 2 (large pencils).** <span class="status-proved">proved</span> Let $m$ be the size of the largest pencil of $\mathcal A$.
If $m = n$ then $f_0 = 1$; if $m = n-1$ then $f_0 = n$; if $m = n-2$ then $f_0 \in \{2n-4, 2n-2\}$, both values occurring for every $n \ge 5$ (for $n = 4$ only $2n - 2 = 6$).
</div>
<div class="proof" markdown>
*Proof.* Let $P$ be the point of multiplicity $m$ and call the lines not through $P$ *free*. A free line meets the $m$
lines through $P$ in $m$ distinct points, none equal to $P$ (two lines through $P$ meet only at $P$).

For $m = n-1$ this gives $1 + (n-1)$ points.

For $m = n-2$, call the free lines $A$ and $B$. The points are $P$, the $n-2$ points $A \cap L$, the $n-2$ points $B \cap L$
(for $L$ through $P$) and $A \cap B$. Here $A \cap L = B \cap L'$ forces $L = L'$, and $A \cap L = B \cap L$ exactly when
$A \cap B \in L$, in which case the three points coincide. Hence

$$f_0 = 2n - 2 - 2\,[A \cap B \text{ lies on a line through } P].$$

Both cases are realizable. <span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Theorem 3 (the bottom, $n \ge 13$).** <span class="status-proved">proved, computer-assisted</span> Let $n \ge 13$. If no $n-2$ lines of
$\mathcal A$ are concurrent, then $f_0(\mathcal A) \ge 2n - 2$. Consequently

$$ V(n) \cap [1, 2n-2] = \{1,\ n,\ 2n-4,\ 2n-2\} \qquad (n \ge 13), $$

and in particular $2n-3$ intersection points are impossible for $n \ge 13$.
</div>

The proof combines three lower bounds for $f_0$ in terms of $m$, the largest pencil size, and $b = n - m$:

* **the spoke bound** $f_0 \ge 1 + G(n, b)$, a refinement of the Kelly–Moser count $f_0 \ge 1 + mb - \binom b2$, obtained by
  counting the points on the $m$ lines through a point of multiplicity $m$;
* **the Melchior bound** $f_0 \ge \frac{n(n-1) + 3m + 3}{m + 3}$, obtained from Melchior's inequality by a one-line
  optimisation;
* **a linear-programming bound** using Melchior's and Hirzebruch's inequalities together, with an exact rational
  certificate for each $(n, m)$ where it is needed ($n = 13, 14, 15, 16$ only).

For $n \ge 17$ the first two bounds suffice (checked for $n \le 120$ by the script and proved for $n \ge 36$ by an
explicit inequality), so the proof for all $n \ge 13$ is complete. The full proof, with the exact LP certificates,
is on the [theorems page](../theorems.md#points).

<div class="thm" markdown>
**Corollary 4.** <span class="status-proved">proved</span> For $n \ge 6$: $2n - 3 \in V(n)$ if and only if $n \le 11$.
</div>
<div class="proof" markdown>
*Proof.* *Case $n \ge 13$.* This is Theorem 3.

*Case $n = 12$.* There are $43$ admissible types with $21$ points. For $34$ of them no linear space exists, and six more
fail Melchior's inequality. The remaining three, $\{4^9\}$, $\{5^2, 4^3, 3^6\}$ and $\{5^3, 3^9\}$, are not realizable: the first
is excluded by Proposition C3, and the other two admit no orientable linear space ([realizable page](realizable.md)).

*Case $n \le 11$.* Certificates exist with $2n - 3$ points:

* $n = 6$: $\{3^3\}$ ($9$ points);
* $n = 7$: $\{3^5\}$ and $\{4^2\}$ ($11$ points);
* $n = 8$: $\{4, 3^5\}$ and $\{5, 3^3\}$ ($13$);
* $n = 9$: $\{4, 3^8\}$, $\{5, 3^6\}$ and $\{4^3, 3^3\}$ ($15$);
* $n = 10$: $\{5, 4, 3^7\}$ and $\{4^4, 3^4\}$ ($17$);
* $n = 11$: $\{4^4, 3^8\}$ ($55 - 4 \cdot 5 - 8 \cdot 2 = 19$).

For $n = 4$ and $5$ the value $2n - 3$ is $5$, resp. $7$, excluded by Theorem 1, and for $n = 3$ it is $3 \in V(3)$. So,
precisely, $2n-3 \in V(n)$ iff $n = 3$ or $6 \le n \le 11$. <span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Observation 5 (a formula that must fail).** <span class="status-computed">computer-verified</span> For $n = 12, 13$,
$V(n) = \{1, n, 2n-4\} \cup [2n-2, \binom n2 - 4] \cup \{\binom n2 - 2, \binom n2\}$, so $d(n) = \binom n2 - 2n + 4 = \frac{n^2 - 5n + 8}{2}$.
This cannot continue: the bounds in the proof of Theorem 3 give $f_0 \ge 2n + 2$ for $n = 17$ whenever no $n - 2$
lines are concurrent, so $2n - 1, 2n, 2n+1 \notin V(17)$ and $d(17) \le 103$. For large $n$, Salamon and Erdős show that
$V(n)$ below roughly $n^{3/2}$ consists of separated "bands", so $d(n) = \binom n2 - \Theta(n^{3/2})$.
</div>

<div class="thm openp" markdown>
**Open question.** Determine $d(14), d(15), d(16)$. The band construction ([theorems](../theorems.md#bands)) and
the extension of certified 13-line arrangements by a line through several existing points give certificates for
65 values at $n = 14$; together with the exclusions this leaves exactly two undecided values, $27$ and $28$, so
$65 \le d(14) \le 67$. For $n = 15$: $73 \le d(15) \le 79$ (undecided $29$–$33$, $37$); $n = 16$: $83 \le d(16) \le 91$;
$n = 17$: $92 \le d(17) \le 103$ (`notes/bands.md`). The undecided values at the low end would need an arrangement
whose largest pencil has only $5$ to $7$ lines and whose other lines are extremely concurrent; the LP bound with
Hirzebruch's inequality misses $2n-1$ by a fraction.
</div>
