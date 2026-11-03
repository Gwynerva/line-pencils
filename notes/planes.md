# Planes in space: a 3D analogue

Technical note behind the site page `docs/planes.md` (November 2026). Code: `scripts/planes_*.py`; data:
`runs/planes_*.json`.

## 1. Setting

An *arrangement* is a set of $n \ge 1$ distinct planes in $\mathbb{RP}^3$. Its intersection lattice is a simple
matroid $M$ of rank $\le 4$ on the $n$ planes: the rank of a set is the dimension of the span of its normal vectors.
In this lattice:

* a **line** is a flat of rank 2, i.e. a line of space together with all planes through it. Its *size* $|L|$ is the
  number of planes through it, and is $\ge 2$;
* a **point** is a flat of rank 3, of size $|P| \ge 3$.

The whole set counts as a line when all planes pass through one line (rank 2), and as a point when they all pass
through one point (rank 3).

**Duality.** Planes in $\mathbb{RP}^3$ correspond to points of $\mathbb{RP}^3$. Under it, a line on $k$ planes is a
line through $k$ of the points, and a point on $m$ planes is a plane through $m$ of the points. So the whole question
can be restated for $n$ points in space, with their collinear triples and coplanar quadruples.

**Local arrangement at a point.** The planes through a point $P$ meet a small sphere around $P$ (equivalently, a
plane not through $P$) in an arrangement of $|P|$ lines. Its pencils are the lines of the arrangement through $P$.
The pencil type of this line arrangement is
$\tau_P = \{\,|L| : L \ni P,\ |L| \ge 3\,\}$, a realizable planar pencil type of $|P|$ lines.

## 2. Candidate definitions of the type

Four candidates, from coarse to fine:

| | records | determines $f_0, f_1$? |
|---|---|---|
| **S** (size type) | multiset of line sizes $\ge 3$, multiset of point sizes $\ge 4$ | $f_1$ yes, $f_0$ **no** |
| **L** (local type) | line sizes $\ge 3$, and for each point on $\ge 4$ planes its size together with $\tau_P$ | yes, by (1) and (2) |
| **I** (incidence type) | L together with which special line passes through which special point (an isomorphism class of a labelled bipartite graph) | yes |
| **M** (matroid) | the whole intersection lattice up to isomorphism | yes |

**Definition used: L.** The *type* of an arrangement is the pair $(\lambda; \pi)$, where

* $\lambda$ is the multiset of sizes $k \ge 3$ of its lines, and
* $\pi$ is the multiset of the points on $m \ge 4$ planes, each recorded as $m\tau_P$.

Notation: lines $\{3^2\}$, points $[5\{3^2\}, 4\{3\}^2]$.

Two counting identities hold, with $t_k$ the number of lines of size $k$ ($k \ge 2$) and the sums over points running
over all points:

$$\sum_{k\ge2}\binom k2 t_k=\binom n2, \tag{1}$$
$$\sum_{k\ge3}\binom k3 t_k+\sum_P\Big[\binom{|P|}3-\sum_{p\in\tau_P}\binom p3\Big]=\binom n3. \tag{2}$$

(1) says that every pair of planes lies on exactly one line. (2) says that every triple of planes lies either on a
line or on exactly one point, not both. Points on 3 planes contribute 1 each.

The number $t_2$ of ordinary lines is determined by (1). The number of points on 3 planes is determined by (2). Hence
$f_1$ (the number of lines) and $f_0$ (the number of points) are functions of the type, exactly as $t_2$ and $f_0$
are functions of the pencil type in the plane. This is the main reason to prefer L to S:

* the size type does not determine $f_0$. For $n = 7$ the size type lines $\{3\}$, points $\{5, 4^4\}$ has two
  realizations, with local types $[5\{3\}, 4\{3\}^2, 4\{\}^2]$ ($f_0 = 16$) and $[5\{\}, 4\{3\}^4]$ ($f_0 = 17$);
