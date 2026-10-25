---
description: "The symbols used on the site: pencil types, numbers of intersection points, linear spaces, and how the four sequences are numbered."
---

# Notation

The symbols used on this site, fixed once. Where the literature has a standard, it follows Grünbaum's
*Arrangements and Spreads*.[^gr]

[^gr]: B. Grünbaum, *Arrangements and Spreads*, CBMS Regional Conference Series in Mathematics 10, American
    Mathematical Society, Providence, 1972.

## Arrangements

| symbol | meaning |
|---|---|
| $\mathbb{RP}^2$ | the real projective plane; points $(x:y:z)$, lines $\{ax+by+cz=0\}$ written $[a:b:c]$ |
| $\mathcal A$ | an arrangement: a set of $n$ distinct lines in $\mathbb{RP}^2$ (no "general position" assumed) |
| $n = \lvert\mathcal A\rvert$ | the number of lines |
| $\mu(P)$ | the multiplicity of a point: the number of lines of $\mathcal A$ through $P$ |
| pencil | the set of lines through an intersection point; its *size* is $\mu(P)$ |
| $t_k(\mathcal A)$ | the number of points with $\mu(P) = k$, $k \ge 2$ (Grünbaum's $t_k$); $t_2$ counts the *ordinary* points |
| $f_0(\mathcal A)$ | $\sum_{k\ge2} t_k$, the number of intersection points (vertices) |
| $m(\mathcal A)$ | $\max\{k : t_k > 0\}$, the size of the largest pencil |
| $\ell(\mathcal A)$ | the loss $\binom n2 - f_0 = \sum_{k \ge 3}(\binom k2 - 1)\,t_k$ |
| pencil type | the multiset $\{k^{t_k} : k \ge 2\}$; written without the $2$s, e.g. $\{6, 4, 3^{12}\}$ |

Synonyms found in the literature for the pencil type: *t-vector* $(t_2, t_3, \dots)$, *weak combinatorics*,
*point-multiplicity sequence*. We prefer "type" and write it as a multiset because the sequences count multisets.

Pencils of size two are always omitted from the written type; their number is
$t_2 = \binom n2 - \sum_{k\ge3}\binom k2 t_k$. When an explicit $t_2$ helps, we write $\{6, 4, 3^{12}, 2^9\}$.

## Combinatorial structures

| symbol | meaning |
|---|---|
| linear space | a set of $n$ elements with a family of *blocks* (subsets of size $\ge 2$) such that every pair of elements lies in exactly one block; for an arrangement, the elements are the lines and the blocks are the pencils |
| blocks of a type | for a type $\{k_1, \dots, k_r\}$: blocks of sizes $k_1, \dots, k_r$, pairwise sharing at most one point; the uncovered pairs are the 2-blocks |
| chirotope $\chi$ | an alternating map $\binom{[n]}{3} \to \{+, 0, -\}$ satisfying the three-term Grassmann–Plücker relations; $\chi = 0$ exactly on the collinear triples |
| orientable | a linear space is orientable if some chirotope has exactly its blocks as zero set; equivalently it is the underlying matroid of a rank-3 oriented matroid, equivalently (Folkman–Lawrence) it is the incidence structure of an arrangement of pseudolines |

In the dual (point) picture a pencil of $k$ lines is a $k$-point line, so a linear space on $n$ points with blocks of
sizes $k_i$ is exactly the combinatorial skeleton of a set of $n$ points with lines of those sizes.

## The sequences

| symbol | definition | first terms |
|---|---|---|
| $a(n)$ | number of arithmetically admissible types for $n$ lines | 1, 1, 2, 4, 7, 15, 32, 66, 141, 295, 619, 1286 |
| $b(n)$ | number of types admitting a linear space | 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384 |
| $c(n)$ | number of types of arrangements of $n$ real lines | 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180 |
| $d(n)$ | number of distinct values of $f_0$ over arrangements of $n$ lines | 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56 |
| $V(n)$ | the set of values of $f_0$; $d(n) = \lvert V(n) \rvert$ | |
| $A_n$ | the set of arithmetically admissible types; $a(n) = \lvert A_n\rvert$ | |

All sequences are indexed by $n \ge 1$, the number of lines; $n = 1$ gives the single line with no intersection
points, counted as one (empty) type and one value $f_0 = 0$.

## Status labels

Results on this site are labelled by how they are established.

* <span class="status-proved">proved</span> — a complete proof is given or a precise reference is cited;
* <span class="status-computed">computer-verified</span> — established by a program whose algorithm is described on the
  [algorithms page](algorithms.md), with the exact command, log and (for examples) an exact certificate checked by the
  [verifier](data.md);
* <span class="status-bound">bound</span> — only an interval is known; both ends are justified;
* <span class="status-conj">conjectured</span> — supported by data, not proved.

## Numbering

Theorems, lemmas and propositions are numbered consecutively within each page. Proofs end with $\square$.
A "Theorem" whose proof relies on a computation says so explicitly and points to the data.
