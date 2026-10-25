# How n Lines Can Meet

*Pencil types of line arrangements and the integer sequences they generate.*

[![verify certificates](https://github.com/Gwynerva/line-pencils/actions/workflows/verify.yml/badge.svg)](https://github.com/Gwynerva/line-pencils/actions/workflows/verify.yml)

<img src="docs/assets/star.svg" width="220" align="right" alt="Ten lines: a regular pentagram and its five axes">

Draw *n* straight lines, no two parallel. At every intersection point write down how many lines pass through it.
The multiset of these numbers is the **pencil type** of the arrangement. Which types occur, and how many for each *n*?

Three sieves — arithmetic, combinatorics (linear spaces), real geometry — give three integer sequences; a fourth
counts how many different numbers of intersection points *n* lines can have. Only the first is in the OEIS.

| sequence | n = 1, 2, 3, … | status |
|---|---|---|
| a(n) arithmetically admissible types | 1, 1, 2, 4, 7, 15, 32, 66, 141, 295, 619, 1286, 2654, … | = A072964(n−1) |
| b(n) ways n lines can meet, consistent with "two lines meet only once" | 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384 | computed through n = 12 |
| c(n) ways n lines in the plane can meet | 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180 | computed through n = 11; 335 ≤ c(12) ≤ 337, 600 ≤ c(13) ≤ 659 |
| d(n) different possible numbers of intersection points | 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56 | computed through n = 13 |

The write-up — definitions, theorems with proofs, algorithms, a gallery of every realizable type up to 13 lines,
and the prepared OEIS submissions — is the site built from `docs/`: **https://gwynerva.github.io/line-pencils/**
(built with [Zensical](https://zensical.org) by `.github/workflows/pages.yml`; `python -m zensical serve` shows it locally).

**Verification:** [VERIFY.md](VERIFY.md) — definitions, how each term is established, and how to check it.

## Checking the terms

```bash
python verifier/verify.py --self-test
python verifier/verify.py data/certificates/n*.json
python scripts/classify.py 12
```

Python 3.10+ only. The searches themselves need `gcc` (for `engine/ls.c`) and `pip install python-sat numpy scipy`.

## Layout

| path | content |
|---|---|
| `verifier/` | the single exact certificate verifier (standard library only) and its tests |
| `engine/ls.c` | exhaustive search for linear spaces (mode 0), orientability (modes 1, 4), enumeration (mode 5) |
| `scripts/` | drivers (`engine_run.py`), SAT encodings (`sat_linear_space.py`, `sat_orient.py`), realizer (`realize.py`, `find_examples.py`), classification (`classify.py`), bounds for the number of points (`f0_bounds.py`), drawings (`draw_svg.py`, `build_gallery_data.py`, `logo_svg.py`) |
| `data/certificates/n{n}.json` | exact certificates (lines over ℚ or ℚ(√d)), one per realizable type |
| `data/results/` | classification of every admissible type with the reason for its verdict; the four sequences |
| `data/exclusions.json` | types excluded by a theorem or by a published result |
| `runs/` | logs and checkpoints of all exhaustive runs |
| `notes/` | mathematical notes: setting, the theorem on intersection points, references, literature verification |
| `oeis/` | the three draft submissions and a submission guide |
| `docs/`, `zensical.toml` | the site (`scripts/build_gallery_data.py` writes the drawing data, `scripts/build_impossible.py` and `scripts/build_tables.py` the generated pages) |
| `legacy/program/` | the author's original exploratory scripts (reference only; superseded) |

## Authorship

The research questions and the standards of rigour were set by Petra Radko (GitHub: Gwynerva). All of the work — the
theorems and proofs, the programs, the computations, the figures and the site text — was carried out by Claude Code
(Anthropic, Fable 5.1), starting from the author's exploratory scripts and
data (`legacy/`).

## Main results

* b(12) = 384 (exhaustive search, no time-outs; SAT cross-check for n ≤ 12).
* c(n) for n ≤ 11 with a verified certificate for every realizable type and a proof for every other type.
* d(13) = 56, and a theorem: for n ≥ 13 the number of intersection points of n lines is 1, n, 2n−4, 2n−2 or at least 2n−1;
  in particular 2n−3 points are impossible exactly for n ≥ 12 (`notes/points.md`).
* {4^9} for 12 lines is not realizable (unique linear space = dual Hesse configuration, Sylvester–Gallai).
* **{6, 4, 3^12} and {6, 3^14} are realizable by pseudolines but not by lines** (exhaustive enumeration of their orientable
  linear spaces, exact isomorphism classes, Gröbner certificates; a five-line hand proof for the first).
* Band theorem: the realizable types with largest pencil n−k are {n−k} ∪ BAND(k) for n ≥ k + C(k,2); as a necessary
  condition it excludes 41 types at n = 13 that pass every other test (`notes/bands.md`).
* Open: 2 types at n = 12 ({4^5, 3^9} and {3^18}), 59 at n = 13; d(14) ∈ [65, 67].

## Licenses

Code: MIT (`LICENSE`). Text, figures and data: CC BY 4.0 (`LICENSE-CC-BY-4.0.md`).
