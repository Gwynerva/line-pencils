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
timed out, and the 17 of them that mattered for $c(13)$ were decided by the SAT encoding of §2. Re-running 29 of the
time-outs with 3600 s per query decided 28 of them (15 `YES`, 13 `NO`), leaving 43 time-outs in that run. Those local searches tested selected types for $c(13)$. Mark Kim's separate exhaustive search
covers all combinatorial candidates and establishes $b(13)=729$, $b(14)=1357$ and $b(15)=2558$
([preprint](https://doi.org/10.5281/zenodo.24567131), [scope and verification](sequences/combinatorial.md#mark-kims-extension-to-15-points)).

**Command.**
```bash
python scripts/engine_run.py 12 0 120 runs/comb_12.json --workers 11
```

## 2. The combinatorial sieve, independently: SAT

`scripts/sat_linear_space.py` encodes the same question for CaDiCaL (via python-sat): a Boolean variable $x_S$ for
every $k$-subset $S$ of the points and every needed size $k$; "exactly $t_k$ true variables among the $k$-subsets"
(sequential-counter cardinality encodings); "at most one true variable among the subsets containing a given pair"
(66 pairs for $n = 12$); and the first block of the largest size fixed to $\{0, \dots, k-1\}$. Each constraint corresponds to a block count, a pair of points, or a choice of labels. The encoding agrees with the
exhaustive search on all 295 types for
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
(`runs/orient_11.json`). At $n = 12$ the engine decided all candidates but one: the
search for $\{4^5, 3^9\}$ did not finish within four hours. That type is settled by splitting it into the 8 possible
configurations of its five 4-pencils and running the SAT encoding on each with the 4-pencils fixed; every case is
refuted within a minute (`scripts/orient_split.py`, [Proposition C3b](theorems.md#c3b)).

```bash
python scripts/engine_run.py 11 4 1800 runs/orient_11.json --workers 2 --only "4,3,3,3,3,3,3,3,3,3,3,3,3,3,3;..."
python scripts/sat_orient.py 12 runs/sat_orient_12.json --workers 2 --only "..."
```

### Checkable UNSAT proofs {#lrat}

A `NO` from a SAT solver is only as good as the solver. For the SAT verdicts that $c(12)$ rests on, the solver is
taken out of the trusted base: each instance is written as a DIMACS CNF, the standalone CaDiCaL 2.1.3 writes an LRAT
proof of unsatisfiability (`--lrat`), and the proof is checked by **cake_lpr**, a checker produced by the CakeML
compiler whose correctness is proved in HOL4 down to the machine code (if it prints `s VERIFIED UNSAT`, the CNF has
no satisfying assignment). `scripts/sat_proof.py` does this; the three SAT scripts have a `--proof DIR` option that
does it for every `NO` they produce.

The proofs are not stored: 34 of them take 108 MB, while regenerating and checking all of them takes under two minutes (85 s on 4 processes).
Instead `data/proofs/lrat_n12.json` lists every instance with what it encodes, the SHA-256 of its CNF and the size of
its proof. The CNF is a deterministic function of the encoder (with python-sat 1.9.dev17, whose cardinality encodings
are part of it), and CaDiCaL is deterministic too: the proofs come out byte for byte the same on every run. The CI
job `lrat-proofs` builds both tools from pinned sources, rebuilds every CNF, compares the hash, solves and checks.

```bash
python scripts/sat_proof.py check            # needs cadical and cake_lpr on PATH (or $CADICAL, $CAKE_LPR)
python scripts/sat_proof.py cnf C3b_case3 case3.cnf    # one instance, for any other solver or checker
```

What the proofs cover and what they do not:

| claim | covered by LRAT + cake_lpr | still trusted |
|---|---|---|
| Proposition C3a, $\{3^{20}\}$ | the 26 point deletions of the two STS(13), each non-orientable | the encoding of §3; that there are exactly two STS(13) (Colbourn–Rosa); that every linear space of type $\{3^{20}\}$ is a point deletion (the short argument in the proof) |
| Proposition C3b, $\{4^5, 3^9\}$ | the 8 cases with fixed 4-pencils, each non-orientable | the encoding; the reduction to 8 cases (`families()`, `canon()`, `blocks_of()` in `scripts/orient_split.py`) |
| the 15 other non-orientable types at $n = 12$ | nothing yet: SAT on the whole type is too slow (see below) | the exhaustive search of `engine/ls.c`, mode 4 |
| everything decided only by `engine/ls.c` (the combinatorial sieve, orientability at $n \le 11$, the enumeration of all orientable linear spaces in §8) | nothing: an exhaustive search emits no certificate | the engine; where the SAT encoding of §2 or §3 agrees, the two independent implementations |

The 15 non-orientable types at $n = 12$ are decided by the engine. The SAT encoding of the whole type, without a
case split, is too hard for checkable proofs. In a trial on 12 cores, 12 of the 15 instances (and $\{3^{20}\}$ as a
whole type) were run with a limit of one hour each. Only $\{5^2, 3^{13}\}$ finished, after 35 minutes, and it is
unsatisfiable, in agreement with the engine. The LRAT proofs grow by about 50 MB per minute of solving, so they are
not covered yet. A case split like that of Proposition C3b would make each case small, but it would add a reduction
argument to the trusted part.

## 4. Finding examples

Realizable types are proved realizable by exhibiting coordinates. The following sources were used:

1. **Rich point sets** (Petra Radko's original exploratory search, which predates this repository): subsets of integer grids, regular polygons
   with their points at infinity ($\mathbb Q(\sqrt 2), \mathbb Q(\sqrt 3), \mathbb Q(\sqrt 5)$), rational torsion points
   of elliptic curves (orders 7–12), and intersections of their lines; simulated annealing over $n$-subsets looking for
   a target type. All examples for $n \le 11$, all but one for $n = 12$ ($\{3^{18}\}$, item 5) and all but 23 for
   $n = 13$ were found this way; the arrangements of 14 lines come from items 4 and 5.
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
   These produced three types for $n = 13$ and the first arrangements of 14 lines.
5. <a id="zone-walk"></a>**Zone walk** (`scripts/zone_walk.py`): a new line is a point of the dual plane, which the dual lines of
   the intersection points cut into cells, edges and vertices; the type of the extended arrangement depends only on
   which intersection points the new line passes through, so one line per class suffices. Starting from two lines, the
   walk inserts a line into every class and re-inserts every line of every kept arrangement, keeping a few
   realizations of different combinatorics per type, in exact integer arithmetic (or over $\mathbb Z[\sqrt d]$ when
   started from irrational certificates). Without any combinatorial input it finds every type for $n \le 12$ that has
   a rational realization, including $\{3^{18}\}$ (Example C3c); it found 18 of the 20 new types for $n = 13$ and
   1104 types for $n = 14$.
6. **Targeted deformation** (`scripts/targeted.py`): for a target type, a certified arrangement with one or two lines
   fewer is deformed inside its own type (minimum-norm Gauss–Newton) until chosen intersection points become collinear,
   and new lines are put through them; exact coordinates are recovered as in item 2. Quadratic irrationalities appear
   by themselves: from rational arrangements it rebuilds $\{5, 3^{10}\}$, which needs $\sqrt 5$, and $\{3^{16}\}$, known only
   over $\mathbb Q(\sqrt 5)$, and
   it found $\{5^3, 4^2, 3^7\}$ for $n = 13$.
7. **Sections of mirror arrangements** (`scripts/mirror_sections.py`): the reflection hyperplanes of a 4-dimensional
   root system (A4, D4, B4, F4, H4) cut a 3-dimensional subspace in a line arrangement; symmetric subspaces (the
   mirrors themselves, directions contained in several mirrors) give the most coincidences. Subsets of $n$ lines are
   grown around the richest points. The restriction of H4 to one of its mirrors is the arrangement of the 31 planes
   perpendicular to the symmetry axes of the icosahedron, and 13 of them have type $\{4^9\}$, which is impossible for
   12 lines. What else was tried, and did not help, is summarised in `notes/constructions.md`.

```bash
python scripts/find_examples.py 12 "6,3,3,3,3,3,3,3,3,3,3,3,3,3,3" --max 400 --time 2400
python scripts/zone_walk.py 12 --save zw12.json        # about 15 min; finds {3^18}
python scripts/targeted.py 13 "5,5,5,4,4,3,3,3,3,3,3,3" --stock zw12.json
python scripts/orient_split.py                         # Proposition C3b
```

## 5. Verification

`verifier/verify.py` — described on the [data page](data.md). Standard library only, exact arithmetic in
$\mathbb Z[\sqrt d]$, all pencils recomputed as maximal concurrent sets from scratch. With `--algebraic` it checks
the cofactor identities of §8 (exact polynomial arithmetic over $\mathbb Q$). The LRAT proofs of §3 are checked by
cake_lpr, not by this program.

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

Four steps, chained (details and the proof of correctness in `notes/nonrealizability.md`):

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
4. `scripts/algebraic_nonrealizability.py --cofactors FILE` makes the Gröbner computation checkable: Singular's
   `lift` gives explicit polynomials $h_T$ (one per collinear triple $T$ inside a block, with determinant $d_T$) and
   $h$ such that $1 = \sum_T h_T\, d_T + h \cdot (t\, d_{T_1} \cdots d_{T_r} - 1)$, an identity in $\mathbb Q[\text{unknowns}, t]$, stored with each class. `python verifier/verify.py --algebraic
   data/proofs/n*.json` (standard library only) rebuilds the $d_T$ from the blocks and the frame itself and checks
   the identity by exact expansion with `fractions`. The identity is a direct witness for the unit ideal, so neither
   sympy nor Singular needs to be trusted. The cofactors are small: 62 to 138 terms per class.

Validation: the non-Pappus configuration is proved non-realizable in 7 s, with $T$ = the Pappus line.

Step 4 checks step 3 completely. Steps 1 and 2 are not covered by a certificate: that the listed classes are *all*
the orientable linear spaces of the type rests on the exhaustive enumeration of the engine and on the isomorphism
test (two independent implementations).

## Recorded timings

| computation | size | time |
|---|---|---|
| combinatorial sieve, $n = 11$ | 619 types | 6 s (12 threads) |
| combinatorial sieve, $n = 12$ | 1286 types | 71 s (11 threads) |
| SAT cross-check, $n = 10$ | 295 types | 12 s (2 processes) |
| SAT cross-check, $n = 12$ | 1286 types | 5.4 h (2 processes) |
| certificate verification before the three 15-line witnesses were added | 2454 certificates | 3.6 s |
| orientability, $\{4, 3^{14}\}$ at $n = 11$ (engine mode 4) | | 126 s |
| orientability, $\{4^3, 3^{14}\}$ at $n = 12$ (engine mode 4, non-orientable) | | 88 min |
| orientability, $\{4^5, 3^9\}$ at $n = 12$ (engine mode 4) | | unfinished after 4 h |
| orientability by SAT, $\{3^{18}\}$ at $n = 12$ (orientable) | | 2 s |
| orientability by SAT, $\{4^5, 3^9\}$ split into 8 cases (non-orientable) | 8 cases × 3 solvers | under 1 min per case |
| LRAT proofs for C3a and C3b: build, CaDiCaL, cake_lpr | 34 instances, 108 MB of proofs | 85 s (4 processes) |
| cofactor identities of Theorems C4, C5 (`verify.py --algebraic`) | 5 classes | 0.2 s |
| zone walk from two lines to $n = 12$ / $n = 13$ | 333 / 613 types | 12 min / 40 min |
| $\{4^9\}$ at $n = 13$ from the H4 sections (`--seed 1`) | | 20 s |
| all orientable linear spaces of $\{6, 3^{14}\}$ (engine mode 5) | 135 360 labelled | 38 min |
