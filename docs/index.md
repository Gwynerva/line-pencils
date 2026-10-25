# How n Lines Can Meet

*Pencil types of line arrangements and the integer sequences they generate.*

<div class="lp-hero-wrap" markdown>
<div class="lp-hero" aria-label="Ten lines: a regular pentagram and its five axes of symmetry"></div>
<div markdown>

Draw $n$ straight lines on a sheet of paper, no two of them parallel. Every pair of lines meets somewhere, but the
meeting points need not be distinct: three, four or more lines may pass through the same point. At each
intersection point write down how many lines go through it. The resulting multiset of numbers is the **pencil type**
of the drawing. The ten lines in the picture meet in one point on five lines, ten points on three lines and five
ordinary crossings, so their type is $\{5, 3^{10}, 2^5\}$. Point at an intersection to see which lines pass through it.

The question is as simple as it sounds: **which pencil types occur, and how many are there for each $n$?**

</div>
</div>

Three tests separate the possible from the impossible. Arithmetic first: a point on $k$ lines uses up
$\binom k2$ of the $\binom n2$ pairs of lines, so the pencil sizes must fit into the available pairs. Combinatorics
second: two lines meet only once, so two pencils cannot share two lines. Geometry last: the lines have to exist in
the real plane. Counting what survives each test gives three integer sequences, and a fourth one counts how many
different *numbers of intersection points* $n$ lines can have.

| sequence | $n = 1, 2, 3, \dots$ | status |
|---|---|---|
| $a(n)$, types allowed by arithmetic | 1, 1, 2, 4, 7, 15, 32, 66, 141, 295, 619, 1286, 2654, … | known: [A072964](https://oeis.org/A072964), shifted by one |
| $b(n)$, ways $n$ lines can meet, consistent with "two lines meet only once" | 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384 | <span class="status-computed">computed</span> through $n = 12$; **not in the OEIS** |
| $c(n)$, ways $n$ lines in the plane can meet | 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180 | <span class="status-computed">computed</span> through $n = 11$; $c(12)$ bounded (see the [sequence page](sequences/realizable.md)); **not in the OEIS** |
| $d(n)$, different possible numbers of intersection points | 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56 | <span class="status-computed">computed</span> through $n = 13$; **not in the OEIS** |

That three sequences arising from a question a schoolchild can ask are missing from the On-Line Encyclopedia of
Integer Sequences is the reason for this site. The missing entries are not an oversight that a formula would
fix: the sequence $c(n)$ contains the *orchard problem* of Sylvester (how many triple points can $n$ lines have?),
which was settled only for large $n$ by Green and Tao in 2013.[^gt] Any closed form for $c(n)$ would answer it for every $n$.

[^gt]: B. Green, T. Tao, On sets defining few ordinary lines, *Discrete & Computational Geometry* 50 (2013), 409–468,
    [doi:10.1007/s00454-013-9518-9](https://doi.org/10.1007/s00454-013-9518-9).

## What is on this site

* [The question](problem.md), stated carefully, with the [notation](notation.md) of Grünbaum's *Arrangements and
  Spreads* and an explanation of the [three sieves](sieves.md).
* One page per [sequence](sequences/index.md), with the status of every term: *proved*, *computer-verified*, *bounded*, or *conjectured*.
* [Theorems and proofs](theorems.md): what is known classically, what we proved, and what the computer checked.
  Among the new results: for $n \ge 13$ lines the number of intersection points is $1$, $n$, $2n-4$, $2n-2$, or at least
  $2n-1$; in particular $2n-3$ intersection points are impossible exactly when $n \ge 12$.
* [Algorithms](algorithms.md) and [data](data.md): how the tests were computed, how every example is certified by
  exact arithmetic, and how to check everything independently.
* A [gallery](gallery.md) of every realizable type up to 13 lines, drawn from exact coordinates, and a page on
  [what cannot be drawn](impossible.md) and why.
* [Open problems](open.md).

## Status of this write-up

This write-up is still being extended. The questions were posed by Petra Radko; the mathematics,
programs, computations and text are the work of Claude Code (see [About](about.md)). Everything stated as a theorem is either proved on the
[theorems page](theorems.md) or cited with a full reference; everything computed can be reproduced from the
[repository](https://github.com/Gwynerva/line-pencils), whose continuous integration re-verifies every certificate on
every change.

## How to cite

> Petra Radko, *How n Lines Can Meet: pencil types of line arrangements and the integer sequences they generate*,
> 2026, https://gwynerva.github.io/line-pencils/ (code: https://github.com/Gwynerva/line-pencils).

Text, figures and data are licensed CC BY 4.0; code is MIT.
