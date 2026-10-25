---
description: "How the numbers were computed: exhaustive search, SAT solving, orientability checks and exact certificates, with the command that reproduces each step."
---

# Algorithms

This page describes every computation behind the numbers: what each program decides, why its answer is
complete, and the command that reproduces it.

All code is in the repository [Gwynerva/line-pencils](https://github.com/Gwynerva/line-pencils); paths below are
relative to its root. Everything was run on one desktop machine (AMD Ryzen 5 5600X, 6 cores / 12 threads, 32 GB).

## 0. Enumerating admissible types

`scripts/pencils.py`, function `candidates(n)`: a recursion producing all non-increasing tuples of integers in
$[3, n]$ whose triangular numbers sum to at most $\binom n2$. The same module implements the theorem filters
(Melchior, Csima–Sawyer, de Bruijn–Erdős) as pure functions of the type.

## 1. The combinatorial sieve: exhaustive search for linear spaces

**Decides:** does a linear space on $n$ points with blocks of the prescribed sizes $k_1 \ge \dots \ge k_r \ge 3$ exist?

**Program:** `engine/ls.c` (C, standard library only; `gcc -O2 -o ls ls.c`), mode 0. Queries are read from standard
input as `n mode seconds k1 k2 ...`; the answer is `YES`, `NO` or `TIMEOUT`, with a witness (the blocks) for `YES`.

**Search.** The state is a partial linear space: a set of blocks already placed (including 2-blocks). The algorithm
repeatedly takes the lexicographically smallest pair of points $\{p, q\}$ not yet covered by a block and branches:
either $\{p, q\}$ is a 2-block (allowed while the budget $t_2$ of 2-blocks is positive), or it is contained in a new
block of size $k$ for one of the still-needed sizes $k$, whose remaining $k - 2$ points are chosen, in increasing
order, among the points $r > q$ not yet joined to $p$, $q$ or each other. Points that lie on no block yet are
interchangeable, so they are used in increasing order (a point touched for the first time must be the smallest
untouched point). At the root the first block is forced to be of the largest size (every linear space with the
prescribed sizes contains such a block, and the point labels can be chosen so that it is found first).

**Completeness.** Every linear space $\mathcal L$ with the prescribed sizes is reached: at each node, the pair
$\{p, q\}$ lies in exactly one block of $\mathcal L$, which is one of the alternatives tried; the symmetry rules only
discard structures isomorphic (by a relabelling of untouched points) to ones that are kept. Hence `NO` means that no
linear space exists. `YES` answers come with an explicit witness, which is re-checked by the driver.

**Cost.** $n = 11$: all 619 types in 6 s on 12 threads; $n = 12$: all 1286 types in 71 s on 11 threads (longest query
48 s); no time-outs (`runs/comb_12.json`, `runs/comb_12.log`). For $n = 13$ the search was run, with a limit of 300 s
per query, only on the 1254 types that pass the inequality filters (they are the candidates for $c(13)$); 71 queries
timed out, and the 17 of them that mattered for $c(13)$ were decided by the SAT encoding of §2. The term $b(13)$ is
therefore not determined: it would also need the types that fail an inequality.

**Command.**
```bash
python scripts/engine_run.py 12 0 120 runs/comb_12.json --workers 11
```

## 2. The combinatorial sieve, independently: SAT

`scripts/sat_linear_space.py` encodes the same question for CaDiCaL (via python-sat): a Boolean variable $x_S$ for
every $k$-subset $S$ of the points and every needed size $k$; "exactly $t_k$ true variables among the $k$-subsets"
(sequential-counter cardinality encodings); "at most one true variable among the subsets containing a given pair"
(66 pairs for $n = 12$); and the first block of the largest size fixed to $\{0, \dots, k-1\}$. Nothing clever, on
purpose: the encoding can be audited in a few minutes. Agreement with the exhaustive search: all 295 types for
$n = 10$, all 619 types for $n = 11$ and all 1286 types for $n = 12$ (`runs/sat_{n}.json`).

```bash
python scripts/sat_linear_space.py 11 runs/sat_11.json --workers 6
```

## 3. The orientability sieve

**Decides:** does an *orientable* linear space with the prescribed block sizes exist, i.e. one admitting a chirotope
(an alternating sign function on triples, zero exactly on the collinear triples, satisfying the three-term
Grassmann–Plücker relations)? A `NO` proves that the type is not realizable by real lines.

Two implementations:

* **Engine, mode 4** (`engine/ls.c`): the search of §1 is continued through all linear spaces (not stopped at the
  first), and at every complete linear space a dedicated solver decides chirotope existence: the relations with two
  non-zero terms are linear equations over $\mathbb F_2$ (the sign of a product is the XOR of the signs) and are
  eliminated by Gauss–Jordan; the relations with three non-zero terms become "not all equal" constraints and are
  decided by a small DPLL search with unit propagation. The reorientation freedom is fixed by normalising
  $\chi(0, 1, x) = +$. Completeness follows from §1 plus the correctness of the chirotope solver, which was
  tested on the Fano plane, the Möbius–Kantor configuration, the Hesse configuration (all non-orientable) and on
  Pappus, non-Pappus and the realizable types (orientable).
* **SAT** (`scripts/sat_orient.py`): the block variables of §2, collinearity variables $c_T \leftrightarrow \bigvee_{S \supseteq T} x_S$,
  sign variables $s_T$, and for each Grassmann–Plücker relation auxiliary variables "term is zero / positive / negative"
  with the clauses "if some term is non-zero then some term is positive and some term is negative".

Both agree on every type decided by both. Orientability is much harder than the combinatorial sieve: for $n = 11$,
the nine combinatorially possible types that are neither realized nor excluded by an inequality are all non-orientable
(`runs/orient_11.json`, `runs/sat_orient_11.json`). At $n = 12$ the engine decided all candidates but one: the
search for $\{4^5, 3^9\}$ did not finish within four hours ([realizable page](sequences/realizable.md)).

```bash
python scripts/engine_run.py 11 4 1800 runs/orient_11.json --workers 2 --only "4,3,3,3,3,3,3,3,3,3,3,3,3,3,3;..."
python scripts/sat_orient.py 11 runs/sat_orient_11.json --workers 2 --only "..."
```

## 4. Finding examples

Realizable types are proved realizable by exhibiting coordinates. Three sources were used:

1. **Rich point sets** (the author's original search, `legacy/program/`): subsets of integer grids, regular polygons
   with their points at infinity ($\mathbb Q(\sqrt 2), \mathbb Q(\sqrt 3), \mathbb Q(\sqrt 5)$), rational torsion points
   of elliptic curves (orders 7–12), and intersections of their lines; simulated annealing over $n$-subsets looking for
   a target type. All examples for $n \le 12$ and all but three for $n = 13$ were found this way.
2. **From a linear space** (`scripts/realize.py`): given blocks, four points not collinear in the linear space are fixed
   to the standard projective frame, the rest are unknowns; the $3 \times 3$ determinants of collinear triples are driven
   to zero by least squares from random starts, and a solution is accepted only if all non-collinear triples have
   determinant bounded away from zero. Then coordinates are made exact: one coordinate at a time is snapped to a nearby
   rational with small denominator and the others re-solved, until the remaining ones are forced; the forced ones are
   recognised as rationals or as $a + b\sqrt d$. **The result is accepted only if the exact verifier confirms the type.**
3. **Orientable linear spaces as a source of candidates** (`scripts/find_examples.py`, `scripts/realize_enum.py`): the SAT
   encoder or the engine (mode 5) enumerates orientable linear spaces of a type, and each one is handed to the realizer.
   Labelled linear spaces that are relabellings of an already tried one are skipped using a cheap isomorphism invariant.
4. **Constructions** (`scripts/bands.py`, `scripts/extend.py`): a pencil added to a smaller certified arrangement
   ([band theorem](theorems.md#bands)), or a line added through several intersection points of a certified arrangement.
   These produced three types for $n = 13$ and the arrangements of 14 lines.

```bash
python scripts/find_examples.py 12 "6,3,3,3,3,3,3,3,3,3,3,3,3,3,3" --max 400 --time 2400
```

## 5. Verification

`verifier/verify.py` — described on the [data page](data.md). Standard library only, about 150 lines, exact
arithmetic in $\mathbb Z[\sqrt d]$, all pencils recomputed as maximal concurrent sets from scratch.

## 6. Classification and the sequences

`scripts/classify.py n` merges certificates, theorem filters, engine and SAT logs into one verdict per admissible
type, with the reason (`data/results/classification_n{n}.json`), and computes the four sequences, printing an interval
whenever some type is still open. It refuses to run if a certificate fails verification or if the engine and the SAT
solver disagree.

## 7. Bounds for the number of points

`scripts/f0_bounds.py` computes the three lower bounds used in the proof of the structure theorem for intersection
points: the spoke bound (a small dynamic programme), the Melchior bound (closed form), and a linear-programming bound
whose rational dual certificate is extracted from the numerical solution and re-verified exactly with `fractions`.

## 8. Proving non-realizability of an orientable type

Three programs, chained (details and the proof of correctness in `notes/nonrealizability.md`):

1. `engine/ls.c` mode 5 enumerates **all** linear spaces of the type (the mode-0 search run to exhaustion; the
   symmetry breaking only removes relabellings) and prints the orientable ones.
2. `scripts/canon_dedupe.py` reduces them to isomorphism classes by an exact canonical form (for types with a unique
   largest block); `scripts/dedupe_enum.py` does the same with graph isomorphism (networkx VF2 on the point–block
   incidence graph) and serves as a cross-check.
3. `scripts/algebraic_nonrealizability.py` proves, for one linear space, that no realization with exactly its
   collinearities exists: with four points fixed as projective frame, the collinearity determinants generate an
   ideal $I$; the program finds (numerically, from real and complex least-squares solutions) a few non-collinear
   triples $T_1, \dots, T_r$ and then verifies **exactly** (sympy Gröbner basis over $\mathbb Q$) that
   $I + (t\, d_{T_1} \cdots d_{T_r} - 1)$ is the unit ideal. By Rabinowitsch's trick this means that every complex
   point of $V(I)$ has one of the $T_i$ collinear. `scripts/prove_type.py` runs this for every class and writes the
   certificates to `data/proofs/`.

Validation: the non-Pappus configuration is proved non-realizable in 7 s, with $T$ = the Pappus line.

## Timings at a glance

| computation | size | time |
|---|---|---|
| combinatorial sieve, $n = 11$ | 619 types | 6 s (12 threads) |
| combinatorial sieve, $n = 12$ | 1286 types | 71 s (11 threads) |
| SAT cross-check, $n = 10$ | 295 types | 12 s (2 processes) |
| SAT cross-check, $n = 12$ | 1286 types | 5.4 h (2 processes) |
| verification of all certificates | 1332 certificates | 1.3 s |
| orientability, $\{4, 3^{14}\}$ at $n = 11$ (engine mode 4) | | 126 s |
| orientability, $\{4^3, 3^{14}\}$ at $n = 12$ (engine mode 4, non-orientable) | | 88 min |
| orientability, $\{4^5, 3^9\}$ at $n = 12$ (engine mode 4) | | unfinished after 4 h |
| orientability by SAT, $\{3^{18}\}$ at $n = 12$ (orientable) | | 2 s |
| all orientable linear spaces of $\{6, 3^{14}\}$ (engine mode 5) | 135 360 labelled | 38 min |
