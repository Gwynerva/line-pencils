# Verification

How the terms of the four sequences a(n), b(n), c(n) and d(n) were obtained and how to check them independently.

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
* **a(n)** — the number of multisets {k_1, ..., k_r} with 3 ≤ k_i ≤ n allowed by arithmetic alone:
  Σ k_i(k_i−1)/2 ≤ n(n−1)/2. This is A072964(n−1) and is listed for comparison only.
* **d(n)** — the number of different possible numbers of intersection points of n lines. For example, four lines
  have 1, 4 or 6 intersection points and nothing else, so d(4) = 3.

The list with no point on three or more lines (general position) is counted. The sequences start at n = 1: one line
has no intersection point, so b(1) = c(1) = d(1) = 1, with 0 the only possible number of points. Working in the real
projective plane gives the same answers, since a projective transformation can move the line at infinity away from
the finitely many intersection points.

## Terms

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a(n) | 1 | 1 | 2 | 4 | 7 | 15 | 32 | 66 | 141 | 295 | 619 | 1286 | 2654 | 5460 | 11066 |
| b(n) | 1 | 1 | 2 | 3 | 5 | 9 | 17 | 29 | 56 | 106 | 202 | 384 | 729 | 1357 | 2558 |
| c(n) | 1 | 1 | 2 | 3 | 5 | 9 | 16 | 28 | 53 | 98 | 180 | 336 | 620–659 | 1104–1229 | — |
| d(n) | 1 | 1 | 2 | 3 | 5 | 9 | 13 | 18 | 24 | 30 | 38 | 46 | 56 | 65–66 | 76–77 |

