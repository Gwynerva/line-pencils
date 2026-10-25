# The question

This page states the problem: first in plain words, then precisely. It also explains why we may work in the
projective plane, and how the problem can be rephrased in terms of points instead of lines.

## In plain words

Take $n$ lines in the plane, no two of them parallel. Every two lines meet, so there are intersection points, but
several lines may pass through the same point. At each intersection point count the lines through it, and collect
these numbers. Their order does not matter, but repetitions do: the result is a *multiset* of numbers, each at
least 2. We call it the **pencil type** of the drawing and write it compactly, with exponents for repetitions:
$\{5, 3, 2^8\}$ means one point on five lines, one point on three lines and eight points on two lines.

The question is: **for a given $n$, which pencil types occur, and how many different ones are there?**

Why not simply count intersection points? Because the number of points hides most of the structure. Here are two
arrangements of seven lines with ten intersection points each:

<div class="figs" markdown>
<figure markdown="1">
<div class="lp-draw" data-n="7" data-type="5,3"></div>
<figcaption>One point on five lines, one on three, eight on two: type {5, 3, 2<sup>8</sup>}.</figcaption>
</figure>
<figure markdown="1">
<div class="lp-draw" data-n="7" data-type="4,3,3,3"></div>
<figcaption>One point on four lines, three on three, six on two: type {4, 3<sup>3</sup>, 2<sup>6</sup>}.</figcaption>
</figure>
</div>

The pencil type tells them apart; the number of points does not. The simpler question — how many different
*numbers* of intersection points $n$ lines can have — is studied too, as the fourth sequence below.

## Definitions

<div class="thm" markdown>
**Definition 1 (arrangement, pencil, type).** An *arrangement* $\mathcal A$ is a set of $n \ge 1$ distinct lines in
the real projective plane $\mathbb{RP}^2$. For a point $P$ let $\mu(P)$ be the number of lines of $\mathcal A$
through $P$. A point with $\mu(P) \ge 2$ is an *intersection point*; the set of lines through it is a *pencil* of size
$\mu(P)$. For $k \ge 2$, $t_k(\mathcal A)$ is the number of intersection points with $\mu(P) = k$, and
$f_0(\mathcal A) = \sum_k t_k$ is the number of intersection points. The *pencil type* of $\mathcal A$ is the multiset
$\{k^{t_k} : k \ge 2\}$.
</div>

Every two lines meet in exactly one point, and a point on $k$ lines accounts for $\binom k2$ of the pairs, so

$$\sum_{k \ge 2} \binom k2\, t_k \;=\; \binom n2 .  \tag{1}$$

Hence $t_2$ is determined by the other $t_k$, and we usually write a type by its pencils of size at least three, as a
non-increasing list: for twelve lines, $\{6, 4, 3^{12}\}$ means $t_6 = 1$, $t_4 = 1$, $t_3 = 12$ and, by (1),
$t_2 = 66 - 15 - 6 - 36 = 9$. The empty list $\{\}$ is *general position*: all $\binom n2$ intersection points are
ordinary, that is, on exactly two lines.

Equation (1) can also be read as a count of lost points: a pencil of $k$ lines merges $\binom k2$ would-be ordinary
points into one, so it loses $\binom k2 - 1$ of them. The *loss* of a type is
$\ell = \binom n2 - f_0 = \sum_{k\ge3} \big(\binom k2 - 1\big) t_k$, a sum of numbers from $2, 5, 9, 14, 20, \dots$

## Why the projective plane

The question was asked in the Euclidean plane, with no two lines parallel. Working in $\mathbb{RP}^2$ changes nothing:

<div class="thm" markdown>
**Lemma 2.** The pencil types of arrangements of $n$ lines in the Euclidean plane with no two lines parallel are
exactly the pencil types of arrangements of $n$ lines in $\mathbb{RP}^2$.
</div>
<div class="proof" markdown>
*Proof.* A Euclidean arrangement without parallels sits in $\mathbb{RP}^2$ with the same intersection points: no two
of its lines meet on the line at infinity. Conversely, a projective arrangement has finitely many intersection points;
choose a line $\ell_\infty$ not in $\mathcal A$ through none of them and remove it. In the affine plane that remains,
two lines of $\mathcal A$ are parallel only if they meet on $\ell_\infty$, which they do not, and the intersection
points are unchanged. <span class="qed">$\square$</span>
</div>

The projective plane is more convenient because every two lines meet without exception, and a projective
transformation may be applied freely. All drawings on this site are produced this way: a transformation is chosen
under which every intersection point is finite and the points are well spread out.

## Duality: lines become points

The map $(a : b : c) \mapsto \{ax + by + cz = 0\}$ identifies points of $\mathbb{RP}^2$ with lines of $\mathbb{RP}^2$
and preserves incidence. Under it, an arrangement of $n$ lines becomes a set of $n$ points, and a pencil of $k$ lines
through a point becomes a line through $k$ of the points. So:

> Pencil types of $n$ lines $=$ multisets of sizes of the lines through at least three of $n$ given points in the plane.

Much of the classical literature speaks the point language. The Sylvester–Gallai theorem ("$n$ points not all on a
line determine a line through exactly two of them") becomes "$n$ lines not all through one point have an ordinary
intersection point"; the orchard problem ("plant $n$ trees in as many rows of three as possible") asks for the largest
$t_3$. We switch between the two pictures freely. The certificates on this site store the $n$ lines by their
coefficient vectors $(a, b, c)$, which are the same numbers as the dual points.

## The four counting questions

Pencil types are filtered by three tests of increasing strength, and each surviving family is counted; a fourth
sequence counts numbers of points. For $n \ge 1$:

1. $a(n)$ — the number of multisets $\{k_1, \dots, k_r\}$ with $3 \le k_i \le n$ allowed by arithmetic alone,
   $\sum_i \binom{k_i}2 \le \binom n2$ (there must be enough pairs of lines).
2. $b(n)$ — the number of those for which the pencils can be assigned to lines consistently with the rule that two
   lines meet only once: no two pencils may share two lines (*combinatorially possible* types).
3. $c(n)$ — the number of pencil types of actual arrangements of $n$ lines (*realizable* types).
4. $d(n)$ — the number of different values of $f_0$, the number of intersection points.

For $n = 1$ there is one line and no intersection point; the empty type and the value $f_0 = 0$ are counted once,
so all four sequences begin with 1. The [three sieves](sieves.md) page explains the tests behind
$c(n) \le b(n) \le a(n)$ and where each inequality first becomes strict.
