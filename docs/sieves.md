# The three sieves

The sequences count what survives three successive tests: arithmetic, combinatorics and geometry. This page
explains the tests, shows where each one first matters, and introduces orientability, a computable test between
the last two.

<figure class="fig" markdown="1">

--8<-- "fig/sieves.svg"

<figcaption>Twelve lines: 1286 types pass the arithmetic test, 384 pass the combinatorial test, between 335 and 337 are realizable.</figcaption>
</figure>

## Sieve 1: arithmetic

A point on $k$ lines accounts for $\binom k2$ pairs of lines, and there are only $\binom n2$ pairs. So a type
$\{k_1, \dots, k_r\}$ (sizes $\ge 3$) is admissible only if $\sum_i \binom{k_i}2 \le \binom n2$; the leftover pairs are
ordinary points. The number $a(n)$ of admissible types is the number of partitions of the triangular number
$\binom n2$ into triangular numbers $\binom k2$ with $k \ge 2$, which is the OEIS sequence A072964 shifted by one:
$a(n) = \mathrm{A072964}(n-1)$.[^a072964] Admissibility is all that arithmetic says, and it is far from sufficient.

[^a072964]: OEIS Foundation Inc., *The On-Line Encyclopedia of Integer Sequences*, entry A072964, "Number of
    partitions of the $n$-th triangular number into triangular parts", https://oeis.org/A072964.

**Where it fails first: $n = 4$.** The type $\{3, 3\}$ passes ($3 + 3 \le 6$) but two triple points among four lines would
have to share two lines, and two lines meet only once.

## Sieve 2: combinatorics (linear spaces)

Two pencils share at most one line. So the pencils of size $\ge 3$ of an arrangement form a family of blocks on the
$n$ lines, any two blocks meeting in at most one line; adding the ordinary points as 2-blocks, every pair of lines
lies in exactly one block. Such a structure is a **linear space** (equivalently a simple matroid of rank $\le 3$).
A type is *combinatorially possible* if some linear space has blocks of exactly these sizes.

Deciding this is a finite search, and the number of linear spaces on $n$ points grows fast (A001200: 232 929 for
$n = 12$, 28 872 973 for $n = 13$[^a001200]); the [algorithms page](algorithms.md) explains how the search is organised
so that all $1286$ admissible types for $n = 12$ are decided in about a minute, and how a SAT solver was used as an
independent check.

[^a001200]: OEIS A001200, "Number of linear geometries on n (unlabeled) points"; the term for $n = 12$ is from
    A. Betten, D. Betten, Linear spaces with at most 12 points, *Journal of Combinatorial Designs* 7 (1999), 119–145.

**Where it is first not enough: $n = 7$.** The Fano plane — seven points, seven lines of three,
every pair of points on a line — is a perfectly good linear space of type $\{3^7\}$. It cannot be drawn with real
lines: a real arrangement that is not a pencil always has an ordinary point (the Sylvester–Gallai theorem, in its
dual form), and the Fano type has $t_2 = 21 - 21 = 0$.

## Sieve 3: geometry (real realizability)

A type is *realizable* if it is the type of an arrangement of $n$ lines in $\mathbb{RP}^2$. Realizability is a
question about real solutions of polynomial equations (the $3\times 3$ determinants of concurrent triples must vanish,
all others must not), decidable in principle by Tarski's theorem and hopeless in practice beyond tiny cases. Two
kinds of tools decide it for us:

* **Certificates.** If a type is realizable we exhibit coordinates, in $\mathbb Q$ or in a quadratic field
  $\mathbb Q(\sqrt d)$, and an independent [verifier](data.md) recomputes the type with exact arithmetic.
  Some types need the irrationality: $\{5, 3^{10}\}$ for ten lines is a regular pentagram with its axes, and the
  pentagon forces $\sqrt 5$ (see the [theorems page](theorems.md)).
* **Obstructions.** Classical inequalities valid for all real arrangements (Melchior, Csima–Sawyer, Hirzebruch),
  the de Bruijn–Erdős bound on the number of points, and **orientability**.

### Orientability: the sieve between the sieves

Give coordinates $p_1, \dots, p_n \in \mathbb R^3$ to the dual points. The signs of the determinants
$\chi(i,j,k) = \operatorname{sign}\det(p_i, p_j, p_k)$ form a **chirotope**: an alternating sign function on triples
that vanishes exactly on the collinear triples and satisfies, for all $a$ and all $x_1, x_2, x_3, x_4$, the
**three-term Grassmann–Plücker relation**:

> among $\chi(a x_1 x_2)\chi(a x_3 x_4)$, $-\chi(a x_1 x_3)\chi(a x_2 x_4)$, $\chi(a x_1 x_4)\chi(a x_2 x_3)$ either all three are $0$ or both signs $+$ and $-$ occur.[^blswz]

[^blswz]: A. Björner, M. Las Vergnas, B. Sturmfels, N. White, G. M. Ziegler, *Oriented Matroids*, 2nd ed.,
    Cambridge University Press, 1999, Definition 3.5.3 and Theorem 3.6.2, [doi:10.1017/CBO9780511586507](https://doi.org/10.1017/CBO9780511586507).

A linear space is *orientable* if such a chirotope exists with the blocks as its zero set. Every real arrangement is
orientable, so **a type none of whose linear spaces is orientable is not realizable.** Orientability is a finite
combinatorial condition — a Boolean satisfiability problem. It excludes, for example, the Möbius–Kantor
configuration $\{3^8\}$ ($n = 8$): it passes every classical inequality and exists as a linear space, even as an
arrangement of complex lines, but admits no orientation.

Orientability is not sufficient. By the Folkman–Lawrence theorem[^fl] an orientable linear space is realizable by
*pseudolines*, curves that pairwise cross once, and pseudolines can do what lines cannot: the **non-Pappus**
configuration (the nine points of Pappus's theorem with the conclusion line removed) is orientable, but any
straight-line realization would have the ninth collinearity forced by Pappus's theorem.

[^fl]: J. Folkman, J. Lawrence, Oriented matroids, *Journal of Combinatorial Theory, Series B* 25 (1978), 199–236,
    [doi:10.1016/0095-8956(78)90039-4](https://doi.org/10.1016/0095-8956(78)90039-4).

For $n \le 11$ this gap never mattered: every combinatorially possible type is either realizable or excluded by an
inequality or by non-orientability. At $n = 12$ it does matter: $\{6, 4, 3^{12}\}$ and $\{6, 3^{14}\}$ are orientable
but not realizable ([Theorems C4, C5](theorems.md#lines-vs-pseudolines)).

## Summary for small n

| $n$ | arithmetic $a(n)$ | combinatorial $b(n)$ | realizable $c(n)$ | combinatorially possible, not realizable |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | |
| 2 | 1 | 1 | 1 | |
| 3 | 2 | 2 | 2 | |
| 4 | 4 | 3 | 3 | |
| 5 | 7 | 5 | 5 | |
| 6 | 15 | 9 | 9 | |
| 7 | 32 | 17 | 16 | Fano $\{3^7\}$ |
| 8 | 66 | 29 | 28 | Möbius–Kantor $\{3^8\}$ |
| 9 | 141 | 56 | 53 | Hesse $\{3^{12}\}$, $\{3^{11}\}$, $\{4^2, 3^7\}$ |
| 10 | 295 | 106 | 98 | eight types, e.g. $\{3^{13}\}$ |
| 11 | 619 | 202 | 180 | 22 types |
| 12 | 1286 | 384 | 335 … 337 | 47 to 49 types; see [what cannot be drawn](impossible.md) |
