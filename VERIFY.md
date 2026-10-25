# Verification

How the terms of the three sequences were obtained and how to check them independently.

## Definitions

Draw n lines in the plane, no two parallel. Some intersection points may lie on three or more lines. For each
arrangement, list how many lines pass through each intersection point.

* **c(n)** — the number of different ways n lines can meet, that is, the number of different lists obtained over all
  arrangements of n lines. Two arrangements meet in the same way when their lists agree up to order. Points on exactly two lines may be
  left out of the list, since their number is determined by the rest.
* **b(n)** — the number of different ways n lines can meet that are consistent with the single rule that two lines
  meet only once, whether or not the lines can actually be drawn. Formally: multisets {k_1, ..., k_r} with
  3 ≤ k_i ≤ n for which there are subsets B_1, ..., B_r of an n-element set with |B_i| = k_i and |B_i ∩ B_j| ≤ 1
  for i ≠ j.
* **d(n)** — the number of different possible numbers of intersection points of n lines. For example, four lines
  have 1, 4 or 6 intersection points and nothing else, so d(4) = 3.

The list with no point on three or more lines (general position) is counted. The sequences start at n = 1: one line
has no intersection point, so b(1) = c(1) = d(1) = 1, with 0 the only possible number of points. Working in the real
projective plane gives the same answers, since a projective transformation can move the line at infinity away from
the finitely many intersection points.

## Terms

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| b(n) | 1 | 1 | 2 | 3 | 5 | 9 | 17 | 29 | 56 | 106 | 202 | 384 | ≥ 662 |
| c(n) | 1 | 1 | 2 | 3 | 5 | 9 | 16 | 28 | 53 | 98 | 180 | 335–337 | 600–659 |
| d(n) | 1 | 1 | 2 | 3 | 5 | 9 | 13 | 18 | 24 | 30 | 38 | 46 | 56 |

Only exact values are submitted: b(n) for n ≤ 12, c(n) for n ≤ 11, d(n) for n ≤ 13. For comparison, the number of
multisets allowed by arithmetic alone (sum of k_i(k_i−1)/2 at most n(n−1)/2) is A072964(n−1):
1, 1, 2, 4, 7, 15, 32, 66, 141, 295, 619, 1286, 2654.

## How each term is established

**b(n).** For every arithmetically admissible multiset an exhaustive backtracking search decides whether blocks of the
given sizes can be placed on n points with pairwise intersections of size at most one (`engine/ls.c`, mode 0; the
search extends the first uncovered pair of points and breaks the symmetry of unused points). Every query terminated;
the results are in `runs/comb_{n}.json`. An independent formulation as a SAT problem (`scripts/sat_linear_space.py`,
CaDiCaL) returns the same answer for every multiset with n ≤ 12.

**c(n).** Each realizable type is certified by explicit coordinates of n lines (`data/certificates/n{n}.json`): the
coefficients of ax + by + cz = 0 as integers, or as integer pairs p + q√d for a non-square d. The program
`verifier/verify.py` recomputes the pencil type of each certificate in exact arithmetic (intersection points by cross
products, pencils as maximal concurrent sets, no floating point) and accepts it only if the type matches. Each
non-realizable multiset is excluded by one of the following, recorded per multiset in
`data/results/classification_n{n}.json`:

* no linear space exists (the search above);
* Melchior's inequality t_2 ≥ 3 + Σ_{k≥4} (k−3) t_k or the Csima–Sawyer bound t_2 ≥ 6n/13 fails, where
  t_2 = n(n−1)/2 − Σ k_i(k_i−1)/2;
* no linear space of the type admits a chirotope (an orientation satisfying the three-term Grassmann–Plücker
  relations), which every real arrangement has (`engine/ls.c`, mode 4; `runs/orient_{n}.json`);
* a theorem: the unique linear space of type {4^9} on 12 points is the dual of the Hesse configuration AG(2,3), excluded by the
  Sylvester–Gallai theorem (`data/exclusions.json`); for {6,4,3^12} and {6,3^14} every orientable linear space has a
  Gröbner-basis certificate that any realization carries an extra collinearity (`data/proofs/`);
* a computation for {3^20}: its linear spaces on 12 points are exactly the Steiner triple systems of order 13 with
  one point deleted; all 26 deletions of the two such systems are non-orientable (`scripts/orchard12.py`). This agrees
  with the orchard number 19 for 12 points (A003035).

Each multiset gets exactly one verdict in the classification file. The names used there are:

| verdict | meaning |
|---|---|
| `real` | a certificate exists and is accepted by the verifier |
| `no-linear-space` | the combinatorial search says NO (also counted out of b(n)) |
| `melchior`, `csima-sawyer` | the inequality of that name fails |
| `non-orientable` | linear spaces exist, but none admits a chirotope |
| `theorem`, `non-realizable-proved` | excluded by one of the theorems or computations above |
| `open` | none of the above; the term is then given as an interval |

**d(n).** The attained values are read off the certificates. The missing values are excluded by: the loss argument
(n(n−1)/2 − 1 and n(n−1)/2 − 3 never occur, since a point on k lines removes k(k−1)/2 − 1 points and 1, 3 are not sums
of 2, 5, 9, ...); the de Bruijn–Erdős theorem (fewer than n points only for a pencil); Elliott's theorem (for n ≥ 10,
between n and 2n−4 only n itself); and, for the remaining values, the classification of all multisets with that
number of points (`notes/points.md` contains the proofs, including a theorem excluding 2n−3 for all n ≥ 13).

## Checking

```
git clone https://github.com/Gwynerva/line-pencils.git
cd line-pencils
python verifier/verify.py --self-test
python verifier/verify.py data/certificates/n*.json
python scripts/classify.py 13
```

The first command runs the verifier's own tests. The second prints `verified 1332 certificates, 0 rejected` and the
number of distinct certified types for each n: 2, 3, 5, 9, 16, 28, 53, 98, 180, 335, 600 for n = 3, ..., 13, plus 3
sample arrangements for n = 14 used on the site.

The third recomputes all four sequences from the certificates, the theorem filters and the search logs. For each n it
prints the four terms and how many multisets received each verdict, then the four sequences, with an interval
`[low, high]` wherever a term is not exact. It stops with an error if any certificate fails or if two searches
disagree. Python 3.10 or later is the only requirement.

The certificate files can also be compared with `data/CHECKSUMS.txt` (`sha256sum -c data/CHECKSUMS.txt`).

To repeat a search instead of reading its log: compile the engine with `gcc -O2 -o engine/ls engine/ls.c` and run
`python scripts/engine_run.py 12 0 120 out.json` (all 1286 multisets for n = 12; 384 answers YES).

## Example

`data/certificates/n10.json`, type [5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], d = 5: a regular pentagram together with its five
axes of symmetry. One point lies on five lines, ten points on three, five points on two. `scripts/pentagon.py` shows
by a Gröbner-basis computation that this type has exactly two realizations up to projective equivalence, conjugate
under √5 ↦ −√5; no realization with rational coordinates exists.

## Authorship

The questions were posed by Petra Radko. The programs, computations, proofs and texts were produced by Claude Code
(Anthropic). The complete write-up is at
https://gwynerva.github.io/line-pencils/.
