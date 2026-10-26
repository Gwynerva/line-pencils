# The band theorem for pencil types

Let $\mathcal A$ be an arrangement of $n$ lines whose largest pencil has exactly $m$ lines, $k = n - m$, with centre $P$.
Removing the $m$ lines through $P$ leaves an arrangement $\mathcal A'$ of $k$ lines, none through $P$ (every line through
$P$ belongs to the pencil). For an intersection point $p$ of $\mathcal A'$ write $\mu'(p)$ for its multiplicity in
$\mathcal A'$, and say that $p$ is *absorbed* if a pencil line passes through it; $S$ denotes the set of absorbed points.

**Lemma 1 (dissection).** The pencil type of $\mathcal A$ is
$$\{m\} \;\cup\; \{\mu'(p) + 1 : p \in S\} \;\cup\; \{\mu'(p) : p \notin S\} \qquad(\text{entries } 2 \text{ omitted as usual}),$$
and its number of intersection points is
$$f_0(\mathcal A) = 1 + km + f_0(\mathcal A') - \sum_{p \in S} \mu'(p).$$

*Proof.* A point $q \ne P$ on a pencil line $\ell$ lies on exactly one pencil line, so $\mu(q) = 1 + (\text{number of lines of }
\mathcal A' \text{ through } q)$: if that number is $\ge 2$, $q$ is an absorbed point of $\mathcal A'$ with $\mu(q) = \mu'(q) + 1$; if
it is $1$, $q$ is an ordinary point. Points off the pencil lines are the non-absorbed points of $\mathcal A'$ with unchanged
multiplicity. This gives the type. Counting points on $\ell$ other than $P$: the $k$ incidences of $\ell$ with $\mathcal A'$
are grouped into points, an absorbed point $p$ accounting for $\mu'(p)$ of them; so $\ell$ carries $k - \sum_{p \in S \cap \ell}(\mu'(p) - 1)$
points. Summing over the $m$ pencil lines, adding $P$ and the $f_0(\mathcal A') - |S|$ non-absorbed points gives the formula. $\square$

**Lemma 2 (construction).** Let $T'$ be a realizable type of $k$ lines, $\mathcal A'$ a realization, $S$ any set of
intersection points of $\mathcal A'$, and $m \ge \max(|S|, \max_p \mu'(p) + 1, 2)$. Then there is an arrangement of $n = m + k$
lines with largest pencil exactly $m$, whose dissection is $(\mathcal A', S)$ with every pencil line through at most one point
of $S$.

*Proof.* Choose $P$ outside the finitely many lines of $\mathcal A'$ and outside the finitely many lines joining two
intersection points of $\mathcal A'$. For $p \in S$ take the line $Pp$: it passes through no other intersection point of
$\mathcal A'$ (by the choice of $P$) and meets the lines of $\mathcal A'$ not through $p$ in points that are not intersection
points of $\mathcal A'$ (else $P$ would be collinear with two intersection points). Add $m - |S|$ further lines through
$P$, each avoiding the finitely many directions in which a line through $P$ would pass through an intersection point of
$\mathcal A'$ or through an intersection of an already added line with $\mathcal A'$. All intersection points created on the
new lines are then ordinary except the absorbed ones, and $P$ has multiplicity $m$, which is the largest since every other
multiplicity is at most $\max_p \mu'(p) + 1 \le m$. $\square$

**Theorem 3 (bands).** For $k \ge 0$ let $\mathrm{BAND}(k)$ be the set of multisets $\{\mu'(p) + \varepsilon_p : p \in V(\mathcal A')\}$
(entries $\ge 3$ kept) over all realizable types of $k$ lines and all $0/1$-assignments $\varepsilon$, and $N(k) = |\mathrm{BAND}(k)|$.
1. For every $n$, a type with largest entry $m = n - k$ is realizable only if the rest of the type lies in $\mathrm{BAND}(k)$.
2. If $n \ge 2$ and $m = n - k \ge \max(\binom k2, k + 1)$, every element of $\mathrm{BAND}(k)$, prefixed with $m$, is
   realizable; hence the number of realizable types of $n$ lines with largest pencil exactly $n - k$ equals $N(k)$,
   independently of $n$. For $k \ge 4$ the condition is $n \ge k + \binom k2$; for $k = 2, 3$ it is $n \ge 2k + 1$, and it
   cannot be weakened there: at $n = 6$, $k = 3$ only $4 = N(3) - 1$ types occur, because $\{4\} \in \mathrm{BAND}(3)$
   would raise the largest pencil above $m = 3$.

*Proof.* (1) is Lemma 1. (2): $|S| \le f_0(\mathcal A') \le \binom k2 \le m$ and $\mu'(p) + 1 \le k + 1 \le m$, so Lemma 2
applies. $\square$

$N(k)$ for $k = 0, \dots, 8$: $1, 1, 2, 5, 12, 30, 74, 176, 401$ (`python scripts/bands.py --table 8`; computed from the
certified types of $k$ lines, so these values are exact for $k \le 12$ and lower bounds beyond). The data for
$n = 11, 12, 13$ agree with the theorem in its range of validity ($k \le 4$) and, as it happens, also for $k = 5$ at
$n = 11, 12$.

**Remarks.** (a) The same statements hold for combinatorially possible types with "linear space" in place of
"arrangement" (the construction adds a point $P$ to the linear space with blocks $\{P\} \cup$ class for each pencil
line). (b) Lemma 1 for $f_0$ with $\mathcal A'$ in general position gives the bands of Salamon–Erdős,
$1 + km + \binom k2 - 2|S|$, and the other types of $\mathcal A'$ fill in the odd values, which is their Lemma 2; the
lower ends of the bands, where several absorbed points share a pencil line (the "crosshatched" extra values of their
Figure 5), are exactly the dissections with $P$ collinear with intersection points of $\mathcal A'$.

## Consequences for $c(n)$

Theorem 3 gives the exact number of realizable types with a pencil of size $\ge n - 4$ for all $n \ge 10$:
$1 + 1 + 2 + 5 + 12 = 21$; with size $\ge n-5$ for $n \ge 15$: $51$; etc. Summing the stable bands,
$$ c(n) \;\ge\; \sum_{k \,:\, n - k \ge \max(\binom k2,\, k+1)} N(k), $$
and the lower bound $\log N(k) \gtrsim$ … is of the same order as the trivial bound. More importantly, part (1) is a
**necessary condition for realizability** that is independent of the three sieves and very effective in practice:
at $n = 13$ it excludes 28 types that survive the arithmetic, combinatorial and inequality sieves (41 before more of
the combinatorial searches finished)
(`data/exclusions.json`, kind `theorem`, reference this note), and the construction of Lemma 2 produced the missing
certificates $\{8, 6\}$, $\{7^2\}$, $\{7, 4^4, 3^3\}$ (`scripts/bands.py 13`).

## Consequences for $V(n)$ (numbers of intersection points)

By Lemma 1, $V(n) = \bigcup_{k} B_k(n)$ with
$B_k(n) = \{\,1 + k(n-k) + f_0(\mathcal A') - \sum_{p \in S}\mu'(p)\,\}$ over realizations $\mathcal A'$ of $k$ lines and
admissible $S$. Lemma 2 gives the *generic part* of each band (every $S$ with $|S| \le m$). For $n = 14, 15, 16, 17$ the
generic parts over all $k \le 13$ contain $62, 73, 83, 92$ values; the extension of 13-line certificates by a line through
several existing points (`scripts/extend.py`) adds $29, 30, 34$ for $n = 14$. Combined with the exclusions (Theorem 1 of
`notes/points.md`, de Bruijn–Erdős, Elliott, and the bounds for $m \le n-3$):

| $n$ | attained (certified) | undecided values | $d(n)$ |
|---|---|---|---|
| 14 | 65 | 27, 28 | 65 or 66 or 67 |
| 15 | $\ge 73$ | 29–33, 37 (not yet attempted by extension) | 73 … 79 |
| 16 | $\ge 83$ | 32–36, 40, 42, 120 | 83 … 91 |
| 17 | $\ge 92$ | 36–39, 43, 45, 128–136 even | 92 … 103 |

The undecided values at the low end are of two kinds: $2n-1$ and $2n$ (which the LP bound with Hirzebruch's inequality
just fails to exclude) and the next few, which would need an arrangement with largest pencil $5$ to $7$ and a very dense
set of absorbed points. Deciding them requires either a sharper inequality or a complete search over the dense
13-line types that are still open.
