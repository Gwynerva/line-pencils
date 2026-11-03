---
description: "A side direction: the same question for planes in space. A proposed definition of the type, first counts up to eight planes, the dual Fano matroid as the first impossible type, and where to dig further."
---

# Planes in space

This page leaves the plane. It asks the same question for $n$ planes in space, proposes a definition of their
type, and gives the first counts. It is an exploration, not part of the main sequences. The computations are
complete for $n \le 8$; everything beyond that is open.

<figure class="fig" markdown="1">
<div class="lp-planes wide" data-scene="skew"></div>
<figcaption>Six planes: three through one line and three through another, skew to the first. Each plane of one triple
crosses the other line, so six points lie on four planes each.</figcaption>
</figure>

## What a type has to record

Two lines in the plane meet in a point. Two planes in space meet in a line. For $n$ planes, no two parallel, there
are therefore two kinds of special places:

* a **line** may lie on $k \ge 3$ of the planes, like the spine of an open book;
* a **point** may lie on $m \ge 4$ of the planes. Three planes always meet in a point, so only four or more is special.

A point on four planes can happen in two ways. Three of the planes may share a line, which the fourth plane crosses;
this is forced, since a line always meets a plane. Or the four planes may meet with no three through a line.

<div class="figs" markdown>
<figure markdown="1">
<div class="lp-planes" data-scene="book"></div>
<figcaption>Five planes. Three share a line (thick), and the other two cross it in two points, each on four
planes.</figcaption>
</figure>
<figure markdown="1">
<div class="lp-planes" data-scene="four"></div>
<figcaption>Four planes through one point, no three of them through a line. Their six lines (thin) all pass through
the point.</figcaption>
</figure>
</div>

To tell such points apart, look at the planes through a point $P$ from close by. A small sphere around $P$ is cut by
them in great circles, that is, in an arrangement of lines of the projective plane. The pencil type of this
arrangement is the **local type** $\tau_P$ of the point. Its pencils are the lines of space through $P$. In the five
planes above both points have $\tau = \{3\}$; in the four planes, $\tau = \{\}$.

<figure class="fig" markdown="1">
<div class="lp-planes wide" data-scene="mirrors"></div>
<figcaption>Six planes through one point (the mirror planes of a regular tetrahedron) and a seventh plane. The four
thick lines lie on three planes each; the seventh plane meets them in four points 4{3}.</figcaption>
</figure>

<div class="figs" markdown>
<figure markdown="1">

--8<-- "fig/planes-sphere.svg"

<figcaption>The six planes through the point cut a small sphere around it in six great circles. The four lines on
three planes give four antipodal pairs of triple points.</figcaption>
</figure>
<figure markdown="1">
<div class="lp-draw" data-n="6" data-type="3,3,3,3"></div>
<figcaption>The six circles, seen as six lines of the projective plane: the complete quadrilateral,
type {3<sup>4</sup>}. So this point has τ = {3<sup>4</sup>}.</figcaption>
</figure>
</div>

## The proposed definition

<div class="thm" markdown>
**Definition.** Let $\mathcal A$ be a set of $n$ distinct planes in $\mathbb{RP}^3$. A *line* of $\mathcal A$ is a
line of space lying on at least two of the planes, and a *point* is a point lying on at least three of them, not all
through one line.

The **type** of $\mathcal A$ consists of:

* the multiset $\lambda$ of the numbers $k \ge 3$ of planes through its lines;
* the multiset of its points on $m \ge 4$ planes, each recorded as $m$ together with its local type $\tau_P$.

We write it as, for example, lines $\{3\}$, points $[4\{3\}, 4\{3\}]$; this is the five planes above.
</div>

Exactly as in the plane, the ordinary objects are determined by the rest. Every pair of planes lies on exactly one
line. Every triple of planes lies either on a line or on exactly one point. So, with $t_k$ the number of lines on
$k$ planes,

$$\sum_{k\ge2}\binom k2 t_k=\binom n2,\qquad
\sum_{k\ge3}\binom k3 t_k+\sum_{P}\Big[\binom{m_P}3-\sum_{p\in\tau_P}\binom p3\Big]=\binom n3,$$

where the second sum runs over all points, and a point on three planes contributes 1. Hence the type determines the
number $f_1$ of lines and the number $f_0$ of points.

**The plane sits inside, twice.**

* **Section.** Cut the arrangement with a plane $H$ through none of its points. $H$ meets the planes in $n$ lines,
  and a line of space on $k$ planes becomes a point of $H$ on $k$ lines. So $\lambda$ is the pencil type of a real
  line arrangement.
