# References

Verified bibliographic data (see `notes/literature_followup.md` for the verification trail). Items marked
with an asterisk were read in the primary source during this project; the others were checked against
publisher or OEIS records.

## Classical theorems used

* **de Bruijn, N. G.; Erdős, P.** On a combinatorial problem. *Indagationes Mathematicae* 10 (1948), 421–423
  (= Proc. Kon. Ned. Akad. Wetensch. 51 (1948), 1277–1279). — $n$ points not all collinear determine at least $n$ lines;
  dually, $n$ lines not all concurrent have at least $n$ intersection points. (Also Hanani 1938, Steinberg; see Erdős 1972.)
* **Melchior, E.** Über Vielseite der projektiven Ebene. *Deutsche Mathematik* 5 (1940/41), 461–475. —
  $t_2 \ge 3 + \sum_{k\ge4}(k-3)t_k$ for every arrangement of real lines that is not a pencil.
* **Kelly, L. M.; Moser, W. O. J.*** On the number of ordinary lines determined by $n$ points. *Canadian Journal of
  Mathematics* 10 (1958), 210–219. DOI 10.4153/CJM-1958-024-6. — $t_2 \ge 3n/7$ (Theorem 3.6); Theorem 4.1: if at most
  $n-k$ points are collinear and $n \ge \frac12\{3(3k-2)^2 + 3k - 1\}$ then at least $kn - \frac12(3k+2)(k-1)$ lines;
  Lemma 4.1 (the "tie line" count, our Lemma 3 in closed form); Corollary 4.1 ($\ge 2n-4$ lines for $n \ge 27$);
  the conjecture $t \ge 2n-4$ for $n > 9$.
* **Elliott, P. D. T. A.*** On the number of circles determined by $n$ points. *Acta Mathematica Academiae Scientiarum
  Hungaricae* 18 (1967), 181–188. DOI 10.1007/BF02020972. — Theorem 3: $n$ points, no $n-1$ collinear, $n \ge 10$,
  determine at least $2n-4$ lines.
* **Csima, J.; Sawyer, E. T.** There exist $6n/13$ ordinary points. *Discrete & Computational Geometry* 9 (1993),
  187–202. DOI 10.1007/BF02189318. — $t_2 \ge 6n/13$ for $n \ne 7$.
* **Hirzebruch, F.*** Arrangements of lines and algebraic surfaces. In: *Arithmetic and Geometry, Vol. II* (M. Artin,
  J. Tate, eds.), Progress in Mathematics 36, Birkhäuser, Boston 1983, pp. 113–140. DOI 10.1007/978-1-4757-9286-7_7.
  — §3.1: $t_2 + t_3 \ge n + \sum_{k\ge5}(k-4)t_k$ when $t_n = t_{n-1} = 0$; remark added in proof: $t_2 + \frac34 t_3 \ge
  n + \sum_{k \ge 5}(k-4)t_k$ (via Sakai). Standard form with $t_n = t_{n-1} = t_{n-2} = 0$ and coefficients $2k-9$:
* **Pokora, P.** Hirzebruch-type inequalities viewed as tools in combinatorics. *Electronic Journal of Combinatorics*
  28 (1) (2021), #P1.9. — survey; Remark 14 states the $\frac34$-inequality with hypothesis $t_n=t_{n-1}=t_{n-2}=0$, $n\ge6$.
* **Green, B.; Tao, T.** On sets defining few ordinary lines. *Discrete & Computational Geometry* 50 (2013), 409–468.
  DOI 10.1007/s00454-013-9518-9; arXiv:1208.4714. — Dirac–Motzkin conjecture and the orchard problem for large $n$.

## Grünbaum's problem (possible numbers of intersection points)

* **Grünbaum, B.** *Arrangements and Spreads.* CBMS Regional Conference Series in Mathematics 10, American Mathematical
  Society, Providence RI, 1972. — notation $t_k$, $f_0$; the orchard problem (p. 22), Sylvester's problem (p. 18).
* **Erdős, P.*** On a problem of Grünbaum. *Canadian Mathematical Bulletin* 15 (1972), 23–25. DOI 10.4153/CMB-1972-005-4.
  — all $m$ with $c_1 n^{3/2} < m \le \binom n2$, $m \ne \binom n2 - 1, \binom n2 - 3$, are numbers of lines determined by
  $n$ points; sharp up to the constant.
* **Salamon, P.; Erdős, P.*** The solution to a problem of Grünbaum. *Canadian Mathematical Bulletin* 31 (1988), 129–138.
  DOI 10.4153/CMB-1988-020-2. — complete description for $n \ge n^*$ (bands $[k(n-k)-\binom k2+1,\ k(n-k)+\binom k2+1]$,
  $m_1 = 1$, $m_2 = n$, $m_3 = 2n-4$, $m_4 = 2n-2$); $n^*$ not determined.
* **Beck, J.** On the lattice property of the plane and some problems of Dirac, Motzkin and Erdős in combinatorial
  geometry. *Combinatorica* 3 (1983), 281–297.
