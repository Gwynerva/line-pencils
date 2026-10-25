---
description: "c(n): the number of different ways n straight lines in the plane can meet. Exact up to 11 lines: 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180."
---

# c(n): ways n lines can meet

**In one sentence:** $c(n)$ is the number of different ways $n$ lines in the plane, no two parallel, can meet — two
ways being the same when they produce the same list of how many lines pass through each intersection point.

This page is about the types that can actually be drawn: every known term with its evidence, and the types that
are still undecided.

<div class="thm" markdown>
**Definition.** A type is *realizable* if it is the pencil type of an arrangement of $n$ distinct lines in
$\mathbb{RP}^2$ (equivalently, of $n$ lines in the Euclidean plane with no two parallel). $c(n)$ is the number of
realizable types.
</div>

## Terms

$c(n)$ for $n = 1, \dots, 11$: **1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180**; $n = 12$: <span class="status-bound">335 … 337</span>; $n = 13$: <span class="status-bound">600 … 659</span>.
Combinatorially possible but not realizable: $0, 0, 0, 0, 0, 0, 1, 1, 3, 8, 22$ types for $n \le 11$, between 47 and 49 for $n = 12$.

Status through $n = 11$: <span class="status-computed">computer-verified</span>; $c(12)$ and $c(13)$ are <span class="status-bound">bounds</span>. The evidence is of two kinds and every
type has one of them:

* **Realizable types: exact certificates.** For each of the 1 + 1 + 2 + 3 + 5 + 9 + 16 + 28 + 53 + 98 + 180 types a set
  of $n$ lines with coordinates in $\mathbb Q$ (all but two) or $\mathbb Q(\sqrt 5)$ ($\{5, 3^{10}\}$ for $n = 10$, which
  provably needs $\sqrt 5$, and $\{3^{16}\}$ for $n = 11$, where the search simply happened to find a pentagonal example
  first) is stored in `data/certificates/`. The [verifier](../data.md) recomputes the pencil type of
  each certificate with exact arithmetic; it runs in continuous integration on every change of the repository.
* **Non-realizable types: a proof.** Each of the $b(n) - c(n)$ combinatorially possible but non-realizable types is
  excluded by Melchior's inequality (Fano $\{3^7\}$, dual Hesse $\{3^{12}\}$, and most others), by the Csima–Sawyer bound
  $t_2 \ge 6n/13$ ($\{3^{11}\}$ at $n = 9$, $\{4, 3^{15}\}$ and $\{3^{17}\}$ at $n = 11$), or because no linear space of
  the type is orientable (Möbius–Kantor $\{3^8\}$ at $n = 8$; $\{4^2, 3^9\}$ and $\{3^{13}\}$ at $n = 10$; nine types at
  $n = 11$). The orientability verdicts come from an exhaustive search ([algorithms](../algorithms.md)); the files
  `data/results/classification_n{n}.json` list the reason for every type.

## n = 12: what is known

Of the 384 combinatorially possible types, 335 have verified certificates (331 over $\mathbb Q$, one over $\mathbb Q(\sqrt 2)$,
three over $\mathbb Q(\sqrt 5)$; the quadratic fields reflect where the search found the example, not a necessity),
28 are excluded by Melchior's
inequality, $\{4^9\}$ by a theorem (it is the type of the complex Hesse arrangement: [theorems](../theorems.md)), $\{3^{20}\}$ because
none of its five linear spaces is orientable ([Proposition C3a](../theorems.md)), 15 more types because no linear space of theirs is orientable, and
$\{6, 4, 3^{12}\}$, $\{6, 3^{14}\}$ by exact algebraic certificates although they are orientable ([Theorems C4, C5](../theorems.md#lines-vs-pseudolines)).
Two types remain undecided. The table lists every type not excluded by an inequality, with its status; the undecided
ones are at the top.

--8<-- "open12.md"

A dash in the "orientable?" column means that the orientability search did not finish.

## n = 13

600 types have verified certificates (`data/certificates/n13.json`; three of them were constructed with the band
theorem). The combinatorial test, the inequalities and the band theorem ([Theorem B4](../theorems.md#bands)) exclude
all other types except 59, so $600 \le c(13) \le 659$ (<span class="status-bound">bound</span>). Of the excluded
types, 41 are excluded by the band theorem alone.

## Fields of definition

Every realizable type for $n \le 13$ in our data has a certificate over $\mathbb Q$ or over $\mathbb Q(\sqrt d)$ with
$d \in \{2, 3, 5\}$. The type $\{5, 3^{10}\}$ ($n = 10$) provably needs an irrational number: the regular pentagon is the
only way to arrange it, up to projective transformation ([Proposition C1](../theorems.md)). We do
not know whether some type for small $n$ needs a field of degree $\ge 3$.
