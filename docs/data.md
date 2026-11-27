---
description: "Where the data are and how to check them yourself: exact certificates for every drawable type and a small verifier that rechecks them all."
---

# Data and verification

All data behind the site can be checked independently. This page describes where the data are, their formats,
the verifier that checks every certificate, and how to run it.

[![verify certificates](https://github.com/Gwynerva/line-pencils/actions/workflows/verify.yml/badge.svg)](https://github.com/Gwynerva/line-pencils/actions/workflows/verify.yml)

## Checking everything

```bash
git clone https://github.com/Gwynerva/line-pencils.git
cd line-pencils
python verifier/verify.py --self-test                 # the verifier's own tests (Pappus, Desargues, pentagram, corrupted certificates)
python verifier/verify.py data/certificates/n*.json   # every certificate: exit code 0 iff all verify
python scripts/classify.py 13                         # recompute the four sequences from certificates + logs
python verifier/verify.py --algebraic data/proofs/n*.json   # cofactor identities of Theorems C4, C5
python scripts/sat_proof.py check                     # LRAT proofs of C3a, C3b (needs cadical and cake_lpr)
```

Python 3.10+ and nothing else is needed for the first four commands; the last one also needs `cadical` and
`cake_lpr` (built as in the CI job `lrat-proofs`). Re-running the *searches* needs a C compiler
(`gcc -O2 -o engine/ls engine/ls.c`) and, for the SAT cross-checks and the realizer, `pip install python-sat numpy scipy`.
The same verification runs in GitHub Actions on every push (badge above).

## The certificate format

One JSON file per $n$, `data/certificates/n{n}.json`, a list of certificates:

```json
{"n": 10,
 "type": [5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
 "d": 5,
 "lines": [[[a0,a1],[b0,b1],[c0,c1]], ...],
 "source": "how it was found"}
```

* `type`: the pencil sizes $\ge 3$, any order.
* `d`: $0$ for rational coordinates, otherwise a positive non-square integer; all numbers live in $\mathbb Q(\sqrt d)$.
* `lines`: $n$ lines $ax + by + cz = 0$ of $\mathbb{RP}^2$, each coefficient an integer pair $[p_0, p_1]$ meaning $p_0 + p_1\sqrt d$.
  Projective coordinates are scaled to integers, so no denominators ever occur. (By duality these are also the
  coordinates of $n$ points; the type is then the multiset of sizes of the lines through $\ge 3$ of them.)

Certificates were produced by Petra Radko's original exploratory search (`source` begins with `legacy search`; the
program itself is not in the repository) or by the
constructions of this project (`source` names the method). The provenance does not matter: **only the verifier's
acceptance counts.**

## The verifier

`verifier/verify.py` uses the Python standard library only. What it does, in order:

1. Checks that `d` is $0$ or a positive non-square integer and that every coefficient is a pair of Python integers
   (arbitrary precision; `True` and floats are rejected). For $d = 0$ the second components must be $0$.
2. Arithmetic in $\mathbb Z[\sqrt d]$ is implemented by three one-line functions (add, subtract, multiply pairs).
   The only mathematical fact used: *if $d$ is a positive integer that is not a perfect square and $p_0, p_1$ are integers,
   then $p_0 + p_1\sqrt d = 0$ implies $p_0 = p_1 = 0$* (otherwise $\sqrt d = -p_0/p_1$ would be rational). Hence a zero test is
   exact: compare the two integer components with $0$.
3. Every line must be a non-zero vector; every two lines must be non-proportional (cross product non-zero, exactly).
4. For every pair $i < j$ the intersection point $P = L_i \times L_j$ is computed exactly, and the pencil through $P$ is
   the set of **all** $k$ with $L_k \cdot P = 0$. Pencils are thus maximal concurrent sets computed from scratch, never
   assembled by merging pairs. The distinct sets found are the intersection points; their sizes are the $t_k$.
5. Sanity: $\sum_S \binom{|S|}2 = \binom n2$ (every pair of lines in exactly one pencil).
6. The multiset of sizes $\ge 3$ must equal `type`.

Why this is enough is Theorem D1 on the [theorems page](theorems.md). Why this is trustworthy: the code is short
enough to be read in full, has no dependencies, uses no floating point, and is exercised by tests that include
hundreds of corrupted certificates (every single coordinate of the Pappus, Desargues and pentagram certificates
changed by $\pm1$; random perturbations; wrong `d`; duplicated lines; wrong type; float or boolean entries) — all of
which must be rejected, and are. The verifier also reports duplicate types and a per-$n$ count of distinct types,
which is how the lower bounds for $c(n)$ are read off.

```bash
python verifier/verify.py data/certificates/n*.json
# verified 2454 certificates, 0 rejected
# distinct realizable types per n: {3: 2, 4: 3, 5: 5, 6: 9, 7: 16, 8: 28, 9: 53, 10: 98, 11: 180, 12: 336, 13: 620, 14: 1104}
```

## Impossibility records

Non-realizability is never asserted without a reason that can be checked:

| reason | where recorded | how to re-check |
|---|---|---|
| no linear space (combinatorial sieve) | `runs/comb_{n}.json` (`"status": "NO"`, with node counts), `runs/sat_{n}.json` | re-run Algorithm 1 or 2 ([algorithms](algorithms.md)) |
| Melchior / Csima–Sawyer / de Bruijn–Erdős | computed from the type by `scripts/pencils.py` | one line of arithmetic |
| no orientable linear space | `runs/orient_{11,12}.json` (engine mode 4), `runs/sat_orient_*.json` | re-run Algorithm 3 |
| orientable, but no realization ($\{6, 4, 3^{12}\}$, $\{6, 3^{14}\}$) | `data/proofs/n12_*.json`: every orientable linear space with the triples, the frame and explicit cofactors $h_T, h$ with $1 = \sum_T h_T d_T + h\,(t\,g - 1)$, $g = d_{T_1} \cdots d_{T_r}$ | `python verifier/verify.py --algebraic data/proofs/n*.json` checks the identity by exact expansion ([algorithms](algorithms.md), §8) |
| none of the linear spaces is orientable: $\{3^{20}\}$, $\{4^5, 3^9\}$ | `data/proofs/lrat_n12.json`: 34 SAT instances (26 point deletions of STS(13), 8 cases of $\{4^5, 3^9\}$) with the SHA-256 of each CNF | `python scripts/sat_proof.py check` rebuilds each CNF, solves it with CaDiCaL writing an LRAT proof, and checks the proof with the verified checker cake_lpr ([algorithms](algorithms.md#lrat)) |
| theorem or recorded computation (e.g. $\{4^9\}$; the band theorem at $n = 13$) | `data/exclusions.json` with statement and reference | read the proof / re-run the script |

What each check covers. The certificate verifier, the cofactor check and cake_lpr each check one step completely, so
the solver or computer algebra system that produced the step need not be trusted. Every verdict that comes only
from the exhaustive search `engine/ls.c` has no certificate: the combinatorial sieve, the orientability verdicts
(including the 15 non-orientable types at $n = 12$ other than $\{3^{20}\}$ and $\{4^5, 3^9\}$), and the enumeration
of all orientable linear spaces behind Theorems C4 and C5. For the combinatorial sieve and for orientability at $n \le 11$ a
second, independent implementation (SAT) agrees wherever both finished; the 15 other non-orientable types at $n = 12$
and the enumeration behind C4 and C5 rest on the engine alone (the isomorphism step has two implementations).

`data/results/classification_n{n}.json` lists, for every admissible type, its $f_0$, whether a linear space exists,
the verdict reached by the local computations and its reason. `data/results/sequences.json` holds the four sequences, including the published extension below.

## Kim's classifications

[Mark Kim's preprint](https://doi.org/10.5281/zenodo.24567131) supplies the combinatorial terms through $n=15$. The project's local classification
for $n=13$ records which types its own search settled. For the full combinatorial classifications at $n=13,14,15$,
see the [pinned upstream tables](https://github.com/marik-11/linear_space_types/tree/e126faeb3f621ef4c85e3872c320a27a901f229e).
Run `python scripts/kim_results.py` to check candidate coverage, counts, consistency with the local results and the
consequences of Melchior's inequality. Pass `--kim-dir DIRECTORY` to use a local copy of the tables. The same option works
with `python scripts/oeis_afiles.py` to generate the supplementary A400149 table through $n=15$.

## Logs

Every long run writes a JSON checkpoint after each answer (`runs/*.json`) and a text log (`runs/*.log`) with the
command line, per-query times and the engine's node counts, so that a `NO` can be traced to a specific exhaustive
search of known size. Engine version: `engine/ls.c` at the commit that produced the log (the repository history is the
record).

## Checksums

`data/CHECKSUMS.txt` holds the SHA-256 checksums of the certificate files; continuous integration checks them on every
push, and so can you:

```bash
sha256sum -c data/CHECKSUMS.txt
```

The checksums are of the files as stored in the repository, with Unix line endings. On a Windows checkout that
converts line endings, check out with `git config core.autocrlf false` first.