The corresponding OEIS entries are [A400149](https://oeis.org/A400149), [A399464](https://oeis.org/A399464)
and [A399605](https://oeis.org/A399605). The table above includes the published extension of b(n) and the current geometric bounds.

## How each term is established

**b(n), n ≤ 12.** For every arithmetically admissible multiset an exhaustive backtracking search decides whether blocks of the
given sizes can be placed on n points with pairwise intersections of size at most one (`engine/ls.c`, mode 0; the
search extends the first uncovered pair of points and breaks the symmetry of unused points). Every query terminated;
the results are in `runs/comb_{n}.json`. An independent formulation as a SAT problem (`scripts/sat_linear_space.py`,
CaDiCaL) returns the same answer for every multiset with n ≤ 12.

**b(n), n = 13–15.** [Mark Kim's preprint](https://doi.org/10.5281/zenodo.24567131), Theorem 1.1, supplies these terms.
Run `python scripts/kim_results.py` to check the [published tables](https://github.com/marik-11/linear_space_types/tree/e126faeb3f621ef4c85e3872c320a27a901f229e)
against the candidate sets and available local verdicts, and to check the geometric exclusions. A fresh run at n = 14
agreed on all 4843 verdicts. The n = 15 term cites Kim's published computation.

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
  relations), which every real arrangement has (`engine/ls.c`, mode 4, `runs/orient_{n}.json`; the SAT encoding
  `scripts/sat_orient.py`, `runs/sat_orient_{n}.json`);
* a theorem: the unique linear space of type {4^9} on 12 points is the dual of the Hesse configuration AG(2,3), excluded by the
  Sylvester–Gallai theorem (`data/exclusions.json`); for {6,4,3^12} and {6,3^14} every orientable linear space has a
  stored cofactor identity, checked by `verify.py --algebraic`, showing that any realization carries an extra
  collinearity (`data/proofs/`);
* a computation for {3^20}: its linear spaces on 12 points are exactly the Steiner triple systems of order 13 with
  one point deleted; all 26 deletions of the two such systems are non-orientable (`scripts/orchard12.py`). This agrees
  with the orchard number 19 for 12 points (A003035);
* a computation for {4^5, 3^9}: the five 4-pencils can sit in only 8 ways on 12 lines, and for each of them SAT shows
  that no linear space of the type admits a chirotope; three solvers agree (`scripts/orient_split.py`,
  `runs/orient_split_12.json`);
* for n = 13, the band theorem (`notes/bands.md`): a type whose largest pencil has n − k lines must come from a type of
  k lines by absorbing points (`data/exclusions.json`, kind `theorem`).

Each multiset gets exactly one verdict in the classification file. The names used there are:

| verdict | meaning |
|---|---|
| `real` | a certificate exists and is accepted by the verifier |
| `no-linear-space` | the combinatorial search says NO (also counted out of b(n)) |
| `melchior`, `csima-sawyer` | the inequality of that name fails |
| `debruijn-erdos` | fewer than n intersection points without a pencil of all n lines (supported, never the only reason) |
| `non-orientable` | linear spaces exist, but none admits a chirotope |
| `theorem`, `non-realizable-proved` | excluded by one of the theorems or computations above |
| `literature` | excluded by a published theorem not re-proved here (supported; no type currently needs it) |
| `open` | none of the above; the term is then given as an interval |

**d(n).** The attained values are read off the certificates. The missing values are excluded by: the loss argument
(n(n−1)/2 − 1 and n(n−1)/2 − 3 never occur, since a point on k lines removes k(k−1)/2 − 1 points and 1, 3 are not sums
of 2, 5, 9, ...); the de Bruijn–Erdős theorem (fewer than n points only for a pencil); Elliott's theorem (for n ≥ 10,
between n and 2n−4 only n itself); and, for the remaining values, the classification of all multisets with that
number of points (`notes/points.md` contains the proofs, including a theorem excluding 2n−3 for all n ≥ 13).
At n = 14 and 15, filtering Kim's tables by Melchior's inequality excludes 27 points and 29–30 points, respectively.
Three additional exact witnesses for n = 15 are in `data/certificates/n15_points.json`.

## Checking

```
git clone https://github.com/Gwynerva/line-pencils.git
cd line-pencils
python verifier/verify.py --self-test
python verifier/verify.py data/certificates/n*.json
python scripts/classify.py 13
python scripts/kim_results.py
```

- `--self-test` runs the verifier's tests. The command with `data/certificates/n*.json` checks coordinates and reports
  `verified 2457 certificates, 0 rejected`. It finds 1104 distinct certified types for 14 lines and checks three
  witnesses for 15 lines.
- `classify.py 13` rebuilds local verdicts from the certificates, theorem filters, and search logs. It then writes
  the sequence summary in `data/results/`, with Kim's published terms and the known bounds.
- `kim_results.py` checks the published classifications, compares them with available local results, and verifies
  the intersection-count exclusions. Use `--kim-dir DIRECTORY` to read local copies of Kim's tables.

These commands use Python 3.10 or later and the standard library.

The certificate files can also be compared with `data/CHECKSUMS.txt` (`sha256sum -c data/CHECKSUMS.txt`).

Two kinds of non-realizability proofs can also be checked without trusting the program that found them:

```
python verifier/verify.py --algebraic data/proofs/n*.json
python scripts/sat_proof.py check
```

The first checks {6,4,3^12} and {6,3^14} (Theorems C4, C5). For every orientable linear space of the type, the file
stores polynomials h_T, h with 1 = Σ h_T d_T + h·(t·g − 1), where the d_T are the collinearity determinants of the
triples inside blocks and g is the product of the determinants of a few non-collinear triples. The verifier rebuilds
the d_T and checks the identity by exact expansion, using the standard library only. So every complex solution of
the collinearities has g = 0, which is an extra collinearity.

The second checks {3^20} and {4^5,3^9} (Propositions C3a, C3b). It rebuilds the 34 SAT instances listed in
`data/proofs/lrat_n12.json`, compares each CNF with its stored SHA-256, solves it with CaDiCaL writing an LRAT proof,
and checks the proof with cake_lpr. cake_lpr is a proof checker whose correctness is proved in HOL4 (CakeML). It
needs `cadical` (2.1.3) and `cake_lpr` on PATH and `pip install python-sat==1.9.dev17`; it takes about a minute. The
proofs (108 MB) are regenerated rather than stored. CI runs both checks on pushes and pull requests.

Not covered by any certificate: verdicts that come only from the exhaustive search `engine/ls.c`. These are the
combinatorial sieve (b(n)), the other 15 non-orientable types at n = 12, and the completeness of the list of
orientable linear spaces used in C4 and C5.

* The sieve is cross-checked by an independent SAT encoding for every n ≤ 12.
* For the 15 non-orientable types, the SAT encoding of the whole type was tried on 12 of them with a limit of one
  hour each. Only {5^2,3^13} finished, and it agrees with the engine (unsatisfiable).
* The isomorphism classes of the enumeration are computed by two independent tests (VF2 graph isomorphism and a
  canonical form), which agree.

The reductions to cases (Steiner triple systems for {3^20}, the 8 configurations of 4-pencils for {4^5,3^9}) are
short arguments, written out in the proofs.

To repeat a search instead of reading its log: compile the engine with `gcc -O2 -o engine/ls engine/ls.c` and run
`python scripts/engine_run.py 12 0 120 out.json` (all 1286 multisets for n = 12; 384 answers YES).

## Example

`data/certificates/n10.json`, type [5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], d = 5: a regular pentagram together with its five
axes of symmetry. One point lies on five lines, ten points on three, five points on two. `scripts/pentagon.py` shows
by a Gröbner-basis computation that this type has exactly two realizations up to projective equivalence, conjugate
under √5 ↦ −√5; no realization with rational coordinates exists.

## Planes in space

The side direction on arrangements of planes (`docs/planes.md`, `notes/planes.md`) has its own independent
verifier: `python scripts/planes_verify.py` recomputes the type of every plane certificate in
`runs/planes_certificates.json` in exact integer arithmetic and confirms 1, 1, 2, 4, 8, 20, 55, 198 types for n ≤ 8.

## Contributors

See [Who contributed](docs/about.md#who-contributed) for the roles of the people and AI agents who worked on the project.
