---
description: "What is still unknown about how n lines can meet: the undecided cases for 13 lines, the number of intersection points for 14 lines and more, growth rates, and related questions worth exploring."
---

# Open problems and where to dig

What is not known: the undecided terms, conjectures supported by the data, and related questions.

## 1. Twelve lines: settled

$c(12) = 336$. The last two types were decided in opposite directions: $\{3^{18}\}$ is realizable with small integer
coefficients ([Example C3c](theorems.md#c3c)), and $\{4^5, 3^9\}$ is not even orientable ([Proposition C3b](theorems.md#c3b)).
Two types, $\{6, 4, 3^{12}\}$ and $\{6, 3^{14}\}$, are proved non-realizable although they are orientable: **the pencil
types of 12 lines and of 12 pseudolines differ** ([Theorems C4, C5](theorems.md#lines-vs-pseudolines)).

How the orientable cases were settled: for a single linear space, non-realizability is a statement about the solutions of a polynomial
system; we prove it by exhibiting non-collinear triples whose determinants' product lies in the radical of the
incidence ideal (a certificate of explicit cofactors, checked by `verify.py --algebraic`; see the
[algorithms page](algorithms.md)); an incidence theorem (like
Pappus for the non-Pappus configuration) is the human-readable special case. For a *type*, every orientable linear
space of that type must be treated, which requires the engine's complete enumeration (mode 5) and an exact
isomorphism reduction. The outcome for $\{6, 3^{14}\}$ and $\{6, 4, 3^{12}\}$ is recorded on the
[theorems page](theorems.md#lines-vs-pseudolines).

## 2. Thirteen lines

$620 \le c(13) \le 659$: 620 types have certificates and 39 are undecided. The constructive searches of the
[algorithms page](algorithms.md#zone-walk) (zone walk, targeted deformation, mirror sections) found no numerical solution for any of the 39, which suggests that
most of them are not realizable. Deciding them needs the orientability
search and, where it says "orientable", the algebraic method used at $n = 12$; several of these types are harder than
anything at $n = 12$.

## 3. How fast do b(n) and c(n) grow?

<div class="thm openp" markdown>
**Open problem.** Determine the exponent $\theta$ such that $\log c(n) = n^{\theta + o(1)}$ (and the same for $b$).
</div>

Known: $\log a(n) \asymp n^{2/3}$ (partitions into triangular numbers) and $\log c(n) \gtrsim n^{1/2}$ (pencils that share
no lines realize every partition of $m \le n$ into parts $\ge 3$). The ratios $c(n)/a(n)$ for $n = 6, \dots, 12$ are
$0.60, 0.50, 0.42, 0.38, 0.33, 0.29, 0.26$: geometry eats a growing share of the arithmetic candidates, but slowly.
A better lower bound would come from a construction that realizes many types at once; a better upper bound from a
structural restriction on how many large pencils can coexist (Melchior's inequality is such a restriction, but it
says nothing about triple points, whose coefficient in it is $0$).

## 4. The intersection-point sequence beyond n = 13

<div class="thm openp" markdown>
**Open problem.** Can 14 straight lines have 28 intersection points? Can 15 straight lines have 32?
These cases determine $d(14)\in\{65,66\}$ and $d(15)\in\{76,77\}$.
See the [points page](sequences/points.md#using-kims-classifications) for the exclusions, constructions, and the remaining values for $n=16$.
</div>

The precise threshold $n^*$ from which the Salamon–Erdős description of $V(n)$ is exact is open (they expect it to be
small). Theorem E3 proves one feature of it: the four smallest values are $1, n, 2n-4, 2n-2$, which holds from $n = 12$ on
(for $n = 12$ by computation).

## 5. Fields of definition

<div class="thm openp" markdown>
**Open problem.** Is there a pencil type, for some $n$, all of whose real realizations need an irrationality of degree
$\ge 3$? Is $\{5, 3^{10}\}$ ($n = 10$) the smallest type that is not realizable over $\mathbb Q$?
</div>

For $n \le 14$ all our certificates are over $\mathbb Q$ or $\mathbb Q(\sqrt d)$, $d \in \{2, 3, 5\}$, but except for the
pentagram we never proved that the irrationality is needed; most of the $\sqrt d$ examples probably have rational cousins.
Rational realizability is a different sieve ("drawable on graph paper") that would give yet another sequence.

## 6. Other geometries

The same question makes sense elsewhere. Apart from pseudolines (Theorems C4, C5) and a first look at planes, we have
not studied these:

* **Pseudolines.** Replace lines by curves that pairwise cross exactly once. Orientability becomes the exact criterion
  (Folkman–Lawrence), so the sequence is computable in principle; it agrees with $c(n)$ for $n \le 11$ and exceeds it at
  $n = 12$ (problem 1).
* **Complex lines.** The Fano type is still impossible, but Möbius–Kantor ($n = 8$) and Hesse ($n = 9$) become possible:
  the complex sequence is $1, 1, 2, 3, 5, 9, 16, 29, \ge 54, \dots$
* **Planes in space, hyperplanes in higher dimensions.** For $n$ planes in real projective space, two planes meet in a
  line, and the analogue of a pencil is a line lying on $k \ge 3$ planes or a point lying on more planes than in
  general position; the type has to record both, together with which lines pass through which points. The same three sieves apply
  (arithmetic, the combinatorics of rank-4 matroids, real realizability), and $d$ has two analogues, the numbers
  of intersection lines and of intersection points. A generic plane cuts the arrangement in an arrangement of $n$
  lines whose pencils are the lines of the space arrangement, so the planar types are a shadow of the spatial ones. The page [Planes in space](planes.md) proposes a definition and gives the counts for $n \le 8$.
* **Lines over finite fields; the sphere (great circles, where every pencil doubles); the hyperbolic plane (where
  non-intersecting lines appear and $f_0$ can be anything from $0$ to $\binom n2$).**

## 7. Pencil types and the orchard problem

$c(n)$ contains the orchard problem: the maximal $t_3$ for $n$ lines is the largest $t$ with $\{3^t\} \cup$ (anything)
realizable. Conversely the orchard literature gives the only non-trivial *upper* bounds we know for a single pencil
size (A003035: $19$ for $n = 12$, $22$ for $n = 13$). For $n = 12$ we reproved the bound for the type $\{3^{20}\}$ alone:
its linear spaces are the Steiner triple systems of order 13 minus a point, and none of them is orientable
([Proposition C3a](theorems.md#c3a)).
