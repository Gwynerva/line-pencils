# Setting, definitions and the three sieves

## Arrangements and pencil types

An **arrangement** $\mathcal A$ is a finite set of $n \ge 1$ distinct lines in the real projective plane
$\mathbb{RP}^2$. Any two lines meet in exactly one point. For a point $P$ let $\mu(P)$ be the number of lines of
$\mathcal A$ through $P$; a point with $\mu(P) \ge 2$ is an **intersection point** (vertex), and the set of lines
through it is a **pencil** of size $\mu(P)$. Following Grünbaum, $t_k(\mathcal A)$ denotes the number of
intersection points with $\mu = k$, and $f_0(\mathcal A) = \sum_{k\ge2} t_k$ the number of intersection points.
Counting pairs of lines,
$$\sum_{k \ge 2} \binom k2\, t_k = \binom n2 .$$

The **pencil type** (t-vector, "weak combinatorics") of $\mathcal A$ is the multiset of the sizes of its pencils:
$\{k^{t_k} : k \ge 2\}$. Since $t_2$ is determined by the others, we write a type by its pencils of size $\ge 3$ only,
as a non-increasing list, e.g. $\{6, 4, 3^{12}\}$ for $n = 12$ (where $t_2 = 66 - 15 - 6 - 36 = 9$).

**Affine versus projective.** The elementary question is about $n$ lines in the Euclidean plane, no two parallel.
Such an arrangement sits inside $\mathbb{RP}^2$ with the same pencils (no new points: parallel classes do not
exist). Conversely, given a projective arrangement, choose a line $\ell_\infty$ through none of its finitely many
intersection points and not in $\mathcal A$; in the affine plane $\mathbb{RP}^2 \setminus \ell_\infty$ the lines of
$\mathcal A$ are pairwise non-parallel (parallel lines would meet on $\ell_\infty$) and have the same pencils.
So the two settings have exactly the same pencil types, and we work projectively.

**Duality.** The projective duality $(a:b:c) \leftrightarrow \{ax + by + cz = 0\}$ maps an arrangement of $n$ lines to a
set of $n$ points, and a pencil of $k$ lines to a line containing exactly $k$ of the points. Thus pencil types of $n$
lines are the same as the multisets of sizes of the "rich" lines ($\ge 3$ points) determined by $n$ points in the
plane. The classical literature (Sylvester–Gallai, Melchior, Kelly–Moser, the orchard problem) is mostly written in the
point language; we translate freely. Certificates in `data/certificates/` store the $n$ lines by their coefficient
vectors, which are the same numbers as the dual points.

## The four sequences

For $n \ge 1$:

* $a(n)$ = number of **arithmetically admissible** types: multisets $\{k_1, \dots, k_r\}$ with $3 \le k_i \le n$ and
  $\sum \binom{k_i}2 \le \binom n2$. (The remaining pairs are double points.) This is the number of partitions of
  $\binom n2$ into triangular numbers $\binom k2$, $k \ge 2$, i.e. OEIS A072964$(n-1)$.
* $b(n)$ = number of **combinatorially possible** types: those for which a *linear space* exists — a family of
  blocks of the prescribed sizes on $n$ points, any two blocks sharing at most one point (the uncovered pairs are
  2-point blocks). Equivalently, a simple rank-3 matroid / a $(v_r, b_k)$-configuration in the broad sense.
* $c(n)$ = number of **realizable** types: types of actual arrangements of $n$ real lines.
* $d(n)$ = number of distinct values of $f_0$ over arrangements of $n$ lines.

Clearly $c(n) \le b(n) \le a(n)$; the three sets of types are the three **sieves**. For $n = 1$ there is one line
and no intersection point: the empty type is counted once, so $a(1) = b(1) = c(1) = d(1) = 1$ (with $f_0 = 0$ the
only value). This offset convention is a choice to be confirmed by the author before the OEIS submission.

## Why the sieves differ

* $a > b$ from $n = 4$: $\{3, 3\}$ is arithmetically fine for 4 lines ($3 + 3 \le 6$) but two triple points would share
  two lines.
* $b > c$ from $n = 7$: the Fano plane $\{3^7\}$ is a linear space but not a real arrangement (Sylvester–Gallai /
  Melchior: a real arrangement that is not a pencil has an ordinary point).
* **Orientability** is the computable intermediate step between $b$ and $c$: every real arrangement gives a chirotope
  (signs of $3\times3$ determinants) satisfying the three-term Grassmann–Plücker relations; a linear space admitting
  no chirotope is not realizable. The converse fails (Pappus: the non-Pappus configuration is orientable but not
  realizable), and this is exactly where the remaining open cases at $n = 12$ live.

## Necessary conditions used as filters

For an arrangement that is not a pencil:

* de Bruijn–Erdős (dual): $f_0 \ge n$.
* Melchior: $t_2 \ge 3 + \sum_{k\ge4}(k-3)t_k$.
* Csima–Sawyer: $t_2 \ge 6n/13$ for $n \ge 8$ (the only exception to $t_2 \ge 6n/13$ for all $n$ is the Kelly–Moser
  arrangement with $n = 7$).
* Hirzebruch (for $t_n = t_{n-1} = t_{n-2} = 0$): $t_2 + \frac34 t_3 \ge n + \sum_{k\ge5}(2k-9)t_k$. (Used only in
  `notes/points.md`.)

Each of these is applied to a type (they depend on the $t_k$ only), and each is a theorem about real lines, so
a type violating one is not realizable even if it is combinatorially possible.
