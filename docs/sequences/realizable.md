---
description: "c(n): the number of different ways n straight lines in the plane can meet. Exact up to 12 lines: 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180, 336. OEIS A399464."
---

# c(n): ways n lines can meet

**In one sentence:** $c(n)$ is the number of different ways $n$ lines in the plane, no two parallel, can meet — two
ways being the same when they produce the same list of how many lines pass through each intersection point. OEIS: [A399464](https://oeis.org/A399464).

This page is about the types that can actually be drawn: every known term with its evidence, and the types that
are still undecided.

<div class="thm" markdown>
**Definition.** A type is *realizable* if it is the pencil type of an arrangement of $n$ distinct lines in
$\mathbb{RP}^2$ (equivalently, of $n$ lines in the Euclidean plane with no two parallel). $c(n)$ is the number of
realizable types.
</div>

## Terms

$c(n)$ for $n = 1, \dots, 12$: **1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180, 336**; $n = 13$: <span class="status-bound">620 … 659</span>.
Combinatorially possible but not realizable: $0, 0, 0, 0, 0, 0, 1, 1, 3, 8, 22, 48$ types for $n \le 12$.

Status through $n = 12$: <span class="status-computed">computer-verified</span>; $c(13)$ is a <span class="status-bound">bound</span>. The evidence is of two kinds and every
type has one of them:

* **Realizable types: exact certificates.** For each of the 732 realizable types with $3 \le n \le 12$ (for $n \le 2$
  there is nothing to certify) a set of $n$ lines with coordinates in $\mathbb Q$ (all but six), $\mathbb Q(\sqrt 2)$ or
  $\mathbb Q(\sqrt 5)$ is stored in `data/certificates/` (see [fields of definition](#fields-of-definition)). The
  [verifier](../data.md) recomputes the pencil type of each certificate with exact arithmetic; it runs in continuous
  integration on every change of the repository.
* **Non-realizable types: a proof.** Each of the $b(n) - c(n)$ combinatorially possible but non-realizable types is
  excluded by Melchior's inequality (Fano $\{3^7\}$, dual Hesse $\{3^{12}\}$, and most others), by the Csima–Sawyer bound
  $t_2 \ge 6n/13$ ($\{3^{11}\}$ at $n = 9$, $\{4, 3^{15}\}$ and $\{3^{17}\}$ at $n = 11$), or because no linear space of
  the type is orientable (Möbius–Kantor $\{3^8\}$ at $n = 8$; $\{4^2, 3^9\}$ and $\{3^{13}\}$ at $n = 10$; nine types at
  $n = 11$; fifteen types at $n = 12$). For $n = 12$ five more are excluded individually: $\{4^9\}$ by Proposition C3,
  $\{3^{20}\}$ and $\{4^5, 3^9\}$ by computations showing that none of their linear spaces is orientable, and
  $\{6, 4, 3^{12}\}$, $\{6, 3^{14}\}$ by Gröbner certificates although they are orientable (see below). The orientability
  verdicts come from an exhaustive search ([algorithms](../algorithms.md)); the files
  `data/results/classification_n{n}.json` list the reason for every type.

## Bounds

| $n$ | lower bound | upper bound |
|---|---|---|
| every $n$ | partitions of $m \le n$ into parts $\ge 3$ | $b(n) \le a(n)$ |
| 13 | 620 | 659 |
| 14 | 1104 | $b(14) \le a(14) = 5460$ |

For every $n$, pencils that share no lines realize every partition of a number $m \le n$ into parts $\ge 3$
([arithmetic page](arithmetic.md#growth)), and $c(n) \le b(n)$ ([A400149](https://oeis.org/A400149)). For $n = 13$ and
$14$ the lower bounds are the verified certificates (`data/certificates/n13.json`, `n14.json`); for $n = 13$ the upper
bound adds the 39 undecided types ([below](#n-13)); for $n = 14$ the classification was not run.

## n = 12: what is known

Of the 384 combinatorially possible types, 336 have verified certificates: 332 over $\mathbb Q$, one over
$\mathbb Q(\sqrt 2)$ (which also has a rational realization) and three over $\mathbb Q(\sqrt 5)$ (no rational realization is
known). The other 48 are excluded: 28 by Melchior's inequality, 15 because none of their linear spaces is orientable,
$\{4^9\}$ by [Proposition C3](../theorems.md#c3) (it is the type of the complex Hesse arrangement), $\{3^{20}\}$ by
[Proposition C3a](../theorems.md#c3a) (none of its five linear spaces is orientable), $\{4^5, 3^9\}$ by
[Proposition C3b](../theorems.md#c3b) (a case split of the orientability search), and $\{6, 4, 3^{12}\}$, $\{6, 3^{14}\}$ by
exact algebraic certificates although they are orientable ([Theorems C4, C5](../theorems.md#lines-vs-pseudolines)).
No type remains undecided. The table lists the 21 types that pass every inequality, with how each was decided;
$\{3^{18}\}$, the last type to be realized ([Example C3c](../theorems.md#c3c)), comes first.

--8<-- "open12.md"

"Non-orientable": no linear space of the type is orientable, so not even pseudolines realize it; "Gröbner": every
orientable linear space of the type has an algebraic certificate of non-realizability. A dash in the "orientable?"
column means that the type was excluded by a theorem without an orientability search.

## n = 13

620 types have verified certificates (`data/certificates/n13.json`): 597 from the original exploratory search, three
built with the band theorem, 18 by the zone walk, one by targeted deformation, and one, $\{4^9\}$, from a plane
section of the H4 mirror arrangement ([algorithms](../algorithms.md#zone-walk)). $\{4^9\}$ is impossible for 12 lines
([Proposition C3](../theorems.md#c3)) but is realized by 13 of the 31 planes perpendicular to the symmetry axes of the
icosahedron.
The combinatorial test, the inequalities and the band theorem ([Theorem B4](../theorems.md#bands)) exclude all other
types except 39, so $620 \le c(13) \le 659$ (<span class="status-bound">bound</span>). Of the excluded
types, 28 are excluded by the band theorem alone.

## Fields of definition

Every realizable type for $n \le 14$ in our data has a certificate over $\mathbb Q$ or over $\mathbb Q(\sqrt d)$ with
$d \in \{2, 3, 5\}$. The type $\{5, 3^{10}\}$ ($n = 10$) provably needs an irrational number: the regular pentagon is the
only way to arrange it, up to projective transformation ([Proposition C1](../theorems.md#c1)). We do
not know whether some type for small $n$ needs a field of degree $\ge 3$.
