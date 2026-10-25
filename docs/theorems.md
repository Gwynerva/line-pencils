---
description: "Complete proofs behind every number on the site: classical inequalities, impossible configurations, lines versus pseudolines, and bounds on intersection points."
---

# Theorems and proofs

Every statement on this site is justified here: by a complete proof, by a precise reference, or by a description
of what a computer checked and how. Labels: <span class="status-proved">proved</span>, <span class="status-computed">computer-verified</span>.

## A. Classical results we rely on

These are quoted, not re-proved. Each is a statement about arrangements of real lines (or, dually, finite point sets)
that are not a single pencil.

<div class="thm" markdown>
**Theorem A1 (de Bruijn–Erdős, 1948; dual form).**[^dbe] An arrangement of $n$ lines that is not a pencil has at least $n$
intersection points, with equality only for the near-pencil ($n-1$ concurrent lines and one more).
</div>

<div class="thm" markdown>
**Theorem A2 (Melchior, 1940/41).**[^mel] For an arrangement of $n \ge 3$ lines that is not a pencil,
$t_2 \;\ge\; 3 + \sum_{k \ge 4} (k - 3)\, t_k .$ In particular $t_2 \ge 3$ (the Sylvester–Gallai theorem).
</div>

<div class="thm" markdown>
**Theorem A3 (Csima–Sawyer, 1993).**[^cs] For an arrangement of $n \ge 8$ lines that is not a pencil, $t_2 \ge 6n/13$.
(The bound holds for all $n \ne 7$; the Kelly–Moser arrangement of 7 lines has $t_2 = 3$.)
</div>

<div class="thm" markdown>
**Theorem A4 (Hirzebruch, 1983).**[^hir] For an arrangement of $n$ lines in the complex projective plane with
$t_n = t_{n-1} = 0$, $t_2 + \tfrac34 t_3 \;\ge\; n + \sum_{k\ge5} (k - 4)\, t_k .$ This is the form stated by Hirzebruch
in the remarks added in proof (p. 140), and the only one used here. The literature usually quotes a stronger
right-hand side, with coefficients $2k - 9$, under the hypothesis $n \ge 6$ and $t_n = t_{n-1} = t_{n-2} = 0$.
</div>

<div class="thm" markdown>
**Theorem A5 (Kelly–Moser, 1958).**[^km] If at most $n - k$ of $n$ points are collinear and $n \ge \tfrac12(27k^2 - 33k + 11)$,
the points determine at least $kn - \tfrac12(3k+2)(k-1)$ lines. **Theorem A6 (Elliott, 1967).**[^ell] If $n \ge 10$ points are
not all collinear and no $n - 1$ of them are collinear, they determine at least $2n - 4$ lines.
</div>

<div class="thm" markdown>
**Theorem A7 (orientability; Folkman–Lawrence, 1978).**[^fl] A real arrangement gives a chirotope (the signs of the
$3\times3$ determinants of the dual points) whose zero set is exactly the set of concurrent triples; conversely a
linear space admitting such a chirotope is realizable by an arrangement of pseudolines. Hence non-orientable
linear spaces are not realizable by lines, while orientable ones may or may not be.
</div>


