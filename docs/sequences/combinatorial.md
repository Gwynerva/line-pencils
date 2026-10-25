---
description: "b(n): the ways n lines could meet if the only rule were that two lines cross once. Known exactly up to 12 lines: 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384."
---

# b(n): ways n lines could meet, judging by combinatorics alone

**In one sentence:** $b(n)$ is the number of different ways $n$ lines can meet that are consistent with the single
rule that two lines meet only once — whether or not the lines can actually be drawn.

The second test ignores geometry and keeps only the rule that two lines meet once: can each pencil be assigned a
set of lines so that no two pencils share two lines? This page gives the terms and the two independent computations
behind them.

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

$b(n)$ for $n = 1, \dots, 12$: **1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384**; for $n = 13$: <span class="status-bound">662 … 2100</span>.
The arithmetic sieve loses $0, 0, 0, 1, 2, 6, 15, 37, 85, 189, 417, 902$ types to the combinatorial one.

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
  a given pair of points". Agrees with the exhaustive search on every type: all $295$ types for $n = 10$, all $619$ for
  $n = 11$ and all $1286$ for $n = 12$ (`runs/sat_{n}.json`).

An earlier, independently written program by the author gives the same values for $n \le 11$.

## Where the arithmetic and combinatorial tests differ

The first type lost is $\{3, 3\}$ at $n = 4$: two triple points among four lines would share two lines. At $n = 12$ the
combinatorial test removes 902 of the 1286 admissible types. Typical reasons are pencils that are too large to coexist
(two pencils of seven lines among twelve lines share at least two lines), or packings that are just barely impossible:
a linear space on 12 elements has at most 20 blocks of size 3, so $\{3^{20}\}$ is combinatorially possible while
$\{3^{21}\}$ is not, although its $21 \cdot 3 = 63$ pairs would fit into $66$.

## Growth

The combinatorial test keeps about 30% of the admissible types at $n = 12$, and the fraction decreases slowly.
No formula or asymptotic for $b(n)$ is known to us; see the [open problems](../open.md).