* **Cone.** Conversely, joining a line arrangement in the plane $z = 1$ to the origin gives planes all through one
  point, of type $\lambda = \tau$ with the single point $[n\tau]$.

So the line part alone gives nothing new: its possible values are the [pencil types](sequences/realizable.md) of $n$
lines, and the possible numbers of lines are the planar $d(n)$. What is new is the points, and how the lines sit in
them.

<figure class="fig" markdown="1">
<div class="lp-draw" data-n="5" data-type="3"></div>
<figcaption>A generic plane cuts the five planes of the book figure in five lines, of type {3}. The line on three
planes has become a point on three lines.</figcaption>
</figure>

**Why this definition and not another.** Three alternatives were compared:

* *Only the numbers* (lines on $k$ planes, points on $m$ planes, without $\tau_P$). This is coarser, and it does not
  determine $f_0$. For seven planes, lines $\{3\}$, points $\{5, 4^4\}$ occurs with 16 and with 17 points.
* *Also which line passes through which point.* For $n \le 7$ this gives the same classes. It first splits a type
  at $n = 8$: two lines on three planes and two points $5\{3\}$, lying on the same line or on different ones.
* *The whole intersection lattice* (the matroid). This is already finer at $n = 6$, because of the two planar
  linear spaces of type $\{3^2\}$.

## First counts

The three sieves carry over:

* *combinatorial* ($b$): the type of some simple matroid of rank $\le 4$, the analogue of a linear space;
* *realizable* ($c$): the type of real planes;
* the number $d$ of possible values of $f_0$.

There is no good analogue of the arithmetic sieve. The pairs of line sizes and points that satisfy the two
identities as inequalities, with every $\tau_P$ an arithmetically admissible planar type, number
$1, 1, 2, 11, 128, 3474, \dots$ for $n = 1, 2, 3, \dots$: far too many.

In the table, "rank 4" means that the planes do not all pass through one point.

| $n$ | $b$ | $c$ | $c$, rank 4 | $d$ |
|---|---|---|---|---|
| 1 | 1 | 1 | 0 | 1 |
| 2 | 1 | 1 | 0 | 1 |
| 3 | 2 | 2 | 0 | 2 |
| 4 | 4 | 4 | 1 | 3 |
| 5 | 8 | 8 | 3 | 5 |
| 6 | 20 | 20 | 11 | 11 |
| 7 | 57 | 55 | 39 | 22 |
| 8 | 207 | 198 | 170 | 41 |

<span class="status-computed">computer-verified</span> How the counts were obtained:

* All simple matroids of rank $\le 4$ were generated by single-element extensions. Their numbers agree with
  Mayhew and Royle[^mr] (OEIS A058733).
* Every realizable type has integer coordinates, which an independent exact verifier, `scripts/planes_verify.py`,
  recomputes.
* Every other type is excluded by a proof, below.

The arrangements through one point contribute exactly the planar $c(n)$: $198 - 170 = 28$. We found no OEIS entry
for these rows: the searches up to $n = 7$ give only unrelated prefix matches. The scripts are
`scripts/planes_*.py`, and the details are in the repository note `notes/planes.md`.

## The first impossible type: the dual Fano matroid

In the plane the first impossible type appears at $n = 7$ and is the Fano plane. In space the first gap is again
at $n = 7$, where two types are combinatorially possible but not realizable. One is the cone over the Fano plane,
seven planes through one point, which is the planar obstruction again. The other is genuinely spatial: it comes from
the matroid dual of the Fano plane.

<div class="thm" markdown>
**Proposition.** <span class="status-proved">proved</span> No seven real planes have the type lines $\{\}$, points
$[4\{\}^7]$: seven points on four planes each, no line on three planes.
</div>
<div class="proof" markdown>
*Proof.*

1. Two of the seven quadruples share at most two planes: three planes not through a line meet in only one point.
   So their complements are seven triples, each two sharing at most one plane, on seven planes. That is the Fano
   plane, and the quadruples are the complements of its lines.
2. Write the planes as vectors $v_0, \dots, v_6 \in \mathbb R^4$ with $v_0, \dots, v_3$ the unit vectors, and number
   them so that the dependent quadruples are $3456, 1256, 1234, 0246, 0235, 0145, 0136$.
