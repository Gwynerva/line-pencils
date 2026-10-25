# Status journal

## Current state

### Settled

* **Verifier** (`verifier/verify.py`): exact, standard library only, tested; 1326 legacy certificates re-verified and
  converted; CI on every push. Site live at https://gwynerva.github.io/line-pencils/.
* **b(n), n ≤ 12**: 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, **384** (engine mode 0, no time-outs; SAT agrees on every
  type for n ≤ 12).
* **c(n), n ≤ 11**: 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180 — certificates + theorems + engine mode 4 (`runs/orient_11.json`).
* **c(12)**: 335 ≤ c(12) ≤ 337 (2 open types: {4^5,3^9}, {3^18}). Decided: {4^9} (theorem), {3^20} (orchard), 9 types
  non-orientable (engine mode 4), **{6, 4, 3^12} not realizable** (unique orientable linear space + Gröbner certificate;
  also a five-line hand proof in the chat log / to be added to the notes), {6, 3^14}: 4 invariant classes, class 1 proved,
  the rest in progress.
* **d(n), n ≤ 13**: 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56 (all exact now that the three 21-point types at n = 12 are
  excluded). **Theorem** (`notes/points.md`): for n ≥ 13 the values below 2n−1 are exactly {1, n, 2n−4, 2n−2}.
  d(14) ∈ [65, 67] (undecided: 27, 28), d(15) ∈ [73, 79], d(16) ∈ [83, 91], d(17) ∈ [92, 103] (`notes/bands.md`).
* **Band theorem** (`notes/bands.md`): the realizable types with largest pencil n−k are exactly {n−k} ∪ BAND(k) once
  n ≥ k + C(k,2); BAND(k) comes from the types of k lines by "absorbing" points. N(k) = 1, 1, 2, 5, 12, 30, 74, 176, 401.
  Necessary condition valid for all n: excludes 41 types at n = 13 that pass every other test.
* **n = 13**: c(13) ∈ [600, 661]; b(13) ∈ [657, 2102] (71 engine time-outs; 17 of them matter and are with the SAT solver).
* **{5, 3^10} needs √5**: exact (`scripts/pentagon.py`). **{4^9}** excluded by a theorem.

### Running

* `runs/orient_12.json`: engine mode 4 on the remaining n = 12 types (4 h each).
* mode-5 enumerations for {5^2,3^12}, {4^5,3^9}, {5,4^2,3^12}, {5^2,3^13}, {4^3,3^14} (90 min each) — feed the prover.
* `runs/dedupe_12_6_3x14.log` (exact isomorphism classes) and the proofs of the four invariant classes of {6,3^14}.
* SAT: the 17 open n = 13 time-outs (`runs/sat_13.json`). The b(12) cross-check is finished: all 1286 verdicts agree.

### Not done

* Human-readable write-up of the {6,4,3^12} proof in `notes/` (the affine computation with A = 0, B = bu, D = du, C = v).
* Exclusion / construction of the remaining n = 12 and n = 13 open types.
* Figures: duality picture, search tree.
* OEIS submission (drafts ready in `oeis/`, decisions for the author listed there).
