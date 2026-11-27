---
description: "b(n): the ways n lines could meet if the only rule were that two lines cross once. Known exactly through 15 lines. OEIS A400149."
---

# b(n): ways n lines could meet, judging by combinatorics alone

**In one sentence:** $b(n)$ is the number of different ways $n$ lines can meet that are consistent with the single
rule that two lines meet only once — whether or not the lines can actually be drawn. OEIS: [A400149](https://oeis.org/A400149).

In other words: can each pencil be assigned a set of lines so that no two pencils share two lines? This page gives
the terms, the project's two computations through 12 lines, and Mark Kim's extension through 15.

<div class="thm" markdown>
**Definition.** A type $\{k_1, \dots, k_r\} \in A_n$ is *combinatorially possible* if there is a family of blocks
$B_1, \dots, B_r \subseteq \{1, \dots, n\}$ with $\lvert B_i \rvert = k_i$ and $\lvert B_i \cap B_j\rvert \le 1$ for $i \ne j$.
$b(n)$ is the number of combinatorially possible types.
</div>

Here the elements $1, \dots, n$ stand for the lines and the block $B_i$ for the lines of the $i$-th pencil. Adding every
pair of elements not covered by a block as a 2-block gives a *linear space*: every pair lies in exactly one block, just
as every two lines meet in exactly one point. So $b(n)$ counts the multisets of block sizes $\ge 3$ that occur in
linear spaces on $n$ elements (compare A001200, which counts the linear spaces themselves).

## Terms

$b(n)$ for $n = 1, \dots, 15$: **1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384, 729, 1357, 2558**.
The combinatorial sieve excludes $a(n)-b(n)$ arithmetic candidates, including 1925, 4103 and 8508 for $n = 13,14,15$.

All terms through $n = 12$ are <span class="status-computed">computer-verified</span>:

* **Exhaustive search** (`engine/ls.c`, mode 0; driver `scripts/engine_run.py`). For each of the $a(n)$ admissible types
  the program decides whether blocks of the given sizes can be packed. It always extends the lexicographically first
  uncovered pair of elements, either by a 2-block or by a new block of a still-needed size, and breaks the symmetry
  of unused elements by introducing them in increasing order. The search is complete because every linear space
  with the required block sizes contains, for the first uncovered pair, exactly one of the alternatives tried; the
  symmetry breaking is valid because untouched elements are interchangeable. Every query terminated (no time-outs);
  the longest single query for $n = 12$ ($\{3^{20}\}$) took 48 seconds, the whole run 71 seconds on 11 threads.
  Logs: `runs/comb_{n}.json`.
* **Independent SAT check** (`scripts/sat_linear_space.py`, CaDiCaL through python-sat): one Boolean variable per
  candidate block, cardinality constraints "exactly $t_k$ blocks of size $k$", and "at most one chosen block contains
  a given pair of elements". Agrees with the exhaustive search on every type: all $295$ types for $n = 10$, all $619$ for
  $n = 11$ and all $1286$ for $n = 12$ (`runs/sat_{n}.json`).

## Mark Kim's extension to 15 points

[Mark Kim, *Line-size types of finite linear spaces: an exhaustive computation up to fifteen points*](https://doi.org/10.5281/zenodo.24567131) (2026), Theorem 1.1 and Table 1, gives
$\lambda(13)=729$, $\lambda(14)=1357$ and $\lambda(15)=2558$. His $\lambda(n)$ is exactly $b(n)$ by the definition above.
The search enumerates feasible distributions of block sizes through each point and then tries to build the blocks.
The [source and per-type verdicts](https://github.com/marik-11/linear_space_types/tree/e126faeb3f621ef4c85e3872c320a27a901f229e)
precede any test for real realizability. A fresh rerun of Kim's method at $n=14$ agreed on all 4843 verdicts.
See [how to check the published tables](../data.md#kims-classifications).

Kim first discards types with $k_1+k_2>n+1$ for the two largest blocks, which cannot fit in an $n$-element set
with at most one shared point. This leaves 2347, 4843 and 10027 candidates at $n=13,14,15$.
The corresponding arithmetic counts $a(n)$ are 2654, 5460 and 11066.
For every $n$, $c(n)\le b(n)\le a(n)$ ([A399464](https://oeis.org/A399464), [A072964](https://oeis.org/A072964)).

## Where the arithmetic and combinatorial tests differ

The first type lost is $\{3, 3\}$ at $n = 4$: two triple points among four lines would share two lines. At $n = 12$ the
combinatorial test removes 902 of the 1286 admissible types. Typical reasons are pencils that are too large to coexist
(two pencils of seven lines among twelve lines share at least two lines), or packings limited by the maximum number of triples:
a linear space on 12 elements has at most 20 blocks of size 3, so $\{3^{20}\}$ is combinatorially possible while
$\{3^{21}\}$ is not, although its $21 \cdot 3 = 63$ pairs would fit into $66$.

## Growth

The combinatorial test keeps about 30% of the admissible types at $n = 12$, and the fraction decreases slowly.
No formula or asymptotic for $b(n)$ is known to us; see the [open problems](../open.md).