* I and M are finer than needed. I coincides with L for $n \le 7$ and first splits a type at $n = 8$: with two triple
  lines and two points $5\{3\}$, the two 5-points can lie on the same triple line or on different ones. M is the
  "combinatorial type" (intersection lattice) and is already finer than L at $n = 6$, because of the planar
  ambiguity: there are two linear spaces of type $\{3^2\}$.

**The planar problem sits inside in two ways**, so L is a genuine extension of the project:

* **Section.** A generic plane $H$ (one through no point of the arrangement and containing no line of it) meets the
  planes in $n$ distinct lines. A point of $H$ on $k$ of these lines is $H \cap L$ for a line $L$ of size $k$, and
  distinct lines $L$ meet $H$ in distinct points: two distinct lines that meet do so in a point of the arrangement,
  which $H$ avoids. So $\lambda$ is the pencil type of a real line arrangement.
* **Cone.** Conversely, the cone over a line arrangement (the planes joining its lines to a point outside the plane)
  is an arrangement of rank $\le 3$ whose type is $(\tau; [n\tau])$, or $(\{n\};[\,])$ for a pencil.

Consequences:

* the arrangements of rank $\le 3$ contribute exactly $c(n)$ types (the planar sequence);
* the values of $\lambda$ are exactly the planar pencil types of $n$ lines;
* the possible values of $f_1$ are exactly the planar values of $f_0$, i.e. the planar sequence $d(n)$. This was
  checked for $n \le 7$: $1, 1, 2, 3, 5, 9, 13$.

So nothing new comes from the lines alone. What is new is the points and how the lines sit in them.

**Ordinary points.** The "unavoidable" points are the near-pencils: $m$ planes through a point, $m-1$ of them through
one line, local type $\{m-1\}$, with $3\{\}$ for $m = 3$. The 3D Sylvester–Gallai theorem attributed to Motzkin
(Lin–Swanepoel, see §6) says, dually, that an arrangement of rank 4 always has such a point. The definition above records the
near-pencil points with $m \ge 4$ ($4\{3\}$, $5\{4\}$, …) explicitly. They cannot be dropped as $t_2$ is dropped in
the plane, because their number is not determined by the remaining data, and with them (1) and (2) make the type
self-contained. The price is longer notation.

## 3. The sieves

* **a (arithmetic).** Count pairs $(\lambda,\pi)$ allowed by (1) and (2) as inequalities, with each $\tau_P$ an
  arithmetically admissible planar type of $|P|$ lines, $\tau_P \ne \{|P|\}$ (`planes_arith.py`). The counts are
  $1, 1, 2, 11, 128, 3474, 187107, 17900247$ for $n = 1, \dots, 8$. Each point consumes only 3 or 4 triples, so the
  count explodes. **There is no natural analogue of $a$**, and it is not used further.
* **b (combinatorial).** Types of simple matroids of rank $\le 4$ on $n$ elements, i.e. of geometric lattices of
  rank $\le 4$. This is the analogue of "linear space".
* **c (realizable).** Types of real arrangements of $n$ planes.
* **d (points).** The number of possible values of $f_0$ (points of the arrangement, all multiplicities). The analogue
  using $f_1$ is the planar $d(n)$, as shown above.

## 4. Terms

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $b(n)$, type L | 1 | 1 | 2 | 4 | 8 | 20 | 57 | 207 |
| $c(n)$, type L | 1 | 1 | 2 | 4 | 8 | 20 | 55 | 198 |
| $c(n)$, type L, rank 4 only | 0 | 0 | 0 | 1 | 3 | 11 | 39 | 170 |
| $b(n)$, rank 4 only | 0 | 0 | 0 | 1 | 3 | 11 | 40 | 178 |
| $d(n)$: values of $f_0$ | 1 | 1 | 2 | 3 | 5 | 11 | 22 | 41 |
| for comparison: $c(n)$, type S | 1 | 1 | 2 | 4 | 8 | 20 | 53 | 173 |
| $b(n)$, type S | 1 | 1 | 2 | 4 | 8 | 20 | 55 | 181 |
| $b(n)$, type I | 1 | 1 | 2 | 4 | 8 | 20 | 57 | 209 |
| simple matroids, rank $\le 4$ | 1 | 1 | 2 | 4 | 8 | 21 | 73 | |
| real-realizable among them | 1 | 1 | 2 | 4 | 8 | 21 | 71 | |

