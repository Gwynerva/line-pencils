---
description: "Draw n lines, no two parallel: how many of them can pass through each intersection point? Pictures, counts, proofs and new integer sequences."
---

# How n Lines Can Meet

*Pencil types of line arrangements and the integer sequences they generate.*

<div class="lp-hero-wrap" markdown>
<div class="lp-hero" aria-label="Ten lines: a regular pentagram and its five axes of symmetry"></div>
<div markdown>

Draw $n$ straight lines on a sheet of paper, no two of them parallel. Every pair of lines meets somewhere, but the
meeting points need not be distinct: three, four or more lines may pass through the same point. At each
intersection point write down how many lines go through it. The resulting multiset of numbers is the **pencil type**
of the drawing. The ten lines in the picture meet in one point on five lines, ten points on three lines and five
ordinary crossings, so their type is $\{5, 3^{10}, 2^5\}$. Hover over (or tap) an intersection point to see which
lines pass through it.

The question is as simple as it sounds: **which pencil types occur, and how many are there for each $n$?**

</div>
</div>

Three tests separate the possible from the impossible. Arithmetic first: a point on $k$ lines uses up
$\binom k2$ of the $\binom n2$ pairs of lines, so the pencil sizes must fit into the available pairs. Combinatorics
second: two lines meet only once, so two pencils cannot share two lines. Geometry last: the lines have to exist in
the real plane. Counting what survives each test gives three integer sequences, and a fourth one counts how many
different *numbers of intersection points* $n$ lines can have.

| | $n = 1, 2, 3, \dots$ | OEIS |
|---|---|---|
| [$a(n)$](sequences/arithmetic.md) arithmetic | 1, 1, 2, 4, 7, 15, 32, 66, 141, 295, 619, 1286, 2654, … | [A072964](https://oeis.org/A072964), shifted |
| [$b(n)$](sequences/combinatorial.md) combinatorial | 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384, 729, 1357, 2558 | [A400149](https://oeis.org/A400149) |
| [$c(n)$](sequences/realizable.md) realizable | 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180, 336 | [A399464](https://oeis.org/A399464) |
| [$d(n)$](sequences/points.md) numbers of points | 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56 | [A399605](https://oeis.org/A399605) |

$a(n)$ counts the types allowed by arithmetic, $b(n)$ those consistent with "two lines meet only once", $c(n)$ the
types of actual lines in the plane, and $d(n)$ the different possible numbers of intersection points. $a(n)$ is
<span class="status-proved">proved</span> for every $n$; the listed terms of $b$, $c$, $d$ are
<span class="status-computed">computer-verified</span>. [Mark Kim's preprint](https://doi.org/10.5281/zenodo.24567131) establishes $b(13)$, $b(14)$ and $b(15)$.
The current bounds include $620 \le c(13) \le 659$, $1104 \le c(14) \le 1229$, $65 \le d(14) \le 66$ and $76 \le d(15) \le 77$.

Three of these four sequences, arising from a question a schoolchild can ask, were missing from the On-Line
Encyclopedia of Integer Sequences; this site was written to fill the gap, and they are now entries
[A400149](https://oeis.org/A400149), [A399464](https://oeis.org/A399464) and [A399605](https://oeis.org/A399605).
The gap is not one a formula could close: the list of realizable types answers Sylvester's *orchard problem* (how
many triple points can $n$ lines have?), which Green and Tao settled only for large $n$ in 2013.[^gt] A complete
description of that list, not just its size, would solve the orchard problem for every $n$.

[^gt]: B. Green, T. Tao, On sets defining few ordinary lines, *Discrete & Computational Geometry* 50 (2013), 409–468,
    [doi:10.1007/s00454-013-9518-9](https://doi.org/10.1007/s00454-013-9518-9).

## What is on this site

* [The question](problem.md), stated carefully, with the [notation](notation.md) of Grünbaum's *Arrangements and
  Spreads* and an explanation of the [three sieves](sieves.md).
* One page per [sequence](sequences/index.md), with the status of every term: *proved*, *computer-verified* or *bound*.
* [Theorems and proofs](theorems.md): what is known classically, what we proved, and what the computer checked.
  Among the new results: for $n \ge 13$ lines the number of intersection points is $1$, $n$, $2n-4$, $2n-2$, or at least
  $2n-1$. Together with a computation for $n = 12$: for $n \ge 6$, $2n-3$ intersection points are impossible exactly
  when $n \ge 12$.
* [Algorithms](algorithms.md) and [data](data.md): how the tests were computed, how every example is certified by
  exact arithmetic, and how to check everything independently.
* A [gallery](gallery.md) of every type known to be realizable for 1 to 14 lines (complete up to 12 lines), in symmetric drawings where we found one and from exact coordinates, and a page on
  [what cannot be drawn](impossible.md) and why.
* [Open problems](open.md), and [planes in space](planes.md): the same question one dimension up, with a proposed
  definition, first counts and the first impossible type.
* [References](references.md).

## Status of this write-up

The questions were posed by Petra Radko; the mathematics,
programs, computations and text are the work of Claude Code (see [About](about.md)). Everything stated as a theorem is either proved on the
[theorems page](theorems.md) or cited with a full reference; everything computed can be reproduced from the
[repository](https://github.com/Gwynerva/line-pencils), whose continuous integration re-verifies every certificate on
every change.

## How to cite

> Petra Radko, *How n Lines Can Meet: pencil types of line arrangements and the integer sequences they generate*,
> 2026. https://gwynerva.github.io/line-pencils/ — code and data: https://github.com/Gwynerva/line-pencils

Text, figures and data are licensed CC BY 4.0; code is MIT.
