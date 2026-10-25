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
```

Python 3.10+ and nothing else is needed for these three commands. Re-running the *searches* needs a C compiler
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

Certificates were produced by the author's original search (`source` begins with `legacy search`) or by the
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
# verified 1332 certificates, 0 rejected
# distinct realizable types per n: {3: 2, 4: 3, 5: 5, 6: 9, 7: 16, 8: 28, 9: 53, 10: 98, 11: 180, 12: 335, 13: 600, 14: 3}
```

## Impossibility records

Non-realizability is never asserted without a reason that can be checked:

| reason | where recorded | how to re-check |
|---|---|---|
| no linear space (combinatorial sieve) | `runs/comb_{n}.json` (`"status": "NO"`, with node counts), `runs/sat_{n}.json` | re-run Algorithm 1 or 2 ([algorithms](algorithms.md)) |
| Melchior / Csima–Sawyer / de Bruijn–Erdős | computed from the type by `scripts/pencils.py` | one line of arithmetic |
| no orientable linear space | `runs/orient_{n}.json` (engine mode 4), `runs/sat_orient_{n}.json` | re-run Algorithm 3 |
| orientable, but no realization (e.g. $\{6, 4, 3^{12}\}$) | `data/proofs/*.json`: every orientable linear space with its Gröbner certificate | recompute the Gröbner bases ([algorithms](algorithms.md), §8) |
| theorem (e.g. $\{4^9\}$, band theorem) or literature (e.g. $\{3^{20}\}$, orchard bound) | `data/exclusions.json` with statement and reference | read the proof / the paper |

`data/results/classification_n{n}.json` lists, for every admissible type, its $f_0$, whether a linear space exists,
the verdict and the reason; `data/results/sequences.json` holds the four sequences with intervals where a term is not
yet exact.

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