Checks against the plane:

* the rank-$\le 3$ part of $c$ is the planar $c(n)$: $1, 1, 2, 3, 5, 9, 16, 28$, and indeed
  $198 - 170 = 28$ and $55 - 39 = 16$;
* the rank-$\le 3$ part of $b$ is the planar $b(n)$: $207 - 178 = 29$.

Values of $f_0$:

* $n=6$: $0,1,6,7,9,10,11,13,14,17,20$
* $n=7$: $0,1,7,\dots,20,22,23,26,29,32,35$
* $n=8$: $0,1,8,10,\dots,39,41,42,44,45,47,50,53,56$

The value 0 is the pencil of planes through one line and 1 is the planes through one point. As in the plane, the
values below $\binom n3$ show gaps near the top.

## 5. Evidence

**Enumeration** (`planes_matroids.py`).

* All simple matroids of rank $\le 4$ on $n \le 7$ elements are generated by single-element extensions:
  coloop extensions, and modular cuts given by linear subclasses of hyperplanes (Crapo's theory; standard, e.g.
  Oxley, *Matroid Theory*, §7.2).
* They are reduced up to isomorphism, and every stored matroid is checked against the flat axioms.
* The counts by rank agree with Mayhew–Royle, Table 2: rank 3 gives $1, 2, 4, 9, 23$ for $n = 3..7$; rank 4 gives
  $1, 3, 11, 49$ for $n = 4..7$.
* For $n = 8$, `planes_types_next.py` takes all 31 545 labelled extensions of the 73 matroids on 7 elements,
  without isomorphism reduction, and groups them by type. This is complete because every simple matroid on 8
  elements is an extension of one on 7.
* The isomorphism catalogue for $n = 8$ (`planes_matroids.py 8`, about 50 minutes) gives 617 matroids of rank 4 and
  68 of rank 3, again in agreement with Mayhew–Royle. It is not needed for the type counts.

**Realizable types.**

* For every realizable type, `runs/planes_certificates.json` holds integer plane coordinates, found by a randomized
  constructive search (`planes_realize.py`).
* `planes_verify.py` shares no code with the search. It recomputes each type from the integer vectors alone (exact
  ranks; lines and points as maximal sets spanning a 2- or 3-space), checks that the planes are distinct, and
  confirms 1, 1, 2, 4, 8, 20, 55, 198 distinct certified types.
* Example: the type with no special lines and points $4\{\}^{12}$ ($n = 8$) has the certificate
  $(23,-6,-3,6),(4,24,-15,15),(1,-2,-1,-2),(20,8,-29,29),(2,1,-2,2),(19,-10,-8,11),(0,1,-1,1),(-1,-2,-2,1)$.

**Non-realizable types.** For each of them, every matroid of that type (from the enumeration, reduced up to
isomorphism by `planes_unresolved.py`) is shown not to be real. Three obstructions are used. They are inherited by
realizations, because a realization of the arrangement restricts to them:

* (R) the planes through a point form a real line arrangement (the local arrangement);
* (C) the other planes cut a plane $e$ of the arrangement in a real line arrangement (the simplification of the
  contraction $M/e$);
* (D) a subset of the planes is a real arrangement.

The Fano configuration violates Sylvester–Gallai and cannot occur in (R) or (C). The dual Fano matroid $F_7^*$
cannot occur in (D), by Proposition P below.

*n = 7* (two types):

* lines $\{3^7\}$, points $[7\{3^7\}]$: the cone over the Fano plane (planar);
* lines $\{\}$, points $[4\{\}^7]$: **the unique matroid of this type is $F_7^*$**, the 3D Fano. Seven 4-sets of a
  7-set pairwise meeting in $\le 2$ elements have complements forming a Steiner triple system, hence the Fano plane.

*n = 8* (nine types):

* $[8\{3^8\}]$: the cone over Möbius–Kantor, planar and known to be non-orientable;
* $\{3^7\}, [7\{3^7\}, 4\{3\}^7]$: obstruction (R);
* $[4\{\}^{14}]$: 14 coplanar quadruples covering every triple once, a Steiner quadruple system of order 8, i.e.
  $AG(3,2)$; the section at any plane is Fano: obstruction (C);