3. Then $v_4 = (0,a,b,c)$, $v_5 = (d,0,e,f)$ and $v_6 = (g,h,0,k)$, with all nine letters nonzero.
4. The quadruples $1256$, $0246$ and $0145$ give $dk = fg$, $ak = ch$ and $bf = ce$.
5. The quadruple $3456$ asks for $aeg + bdh = 0$.
6. Substituting gives $aeg + bdh = 2abfg/c$, which is not zero. <span class="qed">$\square$</span>
</div>

For eight planes there are nine combinatorially possible types that cannot be realized. One is the cone over the
Möbius–Kantor configuration, excluded because $\{3^8\}$ is not a type of eight lines. For the other eight types,
every matroid of the type has to be excluded, and three arguments do this for all of them but two:

* the planes through some point form the Fano configuration;
* the other planes cut one of the planes in the Fano configuration;
* seven of the planes form the dual Fano matroid.

The two exceptions are two of the five matroids of the type with eleven points on four planes (and no line on three
planes). For them a Gröbner basis shows that they have no realization over any field of characteristic 0.

The richest of the impossible types is fourteen points on four planes, the affine space $AG(3,2)$. Thirteen such
points are impossible too. Twelve are possible: the eight face planes of the regular octahedron, viewed
projectively, have this type.

## Where to dig

<div class="thm openp" markdown>
**Open problem.** Compute $b$ and $c$ for nine planes.

There are 185 981 simple matroids of rank 4 on nine elements.[^mr] Their orientability has been tested,[^mmib]
but real realizability in rank 4 is settled only up to eight elements, even for oriented matroids.[^fmm]
</div>

* **Inequalities.** In the plane, Melchior's and Hirzebruch's inequalities do most of the excluding. For planes in
  space we found no such inequality in terms of lines on $k$ planes and points on $m$ planes. Michałek and
  Pokora[^mp] study $f_0 - f_1 + n + 2 \ge 0$ for complex plane arrangements and show that it can fail.
* **The number of points.** In the plane the possible numbers of points are known for large $n$ (Salamon–Erdős).
  The values for planes show the same kind of gaps near the top: for eight planes all values from 10 to 39 occur,
  then 41, 42, 44, 45, 47, 50, 53, 56.
* **Sylvester–Gallai in space.** An arrangement not through one point always has a point whose planes are all but one
  through a common line (Motzkin, see Lin–Swanepoel[^ls]). How many must there be? The orchard problem for
  four-point planes is solved for large $n$ by Lin and Swanepoel[^ls], and for few ordinary planes see Ball[^ball]
  and Ball–Monserrat.[^bm]
* **Hyperplanes.** In dimension $d$, the type would record flats of each dimension together with their local types.
  The section and cone constructions again embed each dimension in the next.

[^mr]: D. Mayhew, G. F. Royle, Matroids with nine elements, *Journal of Combinatorial Theory, Series B* 98 (2008),
    415–431, Table 2, [arXiv:math/0702316](https://arxiv.org/abs/math/0702316).
[^mmib]: Y. Matsumoto, S. Moriyama, H. Imai, D. Bremner, Matroid enumeration for incidence geometry, *Discrete &
    Computational Geometry* 47 (2012), 17–43,
    [doi:10.1007/s00454-011-9388-y](https://doi.org/10.1007/s00454-011-9388-y).
[^fmm]: K. Fukuda, H. Miyata, S. Moriyama, Complete enumeration of small realizable oriented matroids, *Discrete &
    Computational Geometry* 49 (2013), 359–381, Theorem 1.1, [arXiv:1204.0645](https://arxiv.org/abs/1204.0645).
[^mp]: M. Michałek, P. Pokora, A counterexample to Purdy's inequality for hyperplane arrangements in projective
    three-space, [arXiv:2607.08463](https://arxiv.org/abs/2607.08463) (2026).
[^ls]: A. Lin, K. Swanepoel, Ordinary planes, coplanar quadruples, and space quartics, *Journal of the London
    Mathematical Society* 100 (2019), 937–956, [doi:10.1112/jlms.12251](https://doi.org/10.1112/jlms.12251),
    [arXiv:1808.10847](https://arxiv.org/abs/1808.10847).
[^ball]: S. Ball, On sets defining few ordinary planes, *Discrete & Computational Geometry* (2018),
    [arXiv:1606.02138](https://arxiv.org/abs/1606.02138).
[^bm]: S. Ball, J. Monserrat, A generalisation of Sylvester's problem to higher dimensions, *Journal of Geometry*
    (2017), [arXiv:1608.03189](https://arxiv.org/abs/1608.03189).