[^dbe]: N. G. de Bruijn, P. Erdős, On a combinatorial problem, *Indagationes Mathematicae* 10 (1948), 421–423.
[^mel]: E. Melchior, Über Vielseite der projektiven Ebene, *Deutsche Mathematik* 5 (1940/41), 461–475.
[^cs]: J. Csima, E. T. Sawyer, There exist $6n/13$ ordinary points, *Discrete & Computational Geometry* 9 (1993), 187–202, [doi:10.1007/BF02189318](https://doi.org/10.1007/BF02189318).
[^hir]: F. Hirzebruch, Arrangements of lines and algebraic surfaces, in *Arithmetic and Geometry II*, Progress in Mathematics 36, Birkhäuser 1983, 113–140, [doi:10.1007/978-1-4757-9286-7_7](https://doi.org/10.1007/978-1-4757-9286-7_7); the form with coefficients $2k-9$ is stated in P. Pokora, Hirzebruch-type inequalities viewed as tools in combinatorics, *Electronic Journal of Combinatorics* 28 (2021), P1.9, Remark 14.
[^km]: L. M. Kelly, W. O. J. Moser, On the number of ordinary lines determined by $n$ points, *Canadian Journal of Mathematics* 10 (1958), 210–219, Theorem 4.1, [doi:10.4153/CJM-1958-024-6](https://doi.org/10.4153/CJM-1958-024-6).
[^ell]: P. D. T. A. Elliott, On the number of circles determined by $n$ points, *Acta Mathematica Academiae Scientiarum Hungaricae* 18 (1967), 181–188, Theorem 3, [doi:10.1007/BF02020972](https://doi.org/10.1007/BF02020972).
[^fl]: J. Folkman, J. Lawrence, Oriented matroids, *Journal of Combinatorial Theory, Series B* 25 (1978), 199–236; see also Björner et al., *Oriented Matroids*, 2nd ed., Cambridge 1999, Theorem 6.2.3.
[^bgs]: S. A. Burr, B. Grünbaum, N. J. A. Sloane, The orchard problem, *Geometriae Dedicata* 2 (1974), 397–424, [doi:10.1007/BF00147569](https://doi.org/10.1007/BF00147569); OEIS A003035.

## B. The three sieves

<div class="thm" markdown>
**Proposition B1.** <span class="status-proved">proved</span> $a(n) = \mathrm{A072964}(n-1)$ for all $n \ge 1$.
</div>
*Proof* on the [arithmetic page](sequences/arithmetic.md).

<div class="thm" markdown>
**Theorem B2.** <span class="status-computed">computer-verified</span> $b(n) = 1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384$ for $n = 1, \dots, 12$.
</div>
<div class="proof" markdown>
*Proof.* For $n \le 2$ the only type is the empty one. For $3 \le n \le 12$ the exhaustive search of
[Algorithm 1](algorithms.md) decided every admissible type without time-outs; completeness of the search is argued there.
The counts of `YES` answers are the stated values (`runs/comb_{n}.json`). The SAT encoding (Algorithm 2) returns the same
verdict on every type for $n \le 12$. <span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Theorem B3.** <span class="status-computed">computer-verified</span> $c(n) = 1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180$ for $n = 1, \dots, 11$,
and $335 \le c(12) \le 337$.
</div>
<div class="proof" markdown>
*Proof.* *Lower bounds.* The certificates in `data/certificates/n{n}.json`, one per type, are all accepted by the exact
verifier; Theorem D1 below explains why acceptance proves realizability.

*Upper bounds.* Every combinatorially possible type without a certificate is excluded in one of three ways:

* by Theorem A2, A3 or A1, applied to its $t_k$;
* because it has no orientable linear space (Algorithm 3, engine mode 4, `runs/orient_{n}.json`; the SAT implementation
  agrees where it finished);
* for $n = 12$, because it is $\{4^9\}$ (Proposition C3), $\{3^{20}\}$ (Proposition C3a), or $\{6, 4, 3^{12}\}$ or
  $\{6, 3^{14}\}$ (Theorems C4 and C5).

The classification files `data/results/classification_n{n}.json` list the reason for every type. For $n = 12$ two types
remain open, whence the upper bound $335 + 2$. <span class="qed">$\square$</span>
</div>

## B′. The band theorem {#bands}

What does an arrangement look like near its largest pencil? Remove the $m$ lines of the largest pencil (centre $P$):
what remains is an arrangement $\mathcal A'$ of $k = n - m$ lines, and every intersection point of the original
arrangement is either $P$, or an intersection point $p$ of $\mathcal A'$ (with multiplicity $\mu'(p)$, raised by one
if a pencil line passes through $p$ — we say $p$ is *absorbed*), or an ordinary point on a pencil line.

<div class="thm" markdown>
**Theorem B4 (bands).** <span class="status-proved">proved</span> Take a realizable arrangement of $k$ lines, list the
multiplicities of all its intersection points (double points included), add $1$ to the multiplicities of an arbitrary
subset of these points, and keep the entries $\ge 3$. Let $\mathrm{BAND}(k)$ be the set of multisets obtained in this way,
and $N(k) = \lvert\mathrm{BAND}(k)\rvert$. Then:

1. for every $n$, a type whose largest entry is $m = n - k$ is realizable only if the rest of it belongs to $\mathrm{BAND}(k)$;
2. if $n \ge 2$ and $m = n - k \ge \max\bigl(\binom k2, k + 1\bigr)$, every such type is realizable, so the number of
   realizable types of $n$ lines with largest pencil exactly $m$ equals $N(k)$, independently of $n$.

The condition on $m$ is needed: for $n = 6$ and $k = 3$ the element $\{4\}$ of $\mathrm{BAND}(3)$ would make the
largest pencil $4$, not $m = 3$, and only $4 = N(3) - 1$ types occur.

Moreover, if $S$ is the set of absorbed points, the number of intersection points is
$f_0 = 1 + km + f_0(\mathcal A') - \sum_{p \in S}\mu'(p)$.
</div>
<div class="proof" markdown>
*Proof.* (1) A point on a pencil line other than $P$ lies on exactly one pencil line, so its multiplicity is one more
than the number of lines of $\mathcal A'$ through it. It is therefore either an absorbed point of $\mathcal A'$ or an
ordinary point, and the type has the stated form.

(2) Choose $P$ off the lines of $\mathcal A'$ and off every line joining two of its intersection points. Join $P$ to the
points to be absorbed (at most $\binom k2 \le m$ of them) and add generic lines through $P$ until there are $m$. Besides
the absorbed points only ordinary points are created, and no point has more than $m$ lines because
$\mu'(p) + 1 \le k + 1 \le m$.

The formula for $f_0$ is a direct count of the points along the pencil lines; full details are in `notes/bands.md`.
<span class="qed">$\square$</span>
</div>

$N(k) = 1, 1, 2, 5, 12, 30, 74, 176, 401$ for $k = 0, \dots, 8$. The data for $n \le 13$ agree with the theorem wherever it
applies. Part (1) is a sieve in its own right: at $n = 13$ it excludes 41 types that pass every other test,
and part (2) builds certificates on demand (`scripts/bands.py`). Applied to $f_0$, the formula gives the bands of
Salamon and Erdős with a one-line proof; see the [points page](sequences/points.md).

## C. Particular configurations

<div class="thm" markdown>
**Proposition C1 (the pentagram needs $\sqrt 5$).** <span class="status-proved">proved</span> Every arrangement of ten
lines of type $\{5, 3^{10}\}$ is projectively equivalent to the regular pentagram together with its five axes of
symmetry. In particular no such arrangement has all its lines defined over $\mathbb Q$.
</div>
<div class="proof" markdown>
*Proof.* We work in the dual picture: ten points, one line $L$ through five of them, ten lines through three of them,
and $t_2 = 45 - 10 - 30 = 5$ lines through two of them, sixteen lines in all. Call the points on $L$ $Q_1, \dots, Q_5$ and
the other points $X_1, \dots, X_5$. A line other than $L$ meets $L$ in at most one point, so each 3-point line consists
either of one $Q_i$ and two $X$'s, or of three $X$'s.

**Step 1: every 3-point line passes through some $Q_i$.** Fix $Q_i$. The lines joining $Q_i$ to the five $X$'s split the
$X$'s into classes, one class per line; a class of size $s$ gives an $(s+1)$-point line, so $s \le 2$. If $g_i$ is the
number of these lines, then $5 - g_i$ of them are 3-point lines. Let $\tau$ be the number of 3-point lines through some
$Q_i$, so that $\sum_i g_i = 25 - \tau$, and let $\lambda$ be the number of lines that contain no $Q_i$. Counting all sixteen
lines,

$$16 = 1 + (25 - \tau) + \lambda, \qquad\text{that is}\qquad \lambda = \tau - 10 .$$

Since there are only ten 3-point lines, $\tau \le 10$, and since $\lambda \ge 0$, we get $\tau = 10$ and $\lambda = 0$. So every
3-point line passes through some $Q_i$, every line through two $X$'s also passes through some $Q_i$, and no three $X$'s
are collinear. Each $Q_i$ lies on exactly two 3-point lines, and these are two disjoint pairs $X_jX_k$, $X_lX_m$.

**Step 2: the combinatorics is unique.** Each $Q_i$ corresponds to a pair of disjoint edges of the complete graph on
$X_1, \dots, X_5$, and the five pairs partition its ten edges. There are exactly six such partitions, and all are
equivalent under relabelling the $X$'s (`scripts/pentagon.py` enumerates them). Up to relabelling,

$$\begin{aligned}
Q_1 &= X_1X_2 \cap X_3X_4, & Q_2 &= X_1X_3 \cap X_2X_5, & Q_3 &= X_2X_4 \cap X_1X_5,\\
Q_4 &= X_3X_5 \cap X_1X_4, & Q_5 &= X_4X_5 \cap X_2X_3.
\end{aligned}$$

In words: each side of the pentagon $X_1X_2X_4X_5X_3$ meets the opposite diagonal in one of the $Q_i$.

**Step 3: the algebra.** Take $X_1, X_2, X_3, X_4$ as the projective frame and $X_5 = (x : y : 1)$. The $Q_i$ are polynomial in
$x$ and $y$, and the condition that all five lie on one line is the vanishing of the ten determinants $\det(Q_a, Q_b, Q_c)$.
A Gröbner basis computation (`scripts/pentagon.py`, output in `notes/pentagon_output.txt`) shows that this system has
exactly two solutions,

$$X_5 = \Big(\tfrac{-1 + \sqrt5}{2} : \tfrac{3 - \sqrt5}{2} : 1\Big) \quad\text{and}\quad \Big(\tfrac{-1 - \sqrt5}{2} : \tfrac{3 + \sqrt5}{2} : 1\Big),$$

both real and non-degenerate (no three $X$'s collinear, the five $Q_i$ distinct). They are the two Galois-conjugate
projective images of the regular pentagon with its axes; in the dual picture the axes are the lines $Q_iX_i$.

**Conclusion.** Every arrangement of type $\{5, 3^{10}\}$ is projectively equivalent to one of these two. A projective
transformation defined over $\mathbb Q$ would keep $X_5$ rational, so no realization is defined over $\mathbb Q$.
<span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Proposition C2 (Fano, Möbius–Kantor, Hesse).** <span class="status-proved">proved</span> The types $\{3^7\}$ ($n = 7$),
$\{3^8\}$ ($n = 8$) and $\{3^{12}\}$ ($n = 9$) are combinatorially possible but not realizable by real lines.
</div>
<div class="proof" markdown>
*Proof.* *Linear spaces.* The Fano plane, the Möbius–Kantor configuration $8_3$, and the affine plane $AG(2,3)$ (the
Hesse configuration $9_4 12_3$); the search of Algorithm 1 finds them.

*Non-realizability.* For $\{3^7\}$, $t_2 = 0$ contradicts Theorem A2; for $\{3^{12}\}$ likewise $t_2 = 36 - 36 = 0$.

For $\{3^8\}$ we have $t_2 = 4$, so the inequalities do not help. The exhaustive search shows that every linear space of this type is the Möbius–Kantor configuration, and that it admits
no orientation (Algorithm 3; classically, Hilbert–Cohn-Vossen §16 or Gropp 1997[^gropp]). <span class="qed">$\square$</span>
</div>

[^gropp]: H. Gropp, Configurations and their realization, *Discrete Mathematics* 174 (1997), 137–151,
    [doi:10.1016/S0012-365X(96)00327-5](https://doi.org/10.1016/S0012-365X(96)00327-5).

<div class="thm" markdown>
**Proposition C3 (nine quadruple points).** <span class="status-proved">proved</span> The type $\{4^9\}$ for twelve lines is
combinatorially possible and unique as a linear space, and not realizable by real lines. Over $\mathbb C$ it is the type
of the Hesse arrangement: the twelve lines of the Hesse configuration, four through each of its nine points.
</div>
<div class="proof" markdown>
*Proof.* Consider twelve elements carrying nine blocks of size 4, any two blocks sharing at most one element. An element
on four blocks would be joined to $4 \cdot 3 = 12 > 11$ other elements, so every element lies on at most three blocks. The
blocks contain $9 \cdot 4 = 36 = 12 \cdot 3$ incidences, so every element lies on exactly three blocks.

Now swap the roles: take the nine blocks as points and the twelve elements as lines, each line consisting of the three
blocks through that element. Two blocks share at most one element, so two of the nine points lie on at most one
common line; and the twelve lines cover $12 \cdot \binom 32 = 36 = \binom 92$ pairs, so every pair lies on exactly one line.
This is a Steiner triple system on nine points, which is unique up to isomorphism: the affine plane $AG(2,3)$, the
Hesse configuration.

Realizability is preserved by duality, and $AG(2,3)$ is not realizable over $\mathbb R$: every pair of its points lies
on a 3-point line, so it has no ordinary line, contradicting the Sylvester–Gallai theorem (Theorem A2). Over
$\mathbb C$ the configuration exists (the nine inflection points of a cubic and their twelve lines), so the obstruction
is genuinely real. <span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Proposition C3a (twenty triple points).** <span class="status-computed">computer-verified</span> The type $\{3^{20}\}$ for
twelve lines is combinatorially possible but not realizable, not even by pseudolines: none of its linear spaces is
orientable.
</div>
<div class="proof" markdown>
*Proof.* Work in the dual picture: twelve points and twenty 3-point lines, which cover $60$ of the $66$ pairs. A point
lies on $(11 - d)/2$ of the 3-point lines, where $d$ is the number of uncovered pairs at that point, so $d$ is odd. The
twelve values of $d$ sum to $2 \cdot 6 = 12$, so every $d$ equals $1$: the uncovered pairs form a perfect matching.

Add a thirteenth point and join it to the two ends of each uncovered pair. The result is a Steiner triple system of
order 13, and conversely deleting a point from a Steiner triple system of order 13 gives a linear space of type
$\{3^{20}\}$. There are exactly two Steiner triple systems of order 13 up to isomorphism.[^cr] Their 26 point
deletions fall into 5 isomorphism classes, and the SAT encoding of Algorithm 3 shows that none of the 26 admits a
chirotope (`scripts/orchard12.py`, `runs/orchard12.json`). <span class="qed">$\square$</span>
</div>

This agrees with the orchard problem: Burr, Grünbaum and Sloane list $19$ as the largest number of 3-point lines for
twelve points.[^bgs]

[^cr]: C. J. Colbourn, A. Rosa, *Triple Systems*, Oxford University Press, 1999.

## C′. Lines versus pseudolines at n = 12 {#lines-vs-pseudolines}

<div class="thm" markdown>
**Theorem C4.** <span class="status-computed">computer-verified</span> The type $\{6, 4, 3^{12}\}$ (twelve lines, 23 intersection
points) is realizable by pseudolines but not by straight lines. More precisely: up to isomorphism there is exactly one
orientable linear space with these block sizes, namely, on the points 0, …, 11:

```
{0,1,2,3,4,5}  {2,6,7,9}
{0,8,9}  {0,10,11}  {1,7,8}  {1,9,10}  {2,8,11}  {3,6,8}
{3,7,10} {3,9,11}   {4,6,10} {4,7,11}  {5,6,11}  {5,8,10}
```

and in every realization of these collinearities by points of the complex projective plane the points $7, 10, 11$ are
collinear as well — so the type that appears is never $\{6, 4, 3^{12}\}$.
</div>
<div class="proof" markdown>
*Proof.* *Uniqueness.* The engine's exhaustive enumeration (mode 5) lists 283 680 linear spaces of the type (labelled,
modulo its symmetry breaking), of which 30 240 are orientable; the exact isomorphism test shows that all orientable
ones are relabellings of the space above (`runs/enum_classes_12_6_4_3x12.json`).

*Forced collinearity.* Take $0, 1, 6, 7$ as projective frame, the points of the 6-block on the line $z = 0$ and the other
points in the affine chart. The 16 collinearity determinants generate an ideal $I$ in 12 unknowns, and the Gröbner basis
of $I + (t \cdot d_{7,10,11} - 1)$ is $\{1\}$ (`data/proofs/n12_6-4-3x12.json`). Hence $d_{7,10,11}$ vanishes on $V(I)$.

*Pseudolines.* Realizability by pseudolines is the Folkman–Lawrence theorem applied to the chirotope found by the
engine. <span class="qed">$\square$</span>
</div>

This is an incidence theorem in the spirit of Pappus, and it also has a short proof by hand.

<div class="proof" markdown>
*Proof by hand.* Send the 6-point line $\{0, \dots, 5\}$ to infinity. The six points $6, \dots, 11$ become affine points
$A, B, C, D, E, F$, and "collinear with a point of the line at infinity" becomes "parallel". The 4-block says that
$A, B, D$ are collinear, and the triples say

$$CD \parallel EF, \qquad BC \parallel DE, \qquad CF \parallel AB, \qquad AC \parallel BE \parallel DF, \qquad AE \parallel BF, \qquad AF \parallel CE .$$

Put $A = 0$, $B = b\,u$, $D = d\,u$ and $C = v$, where $u, v$ are independent (because $A, B, C$ are not collinear) and
$b, d$ are distinct and non-zero. From $AC \parallel BE \parallel DF$ we get $E = b\,u + e\,v$ and $F = d\,u + f\,v$. Then:

* $BC \parallel DE$ gives $d = b(e+1)$;
* $AE \parallel BF$ gives $bf = e(d - b) = b e^2$, so $f = e^2$;
* $AF \parallel CE$ gives $d(e-1) = fb$, that is $b(e+1)(e-1) = be^2$, that is $-1 = 0$.

So the configuration does not exist over any field; the parallelisms $CD \parallel EF$ and $CF \parallel AB$ were not even
needed. This is slightly stronger than the statement of the theorem: under the non-degeneracy conditions used here
($A, B, C$ not collinear, $A, B, D$ distinct) the collinearities have no solution at all, while the Gröbner certificate
only says that every solution, degenerate or not, has $7, 10, 11$ collinear.
<span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Theorem C5.** <span class="status-computed">computer-verified</span> The type $\{6, 3^{14}\}$ (twelve lines, 24 intersection
points) is realizable by pseudolines but not by straight lines. Its orientable linear spaces form exactly four
isomorphism classes (676 080 linear spaces in the exhaustive enumeration, 135 360 of them orientable, with
34 560 + 14 400 + 57 600 + 28 800 labelled copies of the four classes), and for each class a Gröbner certificate shows that
every complex realization of its collinearities has an extra collinear triple: for two classes one specific triple is
forced, for the other two one of two specific triples.
</div>
<div class="proof" markdown>
*Proof.* *Enumeration.* `engine/ls.c`, mode 5.

*Isomorphism classes.* `scripts/canon_dedupe.py` computes an exact canonical form. The 6-block $B$ is unique, so an
isomorphism maps $B$ to itself and the six other points $X$ to themselves. Each point $q \in B$ is recorded by the set
of pairs of $X$ that lie in a block through $q$ (its pair-mask), and the blocks inside $X$ by one more pair-mask. Taking
the $q$-masks as a sorted list removes the labels of $B$; the minimum of (sorted $q$-masks, $X$-mask) over the 720
permutations of $X$ is then a complete invariant. An independent VF2 graph-isomorphism check agrees on the first class.

*Certificates.* `data/proofs/n12_6-3x14.json`; each is verified by a reduced Gröbner basis $\{1\}$ in sympy.
<span class="qed">$\square$</span>
</div>

So the sequence for pseudolines, which agrees with $c(n)$ for $n \le 11$, is at least $c(12) + 2$ at $n = 12$ — the first
place where straight lines are genuinely more restrictive than pseudolines in this counting problem.

## D. The verifier

<div class="thm" markdown>
**Theorem D1 (soundness of certificates).** <span class="status-proved">proved</span> If `verifier/verify.py` accepts a
certificate with field parameter $d$, $n$ lines and type $T$, then there is an arrangement of $n$ distinct lines in
$\mathbb{RP}^2$ whose pencil type is $T$; its lines are the given coefficient vectors read in $\mathbb Q(\sqrt d)
\subset \mathbb R$.
</div>
<div class="proof" markdown>
*Proof.* *Exact arithmetic.* The program represents elements of $\mathbb Z[\sqrt d]$ as integer pairs and uses only ring
operations, so every computed quantity is the exact value of the corresponding expression in the real number $\sqrt d$.
An element $p_0 + p_1\sqrt d$ with integers $p_0, p_1$ is zero iff $p_0 = p_1 = 0$, because $d$ is checked to be $0$ or a
positive non-square integer, so $\sqrt d$ is irrational (or absent). Hence every zero test is exact.

*Distinct lines.* The program checks that each line is a non-zero vector and that no two are proportional (cross product
non-zero), so the $n$ lines are distinct.

*The type.* For each pair $i < j$ it computes the intersection point $P = L_i \times L_j$ and the set $S_{ij} = \{k : L_k \cdot P = 0\}$
of *all* lines through $P$; the distinct sets $S_{ij}$ are exactly the intersection points of the arrangement with
their pencils, so the multiset of their sizes is the pencil type. Acceptance means this multiset, restricted to sizes
$\ge 3$, equals $T$. <span class="qed">$\square$</span>
</div>

The verifier is deliberately dumb: it never merges pairs, never uses floating point, never trusts a field of the
certificate other than the numbers. Its tests (`verifier/test_verify.py`) check that Pappus, Desargues, the
pentagram and generic arrangements are accepted and that every single-number perturbation of a rigid configuration,
wrong fields, duplicated lines, wrong types and floating-point coordinates are rejected.

## E. Intersection points {#points}

The proofs of Theorems 1–3 of the [points page](sequences/points.md) are given in full in the repository notes
(`notes/points.md`); we summarise the structure of the proof of the main theorem and give the one ingredient that is
not a one-liner.

<div class="thm" markdown>
**Lemma E1 (spoke bound).** <span class="status-proved">proved</span> Let $P$ be a point of maximal multiplicity $m$ in an
arrangement of $n$ lines, $b = n - m$. For each line $L$ through $P$ let $g_L$ be the number of points on $L$ other than $P$.
Then $f_0 \ge 1 + \sum_L g_L$; each $g_L$ partitions the $b$ lines not through $P$ into $g_L$ classes of sizes $\le m - 1$
(the lines through one point of $L$); and the total number of pairs of free lines inside classes, over all $L$, is at
most $\binom b2$. Consequently $f_0 \ge 1 + G(n, b)$ for the integer programme $G$ defined in `notes/points.md`, and in
closed form $f_0 \ge 1 + mb - \binom b2$ (Kelly–Moser's Lemma 4.1).
</div>

<div class="thm" markdown>
**Lemma E2 (Melchior bound).** <span class="status-proved">proved</span> If $\mathcal A$ is not a pencil and $m$ is its
largest multiplicity, $f_0 \ge \dfrac{n(n-1) + 3m + 3}{m + 3}$.
</div>
<div class="proof" markdown>
*Proof.* From Theorem A2 and $t_2 = \binom n2 - \sum_{k\ge3}\binom k2 t_k$: $\sum_{k\ge3}(\binom k2 + k - 3)t_k \le \binom n2 - 3$.
The loss is $\sum_{k\ge3}(\binom k2 - 1)t_k$ and $(\binom k2 - 1)/(\binom k2 + k - 3) = (k+1)/(k+3)$ increases with $k$, so the
loss is at most $\frac{m+1}{m+3}(\binom n2 - 3)$. <span class="qed">$\square$</span>
</div>

<div class="thm" markdown>
**Theorem E3.** <span class="status-proved">proved, computer-assisted</span> For $n \ge 13$: if no $n - 2$ lines are concurrent then $f_0 \ge 2n-2$.
</div>
<div class="proof" markdown>
*Proof.* Let $m \le n - 3$ be the largest multiplicity and $b = n - m \ge 3$. There are three ranges of $n$.

*Case $n \ge 36$.* If $b \le (2n-9)/3$, Lemma E1 gives $f_0 \ge 1 + mb - \binom b2 \ge 2n - 2$: the difference is
$n(b-2) - \frac{3b^2 - b - 6}2$, which is $\ge 0$ when $n \ge \frac32 b + \frac92$. Otherwise $m < (n+9)/3$, and Lemma E2
gives $f_0 > \frac{3n(n-1)}{n+18} \ge 2n-2$, because $n^2 - 37n + 36 \ge 0$.

*Case $17 \le n \le 120$.* The script `scripts/f0_bounds.py` checks that
$\max(1 + G(n,b), \lceil\text{Lemma E2}\rceil) \ge 2n-2$ for every $m \le n-3$. This range overlaps the previous one.

*Case $13 \le n \le 16$.* The same check succeeds except for $(n, m) = (13, 5), (14, 5), (14, 6), (15, 6), (16, 6)$. For
these five pairs a linear programme over $(t_2, \dots, t_m)$ with the pair identity, Theorem A2, Theorem A4 (with
coefficients $k - 4$) and $t_m \ge 1$ has optimum $\ge 2n - 2$. The script prints exact dual multipliers and re-verifies
them coefficientwise in rational arithmetic.

For example, for $(13, 5)$ the multipliers $\alpha = \frac5{24}$ (pairs), $\beta = \frac7{24}$ (Melchior) and
$\gamma = \frac12$ (Hirzebruch) satisfy

$$\alpha\tbinom k2 + \beta\,\mathrm{mel}_k + \gamma\,\mathrm{hir}_k = 1,\ 1,\ \tfrac{23}{24},\ 1 \qquad (k = 2, 3, 4, 5),$$

hence $f_0 \ge \frac5{24}\cdot 78 + \frac7{24}\cdot 3 + \frac12 \cdot 13 = 23.625$, that is $f_0 \ge 24$.
<span class="qed">$\square$</span>
</div>

Together with Lemma 2 of the points page (largest pencil of size $\ge n-2$) this gives
$V(n) \cap [1, 2n-2] = \{1, n, 2n-4, 2n-2\}$ for $n \ge 13$, and in particular **$2n - 3$ is never the number of intersection
points of $n \ge 13$ lines**. For $n = 12$ the same conclusion ($21 \notin V(12)$) is computer-verified. It is false for $n = 3$ and for
$6 \le n \le 11$, and true for $n = 4, 5$.

<div class="thm" markdown>
**Theorem E4.** <span class="status-computed">computer-verified</span> $d(n) = 1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56$ for $n = 1, \dots, 13$.
</div>
<div class="proof" markdown>
*Proof.* For each $n$ the certificates give the attained values listed on the points page. The missing values are
excluded as follows.

* $2, \dots, n-1$: by Theorem A1.
* $n+1, \dots, 2n-5$: by Theorem A6 for $n \ge 10$, and by the classification for $n \le 9$.
* $\binom n2 - 1$ and $\binom n2 - 3$: by Theorem 1 of the points page.
* The sporadic values $8$ ($n = 7$), $9, 10$ ($n = 8$), $10, 11, 12$ ($n = 9$) and $21$ ($n = 12$): every admissible type
  with that $f_0$ is non-realizable (classification files).
* $23$ for $n = 13$: by Theorem E3. Independently, all 81 admissible types with $f_0 = 23$ fail the combinatorial sieve
  or Theorem A2 (`runs/comb_13_f23.json`, `runs/sat_13_f23.json`).

<span class="qed">$\square$</span>
</div>

## F. What is conjectured

See the [open problems](open.md) page for conjectures and the evidence for them. Nothing on this page depends on them.