* $[4\{\}^{13}]$, $\{3\},[4\{3\}^5,4\{\}^7]$, $\{3^3\},[5\{3^2\}^3,4\{3\}^3,4\{\}^4]$,
  $\{3^4\},[6\{3^4\},4\{3\}^8,4\{\}^3]$: obstruction (C);
* $[5\{\},4\{\}^7]$: obstruction (D) with $F_7^*$;
* $[4\{\}^{11}]$, which has five matroids:
  * two have obstruction (C);
  * one has obstruction (D);
  * two (called A8 and B8 in `planes_grobner.py`) have none of these. For them a Gröbner basis shows they are not
    realizable over any field of characteristic 0:
    * fix $\{0,1,2,3\}$ to the unit vectors;
    * normalize a spanning tree of the nonzero pattern to 1;
    * then the ideal of the 11 coplanarity determinants, saturated by the variables and by one determinant that
      must be nonzero, contains 1.

**Proposition P.** $F_7^*$ is not realizable over any field of characteristic $\ne 2$.

*Proof.* Its 4-circuits are $3456, 1256, 1234, 0246, 0235, 0145, 0136$.

1. Take $v_0, \dots, v_3$ to be the unit vectors.
2. The circuits $1234$, $0235$ and $0136$ give $v_4 = (0,a,b,c)$, $v_5 = (d,0,e,f)$ and $v_6 = (g,h,0,k)$.
3. All nine letters are nonzero, because the corresponding 4-sets are bases.
4. The circuits $1256$, $0246$ and $0145$ give $dk = fg$, $ak = ch$ and $bf = ce$. Hence $k = fg/d$,
   $h = afg/(cd)$ and $e = bf/c$.
5. The circuit $3456$ requires $\det\begin{pmatrix}0&a&b\\d&0&e\\g&h&0\end{pmatrix} = aeg + bdh = 0$.
6. Substituting gives $aeg + bdh = 2abfg/c \ne 0$, a contradiction. $\square$

`planes_grobner.py` rechecks this mechanically, along with A8 and B8, in about 3 seconds.

So $n = 7$ is the first $n$ where $c < b$, in the plane and in space alike. The witnesses are the Fano plane and its
matroid dual.

## 6. Literature

Sources consulted (abstracts, introductions, tables), with page or table references.

* **D. Mayhew, G. F. Royle**, Matroids with nine elements, *JCTB* 98 (2008) 415–431, arXiv:math/0702316.
  * Table 2 gives the simple matroids of rank 4 on $n = 4..9$: $1, 3, 11, 49, 617, 185981$ (OEIS A058733); rank 3 is
    A058731.
  * §7 lists the non-representable matroids on 8 elements: 39 that are Ingleton non-representable, plus 5 more of
    rank 4.
  * There are no counts of real-representable matroids.
* **K. Fukuda, H. Miyata, S. Moriyama**, Complete enumeration of small realizable oriented matroids, *DCG* 49 (2013)
  359–381, arXiv:1204.0645.
  * Table 1 counts the simple oriented matroids of rank 4: $1, 3, 12, 206, 181472$ for $n \le 8$.
  * Theorem 1.1: 177 504 of the 181 472 in rank 4 with $n = 8$ are realizable.
  * They count oriented matroids (the full face structure), which is much finer than our types.
* **L. Finschi**, catalogue of oriented matroids (finschi.com/math/om): the same rank-4 counts (OEIS A063801).
* **Matsumoto, Moriyama, Imai, Bremner**, Matroid enumeration for incidence geometry, *DCG* 47 (2012) 17–43, and
  its RIMS Kôkyûroku 1641 companion: orientability of simple matroids of rank 4 is tested up to $n = 9$. Their
  tables were not compared with the counts here.
* **S. Ball, J. Monserrat**, A generalisation of Sylvester's problem to higher dimensions, *J. Geom.* (2017),
  arXiv:1608.03189. It bounds the number of planes through exactly 3 points (no three collinear); Motzkin's examples
  without such planes are points on two skew lines and the 10 triple points of 5 general planes.
