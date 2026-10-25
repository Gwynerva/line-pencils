---
description: "a(n): the ways n lines could meet if only counting mattered. It equals the number of partitions of a triangular number into triangular parts."
---

# a(n): arithmetically admissible types

The first test is pure counting: there must be enough pairs of lines for the pencils. The sequence it gives is
already in the OEIS under a different description; this page records the identification.

<div class="thm" markdown>
**Definition.** $A_n$ is the set of multisets $\{k_1, \dots, k_r\}$ of integers with $3 \le k_i \le n$ and
$\sum_{i=1}^r \binom{k_i}2 \le \binom n2$ ($r = 0$ allowed). $a(n) = \lvert A_n \rvert$.
</div>

<div class="thm" markdown>
**Proposition 1.** <span class="status-proved">proved</span> For $n \ge 1$, $a(n)$ equals the number of partitions of
the triangular number $\binom n2$ into triangular numbers $\binom k2$, $k \ge 2$; that is, $a(n) = \mathrm{A072964}(n-1)$.
</div>
<div class="proof" markdown>
*Proof.* Pad a multiset in $A_n$ with $t_2 = \binom n2 - \sum_i \binom{k_i}2$ copies of $2$. The result is a partition of
$\binom n2$ into parts $\binom k2$ with $2 \le k \le n$, and every such partition arises exactly once; the restriction
$k \le n$ is automatic because $\binom{n+1}2 > \binom n2$. A072964$(m)$ counts partitions of $\binom{m+1}2$ into triangular
parts $\binom k2$, $k \ge 2$ (the OEIS definition uses the triangular numbers $1, 3, 6, \dots$). <span class="qed">$\square$</span>
</div>

Terms ($n = 1, 2, \dots$): 1, 1, 2, 4, 7, 15, 32, 66, 141, 295, 619, 1286, 2654, 5460, 11066, 22357, …
(computed by `scripts/pencils.py`, `candidates(n)`, and agreeing with A072964).

## Growth

The number of partitions of $N$ into triangular numbers grows like $\exp(c N^{1/3})$ (partitions into values of a
quadratic polynomial; Hardy–Ramanujan–type asymptotics[^hr]), so $\log a(n) \asymp n^{2/3}$. This is the trivial upper
bound for $\log b(n)$ and $\log c(n)$. A trivial lower bound for $c(n)$ comes from pencils that share no lines:
every partition of a number $\le n$ into parts $\ge 3$ is a realizable type (put the parts as disjoint pencils, the
remaining lines in general position), so $\log c(n) \gtrsim \pi\sqrt{2n/3}$, i.e. $\log c(n) \asymp n^{1/2}$ at least.
Whether the true exponent is $1/2$, $2/3$ or in between is an [open problem](../open.md).

[^hr]: G. H. Hardy, S. Ramanujan, Asymptotic formulae in combinatory analysis, *Proceedings of the London
    Mathematical Society* (2) 17 (1918), 75–115; for partitions into values of a polynomial see E. M. Wright,
    Asymptotic partition formulae III: partitions into $k$-th powers, *Acta Mathematica* 63 (1934), 143–191.

## What the arithmetic sieve already knows about the number of points

The number of intersection points of a type is $f_0 = \binom n2 - \sum_i (\binom{k_i}2 - 1)$. The possible losses
$\binom k2 - 1$ are $2, 5, 9, 14, 20, \dots$; neither $1$ nor $3$ is a sum of these, so $f_0 = \binom n2 - 1$ and
$f_0 = \binom n2 - 3$ never occur, for any $n$. Everything else about $d(n)$ needs geometry.
