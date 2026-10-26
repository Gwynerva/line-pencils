# Status journal

## Current state

### Settled

* **Verifier** (`verifier/verify.py`): exact, standard library only, tested; 1326 legacy certificates re-verified and
  converted; CI on every push. Site live at https://gwynerva.github.io/line-pencils/.
* **b(n), n ≤ 12**: 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, **384** (engine mode 0, no time-outs; SAT agrees on every
  type for n ≤ 12).
* **c(n), n ≤ 11**: 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180 — certificates + theorems + engine mode 4 (`runs/orient_11.json`).
* **c(12) = 336**. The last two types: {3^18} realized with integer coefficients in [−3, 3] (zone walk,
  `scripts/zone_walk.py`); {4^5, 3^9} not orientable (SAT over the 8 configurations of its 4-pencils, three solvers,
  `scripts/orient_split.py`, `runs/orient_split_12.json`). Also decided: {4^9} (theorem), {3^20} (no orientable linear
  space, `scripts/orchard12.py`), 15 types non-orientable (engine mode 4), {6, 4, 3^12} and {6, 3^14} orientable but not
  realizable (Gröbner certificates; hand proof for the first on the theorems page).
* **d(n), n ≤ 13**: 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56 (all exact now that the three 21-point types at n = 12 are
  excluded). **Theorem** (`notes/points.md`): for n ≥ 13 the values below 2n−1 are exactly {1, n, 2n−4, 2n−2}.
  d(14) ∈ [65, 67] (undecided: 27, 28), d(15) ∈ [73, 79], d(16) ∈ [83, 91], d(17) ∈ [92, 103] (`notes/bands.md`).
* **Band theorem** (`notes/bands.md`): the realizable types with largest pencil n−k are exactly {n−k} ∪ BAND(k) once
  n − k ≥ max(C(k,2), k+1) and n ≥ 2; BAND(k) comes from the types of k lines by "absorbing" points. N(k) = 1, 1, 2, 5, 12, 30, 74, 176, 401.
  Necessary condition valid for all n: excludes 28 types at n = 13 that pass every other test (41 before more of the
  n = 13 combinatorial searches finished).
* **n = 13**: c(13) ∈ [620, 659] (20 types realized by the zone walk, the targeted deformation and a section of the H4
  mirror arrangement, 39 open; no constructive search found even a numerical solution for any of the 39); b(13) ∈ [662, 2087] (engine mode 0 with re-runs of the
  time-outs, `runs/comb_13.json`).
* **n = 14**: c(14) ≥ 1104 (zone walk, `data/certificates/n14.json`).
* **Constructive searches**: what was tried and what worked is summarised in `notes/constructions.md`.
* **{5, 3^10} needs √5**: exact (`scripts/pentagon.py`). **{4^9}** excluded by a theorem.

### Not done

* Exclusion of the 39 open n = 13 types (case splits like the one for {4^5, 3^9} are the natural next step).
* b(13): the remaining engine time-outs.
* Figures: duality picture, search tree.
* OEIS: A399464, A399605, A400149 submitted; after review add c(12) = 336 to A399464 (`oeis/SUBMISSION_GUIDE.md`, §7).
