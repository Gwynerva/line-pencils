# Constructive searches for 12 and 13 lines (October 2026)

What was tried to settle the last types for n = 12 and to push n = 13, what worked and what did not. Only the methods
that produced certificates or proofs are kept in `scripts/`; the others are described here so that they need not be
repeated.

## Kept

| method | script | outcome |
|---|---|---|
| zone walk | `scripts/zone_walk.py` | every type with a rational realization for n ≤ 12, including {3^18}; 14 new types at n = 13; 1104 types at n = 14 |
| zone walk over Z[√5], Z[√2], started from the certificates of 12 lines | `scripts/zone_walk.py --from 12 --d 5` | 4 more new types at n = 13 (over Q(√5)) |
| targeted deformation (one or two new lines) | `scripts/targeted.py` | {3^18} over Q(√5); {5^3, 4^2, 3^7} at n = 13; rebuilds the √5 types {5, 3^10} and {3^16} from rational arrangements |
| sections of 4-dimensional mirror arrangements | `scripts/mirror_sections.py` | {4^9} at n = 13: 13 of the 31 planes perpendicular to the symmetry axes of the icosahedron (over Q(√5)) |
| symmetric drawings for the gallery | `scripts/symmetric_drawings.py` | no new types, but symmetric drawings without parallel lines for a large part of the known types |
| orientability by a case split | `scripts/orient_split.py` | {4^5, 3^9} is not orientable (8 cases, 3 SAT solvers, control type satisfiable) |

**Zone walk.** A new line is a point of the dual plane; the dual lines of the intersection points cut it into cells,
edges and vertices, and the type of the extended arrangement depends only on which points the line passes through.
The walk inserts one line per class and re-inserts every line of every kept arrangement. How many realizations are
kept per type matters little (at n = 13: 609, 612, 612, 611 types for 1, 2, 4, 8 realizations per type), but keeping
realizations of *different combinatorics* matters: that version found {3^18}. Starting from two lines, the walk
misses exactly the types for which we only have √5 realizations ({5, 3^10}, which needs √5, and {3^16}): its arithmetic
never leaves the field it starts in. Of the 140 types that had certificates over Q(√d) at n = 13 before this work, 139
also got rational realizations.

**Targeted deformation.** Keep the pencils of a smaller certified arrangement, push one or two new lines through chosen
points and solve by Gauss–Newton with the smallest change; irrational coordinates appear as roots of the equations. It
is the only method here that reaches the rigid √5 types without being given them.

**Case split.** For {4^5, 3^9} the undivided orientability search (engine mode 4) did not finish in 4 h; fixing the
configuration of the five 4-pencils first (only 8 fit into 12 lines) makes each SAT instance take seconds. Euler's
formula shows why the type is tight: an arrangement of this type would have only triangular faces except one
quadrilateral.

## Tried, not kept

* **Points on a cubic.** Three points of a cubic are collinear iff they sum to zero in the group law, so {3^t} on a
  cubic is a set of 12 group elements with t zero-sum triples. Cuspidal cubic (t, t³) with integers in [−9, 9]: at
  most 15 triples. Real elliptic curves, subgroups Z_N (N ≤ 18) and Z_N × Z_2 (N ≤ 9) exhaustively, larger N by
  local search: 17 and 19 occur, 18 never. ({3^18} was later realized off any cubic.)
* **Stepwise degeneration.** From general position, impose one new concurrency at a time with a small Gauss–Newton
  step. Extra coincidences appear by themselves (Pappus at n = 9), but at n = 12 the greedy path stalls at 16 triple
  points and never reaches the known {3^19}.
* **Rotationally symmetric arrangements** (orbits of C_k): the numerical version produced near-degenerate false
  positives and was dropped.
* **Blowing up a free pencil.** A pencil whose lines meet the other lines only in double points can be replaced by a
  small copy of any realizable arrangement of as many lines. At n = 13 this gives 335 types, all known; no contradiction
  with the classification.
* **Snapping near-coincidences** (trying the smallest zones of the dual map first in the targeted search): as fast as
  random choices on {3^18}, nothing new at n = 13.
* **Random lattice points.** Random small subsets of an integer grid, lines through at least two of them, n of those
  lines chosen with weights: 300 of the 336 types at n = 12 in five minutes and 527 of the 619 then known at n = 13 in ten, nothing
  new; a quick source of starting points, not of new types.

* **Projections of 3- and 4-dimensional figures.** Central projections of the edges, diagonals and symmetry axes of
  polyhedra; projections of the edges of the tesseract, 16-, 24- and 600-cell and of star figures (edges = vertex pairs
  at any fixed distance, which covers the Kepler–Poinsot and Schläfli–Hess polytopes); plane sections of the A4, D4,
  B4, F4, H4 mirror arrangements, random and symmetric, with all 13-subsets of the B4 and F4 sections. Together they
  reach 589 of the 620 known types at n = 13; the only new one is {4^9} (kept above). The pentagram with its axes,
  {5, 3^10}, sits inside the 15 mirror planes of the icosahedron.

For the 39 open types at n = 13, none of the constructive methods found even a numerical solution.