* **S. Ball**, On sets defining few ordinary planes, *DCG* (2018), arXiv:1606.02138.
* **A. Lin, K. Swanepoel**:
  * Ordinary planes, coplanar quadruples, and space quartics, *J. LMS* 100 (2019) 937–956, arXiv:1808.10847.
    The introduction states Motzkin's theorem: a non-coplanar finite point set spans a plane in which all but one of
    its points lie on a line. Dually, this is the near-pencil point of §2.
    Corollary 1.3 is the 3D orchard problem: the maximum number of 4-point planes for large $n$ with no three points
    collinear. It is $n^3/24 - n^2/4 + 5n/6$ for $8 \mid n$, which gives 12 at $n=8$, matching the cube
    $[4\{\}^{12}]$; but the formula is only proved for large $n$.
  * On sets defining few ordinary hyperplanes, *Discrete Analysis* 2020:4.
* **M. Michałek, P. Pokora**, A counterexample to Purdy's inequality for hyperplane arrangements in projective
  three-space, arXiv:2607.08463 (2026).
  * Notation: $\lambda$ = number of lines, $p$ = points on $\ge 3$ planes, i.e. our $f_1, f_0$.
  * They study $p - \lambda + n + 2 \ge 0$: two skew pencils violate it, and they give a complex counterexample.
    This is relevant to $d(n)$.
* **M. de Borbon, D. Panov**, A Miyaoka–Yau inequality for hyperplane arrangements in $\mathbb{CP}^n$,
  arXiv:2411.09573 (abstract only). It is a candidate source of Hirzebruch-type obstructions.

Not found: any enumeration of flat-size distributions or "weak combinatorics" of plane arrangements, and any
Melchior- or Hirzebruch-type inequality for real plane arrangements stated with $t_k$ and point counts.

## 7. OEIS

Searched on 3 Nov 2026 (oeis.org, `fmt=short`); no match for:

* $1,1,2,4,8,20,55$ ($c$, type L)
* $1,1,2,4,8,20,53$ (type S)
* $1,1,2,4,8,21,71$ (realizable matroids)
* $1,1,2,3,5,11,22$ ($d$)
* $1,2,11,128,3474$ ($a$)

$1,1,2,4,8,20,57$ ($b$) matches only A344490, $1,1,1,2,4,8,20,57,171,\dots$, an unrelated recurrence; the next term
there is 171, not 207. $1,3,11,39$ (rank 4) has 16 unrelated hits. The searches were made with the terms up to
$n = 7$; searches including the $n = 8$ terms are still to be made.

Related existing entries are the matroid counts A058733 and A058731, the oriented matroids A063801, and the
realizable uniform oriented matroids A222317.

## 8. Summary and open questions

* Definition L asks how many planes pass through each line and how the planes meet at each point. It keeps the two
  exact counting identities and contains the planar problem twice.
* $b$, $c$ and $d$ are determined for $n \le 8$, with certificates and proofs as above.
* The first gap, at $n = 7$, consists of the cone over the Fano plane and the dual Fano matroid.

Open questions and known limits:

* **Nine planes.** $n = 9$ means 185 981 matroids of rank 4. The extension step is feasible, but the isomorphism
  reduction needs a canonical form (for example via nauty or a C routine); networkx is too slow.
* **Realizability in rank 4.** It is unknown beyond $n = 8$ even for oriented matroids (Fukuda–Miyata–Moriyama).
  Deciding $c(9)$ would need orientability tests and Gröbner computations as in the planar $n = 12$ case, now in
  rank 4. The growth ($\approx n^{3}$ triples instead of $n^2$ pairs) puts $n \ge 10$ out of reach of this method.
* **The number of points.** The section and cone arguments of §2 hold for every $n$; the complete list of $f_0$
  values for large $n$ (an analogue of Salamon–Erdős) is open.
* **Coarser types.** The size type S gives a different sequence ($1, 1, 2, 4, 8, 20, 53, 173$ for $c$).