* **Erdős, P.; Purdy, G.** Extremal problems in combinatorial geometry. In: *Handbook of Combinatorics* (Graham,
  Grötschel, Lovász, eds.), Elsevier, Amsterdam 1995, Vol. 1, Ch. 17, pp. 809–874.

## The orchard problem

* **Sylvester, J. J.** Problem 2473. *Mathematical Questions and Solutions from the Educational Times* 8 (1867), 106–107.
* **Burr, S. A.; Grünbaum, B.; Sloane, N. J. A.** The orchard problem. *Geometriae Dedicata* 2 (1974), 397–424.
  DOI 10.1007/BF00147569. — values of the maximal number of triple points for small $n$ (19 for $n=12$), cubic-curve constructions.
* **Füredi, Z.; Palásti, I.** Arrangements of lines with a large number of triangles. *Proceedings of the American
  Mathematical Society* 92 (1984), 561–566. DOI 10.1090/S0002-9939-1984-0760946-2.
* **OEIS A003035**, Maximal number of 3-tree rows in n-tree orchard problem: 0, 0, 1, 1, 2, 4, 6, 7, 10, 12, 16, 19, 22, 26, 31, 37.
  The terms for $n = 13, 14, 15$ are due to Zhao Hui Du (computer search, 2008 and 2026; unpublished).

## Configurations that exist combinatorially but not over the reals

* **Hilbert, D.; Cohn-Vossen, S.** *Geometry and the Imagination.* Chelsea, New York 1952 (German original 1932), Chapter III
  (configurations $(7_3)$, $(8_3)$, $(9_3)$).
* **Gropp, H.** Configurations and their realization. *Discrete Mathematics* 174 (1997), 137–151.
  DOI 10.1016/S0012-365X(96)00327-5. — Möbius–Kantor $(8_3)$ is not realizable over $\mathbb R$.
* **Grünbaum, B.** *Configurations of Points and Lines.* Graduate Studies in Mathematics 103, AMS 2009.
* **Artebani, M.; Dolgachev, I.** The Hesse pencil of plane cubic curves. *L'Enseignement Mathématique* 55 (2009), 235–273.
  — the Hesse configuration $(9_4 12_3)$ lives over $\mathbb Q(\sqrt{-3})$; over $\mathbb R$ it is excluded by Sylvester–Gallai.
* **Coxeter, H. S. M.** A problem of collinear points. *American Mathematical Monthly* 55 (1948), 26–28.

## Oriented matroids

* **Folkman, J.; Lawrence, J.** Oriented matroids. *Journal of Combinatorial Theory, Series B* 25 (1978), 199–236.
  DOI 10.1016/0095-8956(78)90039-4. — topological representation: rank-3 oriented matroids = pseudoline arrangements.
* **Björner, A.; Las Vergnas, M.; Sturmfels, B.; White, N.; Ziegler, G. M.** *Oriented Matroids*, 2nd ed.
  Encyclopedia of Mathematics and its Applications 46, Cambridge University Press 1999. DOI 10.1017/CBO9780511586507.
  — chirotopes and the 3-term Grassmann–Plücker relations (Definition 3.5.3, Theorem 3.6.2).
* **Bokowski, J.; Pokora, P.** On line and pseudoline configurations and ball-quotients. *Periodica Mathematica
  Hungarica* 77 (2018), 164–174. DOI 10.1007/s10998-017-0224-x. — classification of pseudoline arrangements with
  12 lines, 19 triple points and 9 double points.

## Linear spaces (combinatorial sieve)

* **Betten, A.; Betten, D.** Linear spaces with at most 12 points. *Journal of Combinatorial Designs* 7 (1999), 119–145.
* **OEIS A001200**, Number of linear geometries on n (unlabeled) points: 1, 1, 1, 2, 3, 5, 10, 24, 69, 384, 5250, 232929, 28872973.
* **Barakat, M.; Behrends, R.; Jefferson, C.; Kühne, L.; Leuner, M.** On the generation of rank 3 simple matroids with an
  application to Terao's freeness conjecture. *SIAM Journal on Discrete Mathematics* (2021). arXiv:1907.01073.

## OEIS entries related to the sequences of this project

* **A072964** Number of partitions of the $n$-th triangular number into triangular parts: 1, 1, 2, 4, 7, 15, 32, 66, 141, 295, 619, 1286, …
  (our arithmetic sieve $a(n) = $ A072964$(n-1)$).
* **A003034** Sylvester's problem: minimal number of ordinary lines through $n$ points.
* **A048872**, **A132346** non-isomorphic arrangements of $n$ lines in the real projective plane; **A241600** affine arrangements.
* **A129230** and **A005834** — coincide with $d(n)$ resp. $c(n)$ on a few terms only; unrelated definitions.

## Software

* Biere, A. et al., CaDiCaL SAT solver (version 1.9.5), used through **python-sat** (Ignatiev, Morgado, Marques-Silva,
  PySAT: a Python toolkit for prototyping with SAT oracles, SAT 2018).
