# Literature follow-up: Hirzebruch's inequality, Salamon–Erdős 1988 details, Elliott 1967

Legend: **[P]** verified from the primary source (text layer / page image of the actual paper); **[R]** reliable secondary (peer-reviewed survey, Crossref/OpenAlex); **[S]** other secondary; **[U]** unverified.

---

## 1. Hirzebruch's inequality (1983)

**Primary source [P]:** F. Hirzebruch, "Arrangements of lines and algebraic surfaces", in: *Arithmetic and Geometry, Vol. II* (M. Artin, J. Tate, eds.; dedicated to I. R. Shafarevich), Progress in Mathematics 36, Birkhäuser, Boston 1983, pp. 113–140. DOI 10.1007/978-1-4757-9286-7_7. MR 717609, Zbl 0527.14033. Open PDF: https://hirzebruch.mpim-bonn.mpg.de/id/eprint/244/1/hirzebrucharr.pdf (I read pp. 131–133 and 140 from this PDF).

Notation (Hirzebruch): k = number of lines, t_r = number of points lying on exactly r lines, f_0 = Σ t_r, f_1 = Σ r t_r. Everything is in the **complex projective plane**; since R ⊂ C every statement applies verbatim to real arrangements.

### (a) The weak inequality t_2 + t_3 ≥ k + Σ_{r≥5}(r−4) t_r

Exact statement, §3.1, p. 132 **[P]** (verbatim):

> **Theorem.** For an arrangement of k lines in the complex projective plane we consider the associated quadratic polynomial F(x). If t_k = t_{k−1} = t_{k−2} = 0, then F(x) ≥ 0 for all integers x. If t_k = t_{k−1} = 0, then F(x) ≥ 0 for all integers x ≠ 1; in particular F(2) ≥ 0 which means
>
> (3)  t_2 + t_3 ≥ k + t_5 + 2t_6 + 3t_7 + ⋯ .

where (2) F(x) = x²(f_0 − k) − 2x(f_1 − 2f_0) + 4(f_0 − t_2) (p. 132). So **the hypothesis for (3) is t_k = t_{k−1} = 0 only.** Hirzebruch adds (p. 133): "The inequality (3) shows for example that arrangements of k lines with t_2 = t_3 = t_k = 0 are impossible in the complex projective plane."

On the restriction k ≥ 6: the underlying theorems in §2.4–2.5 are stated for k ≥ 6 ("Theorem. For an arrangement with k ≥ 6 and t_k = t_{k−1} = 0, the surface Y has canonical dimension ≥ 0 for n ≥ 3. For an arrangement with k ≥ 6 and t_k = t_{k−1} = t_{k−2} = 0 the canonical dimension is ≥ 0 for n ≥ 2." — p. 131), and "We leave it to the reader to investigate the surfaces for k = 4, 5 (t_k = t_{k−1} = 0). The surface Y is rational, or of canonical dimension ≥ 0." (p. 131), which is why the Miyaoka–Yau inequality, and hence (3), still holds for k = 4, 5. The theorem in §3.1 itself carries no explicit lower bound on k. Pokora's survey states it both ways: Theorem 5 "arrangement of d ≥ 4 lines such that t_d = t_{d−1} = 0" and Theorem 8 "d ≥ 6 lines such that t_d = t_{d−1} = 0", with Remark 16: "every configuration of d ∈ {4, 5} lines with t_d = t_{d−1} = 0 also satisfies Hirzebruch's inequality (3), therefore the formulation of Theorem 5 is in fact equivalent to that of Theorem 8" **[R]**. (For d ≤ 3 with t_d = t_{d−1} = 0 there is nothing to prove / no such arrangement.)

The t_k = t_{k−1} = t_{k−2} = 0 hypothesis gives more: F(x) ≥ 0 for **all** integers x, in particular F(1) ≥ 0 (Hirzebruch's H_L(2) ≥ 0 in Pokora's normalisation), which reads **[R, Pokora Remark 13]**: for d ≥ 6, t_d = t_{d−1} = t_{d−2} = 0:
 t_2 + 3t_3 + t_4 ≥ d + Σ_{r≥5}(2r − 9) t_r.
Also from F(4) ≥ 0 (Pokora Remark 12): 4t_2 + 3t_3 + t_4 ≥ 4d + Σ_{r≥5}(2r−9)t_r — hmm, Pokora writes this for "n = 5" of his H_L; equality exactly for A_1(6) over R and the dual Hesse over C.

### (b) The "3/4" inequality

**Hirzebruch's own version, p. 140, "Remarks added in proof", item 2) [P]** (verbatim):

> 2) The inequality (3) in 3.1 can be improved by using results of F. Sakai (Semi-Stable Curves on Algebraic Surfaces and Logarithmic Pluricanonical Maps, Math. Ann 254, p. 89–120 (1980)). We have
>
>   t_2 + (3/4) t_3 ≥ k + t_5 + 2t_6 + 3t_7 + ⋯
>
> This is sharp for A_1(6), A_1(9), A_3^0(3), A_3^0(4) and the arrangements with S–T numbers 24 and 25.

No hypothesis is restated in the remark; it refers to "(3) in 3.1", whose hypothesis is t_k = t_{k−1} = 0. Note the right-hand side here has coefficients (r − 4), the same as in (3). (A_1(6): 6 lines, t_2 = 3, t_3 = 4: 3 + 3 = 6 ✓; A_3^0(3) = dual Hesse, 9 lines, t_3 = 12: 9 = 9 ✓; S–T 25 = Hesse 12 lines t_2 = 12, t_4 = 9: 12 = 12 ✓ — consistent with the (r−4) right-hand side, where t_4 has coefficient 0.)

**The version "usually found in the literature" has a different (stronger) right-hand side and a stronger hypothesis** — Pokora, Remark 14 **[R]** (verbatim):

> Remark 14. In the literature, we can find usually the following variant of Hirzebruch's inequality
>
> (5)  t_2 + (3/4) t_3 ≥ d + Σ_{r≥5}(2r − 9) t_r
>
> provided that d ≥ 6 and t_d = t_{d−1} = t_{d−2} = 0. In order to justify this claim, one needs to use Miyaoka–Sakai's improvement [27, 35, 39] of the Bogomolov–Miyaoka–Yau inequality …

Same form in Basit–Dvir–Saraf–Wolf **[P, arXiv text]**: "Theorem 1.7 (Hirzebruch's inequality [Hir83]). Let V be a set of n points in C², such that t_n(V) = t_{n−1}(V) = t_{n−2}(V) = 0. Then t_2(V) + (3/4)t_3(V) ≥ n + Σ_{r≥5}(2r − 9)t_r(V)." (dual formulation, points instead of lines) — F. Basit, Z. Dvir, S. Saraf, C. Wolf, "On the number of ordinary lines determined by sets in complex space", arXiv:1611.08740 (Discrete Comput. Geom. 61 (2019) 778–808 [U for journal data]). And in de Zeeuw **[P, arXiv text]**: "For a point set P in C² (or in R²) with at most n − 3 points collinear, Hirzebruch's inequality [13] states that t_2 + (3/4)t_3 ≥ n + Σ_{i≥5}(2i − 9)t_i. (4)" — F. de Zeeuw, "Spanned lines and Langer's inequality", arXiv:1802.08015 (2018). Pokora's Remark 15 says that *Research Problems in Discrete Geometry* (Brass–Moser–Pach 2005, p. 315, Problem 7) and Erdős–Purdy's Handbook chapter §4.1.1 state (5) and ask for an elementary proof over R.

**Summary of "which hypothesis goes with which":**
| inequality | hypothesis | source |
|---|---|---|
| t_2 + t_3 ≥ k + Σ_{r≥5}(r−4)t_r | t_k = t_{k−1} = 0 (k ≥ 4; k ≥ 6 in the derivation, k = 4, 5 trivial) | Hirzebruch (3), p. 132 [P]; Pokora Thm 5/8 [R] |
| t_2 + (3/4)t_3 ≥ k + Σ_{r≥5}(r−4)t_r | not restated; context = hypothesis of (3), i.e. t_k = t_{k−1} = 0 | Hirzebruch p. 140, remark added in proof [P] |
| t_2 + (3/4)t_3 ≥ d + Σ_{r≥5}(2r−9)t_r | d ≥ 6 and t_d = t_{d−1} = t_{d−2} = 0 | Pokora Remark 14 [R]; BDSW Thm 1.7, de Zeeuw (4) [P]; Brass–Moser–Pach p. 315 [S] |
| t_2 + 3t_3 + t_4 ≥ d + Σ_{r≥5}(2r−9)t_r | d ≥ 6, t_d = t_{d−1} = t_{d−2} = 0 | Pokora Remark 13 [R] (= Hirzebruch's F(1) ≥ 0) |
| t_2 + (3/4)t_3 ≥ d + Σ_{r≥5}(r²/4 − r)t_r | d ≥ 6 and t_r = 0 for r > 2d/3 | Bojanowski 2003 (Master thesis, Polish); Pokora Thm 19 [R] |

So the coordinator's formulation (b) "if t_n = t_{n−1} = t_{n−2} = 0 then t_2 + (3/4)t_3 ≥ n + Σ(k−4)t_k" is **correct but not the sharpest standard form**: under that hypothesis the literature gives the stronger coefficients (2r − 9) ≥ (r − 4) for r ≥ 5. Whether Hirzebruch's (r−4)-version of the 3/4-inequality really needs only t_k = t_{k−1} = 0 is not spelled out in the primary source (the remark gives no proof); all later authors state the 3/4-inequality with t_{d−2} = 0 as well. Safest citation for a real arrangement of n lines, no n−2 concurrent: t_2 + (3/4)t_3 ≥ n + Σ_{r≥5}(2r−9)t_r (Hirzebruch 1983 + Sakai; see Pokora 2021, Remark 14).

All of these are theorems about **complex** arrangements (Hirzebruch: "arrangement of k lines in the complex projective plane"; Pokora: L ⊂ P²_C, "we will use the natural inclusion R ⊂ C"), so they apply to real arrangements and, dually, to real point sets. They do **not** hold for pseudoline arrangements in general (Pokora Theorem 40 quotes Shnurnikov's weaker pseudoline inequality t_2 + (3/2)t_3 ≥ 8 + Σ_{r≥4}(2r − 7.5)t_r for d ≥ 5, t_d = … = t_{d−3} = 0; Bokowski–Pokora use only Melchior for pseudolines).

**Secondary sources (full citations):**
- P. Pokora, "Hirzebruch-type inequalities viewed as tools in combinatorics", *Electron. J. Combin.* 28 (1) (2021), #P1.9. https://www.combinatorics.org/ojs/index.php/eljc/article/view/v28i1p9 [R; page images of pp. 3, 8, 9 read].
- P. Pokora, "Hirzebruch-type inequalities and plane curve configurations", arXiv:1610.05019 (2016/17), journal DOI 10.1007/s00454-015-9744-4 listed in its metadata [U which journal] — concerns d-configurations of curves; it quotes Hirzebruch [5] only in general form.
- R. Bojanowski, *Zastosowania uogólnionej nierówności Bogomolova–Miyaoka–Yau*, Master thesis (in Polish), Univ. Warsaw 2003, http://www.mimuw.edu.pl/~alan/postscript/bojanowski.ps [S; cited by Pokora as [7]; Theorems 2.2, 2.3 there].
- J. Bokowski, P. Pokora, "On the Sylvester–Gallai and the orchard problem for pseudoline arrangements", *Period. Math. Hungar.* 77 (2) (2018), 164–174, DOI 10.1007/s10998-017-0224-x; arXiv:1607.05864 [P: text does not state Hirzebruch's inequality; uses Melchior for pseudolines].
- F. de Zeeuw, "Ordinary lines in space", arXiv:1803.09524 — does not state Hirzebruch's inequality (uses Beck + Langer); the statement is in de Zeeuw, "Spanned lines and Langer's inequality", arXiv:1802.08015, eq. (4) [P].
- A. Langer, "Logarithmic orbifold Euler numbers of surfaces with applications", *Proc. London Math. Soc.* 86 (2003) 358–396, Prop. 11.3.1 [S] — source of Bojanowski/Langer inequalities: Σ_{r≥2} r² t_r ≥ ⌈4d²/3⌉ and Σ_{r≥2} r t_r ≥ ⌈d²/3 + d⌉ when t_r = 0 for r > 2d/3 (Pokora Thm 20) [R].

---

## 2. Salamon–Erdős 1988 — details

Source [P]: P. Salamon, P. Erdős, "The solution to a problem of Grünbaum", *Canad. Math. Bull.* 31 (2) (1988) 129–138, DOI 10.4153/CMB-1988-020-2. (Text layer of the Cambridge PDF + page scans of the Rényi copy, https://static.renyi.hu/~p_erdos/1988-36.pdf.)

Setting: P_n = n points in the plane; m = number of connecting lines; the **k-th band** = configurations in which the largest number of collinear points is exactly n − k (0 ≤ k ≤ n − 2). P_{n−k} = points on the "large line", P_k = the rest.

### (a) Band formulas and which values are attained

- Lemma 1 (p. 131) [P]: "For all 0 ≤ k ≤ n − 2, the maximum number of lines in the k-th band is M_max(k) = k(n − k) + C(k,2) + 1. The minimum number of lines is bounded below by M_min(k) = k(n − k) − C(k,2) + 1." (Lower bound = Kelly–Moser's tie-line count: "There are k(n − k) (possibly coincident) tie lines… if a, b ∈ P_k, then they share at most one tie line. Thus there are at least k(n−k) − C(k,2) distinct tie lines and thus at least k(n−k) − C(k,2) + 1 connecting lines, counting the large line." Valid for k = 0, 1 with C(0,2) = C(1,2) = 0.) Note M_min(k) = kn − ½(3k+2)(k−1) (Kelly–Moser's form) and M_max(k) − M_min(k) = 2·C(k,2) = k(k−1).
- Lemma 2 (p. 132) [P]: "All values in the k-th band, for n ≥ k(k + 1)/2, between the largest m value M_max(k) and the smallest m value M_min(k) are realized except for M_max − 1 and M_max − 3." Proof: slide points of P_{n−k} onto the C(k,2) lines of P_k (each move −2) → all M_max − 2j, j = 0..C(k,2); starting from M_max − 2 (three points of P_k collinear) moves give −2 or −3 → all values (M_max − 2) − 2j and (M_max − 2) − 2j − 3, j = 1, …, C(k,2) − 3; "Except for M_max − 3, all integers between M_min + 1 and M_max − 2 are of this form." (Condition n ≥ k(k+1)/2 ⇔ C(k,2) ≤ n − k, i.e. enough points on the big line.)
- Lemma 3 (p. 132–133) [P]: "For n ≤ k(k + 1)/2 and k ≤ n − 3 all values in the interval between M_max(k) and M_max(k) − 2(n − k) are taken on except M_max − 1 and M_max − 3." (For k = n − 2 only the single value M_max(n−2) = C(n,2); for k = n − 3 only values M_max(n−3) − 2j.) Overlap of consecutive bands: "M_max(k) − 3 ≤ M_max(k+1) − 2(n − k) for all k < n − 2" in that range.
- Lemma 4 (p. 133) [P]: "For n sufficiently large, any configuration in a band with k > [√n + 2] has more than M_max([√n + 2] − 1) lines." (Kelly–Moser's M_min(k) is increasing up to k = [(n + 0.5)/3]; beyond n/3 use Beck's theorem.)
- Count of values in a band (p. 134) [P]: "We first note that for k ≥ 3, the number of values in a band is 2·C(k,2) − 1. Summing these from 3 to j and adding 4 for the first three bands we find that there are h(j) = 4 + j(j + 2)(j − 2)/3 values in the first j + 1 bands for j ≥ 2." (Band k: k(k−1) + 1 integers from M_min to M_max minus the two gaps = k(k−1) − 1 = 2C(k,2) − 1 values, for k ≥ 3; bands 0, 1, 2 contribute 1 + 1 + 2 = 4 values: {1}, {n}, {2n−4, 2n−2}.) Check: h(2) = 4, h(3) = 9, h(4) = 20, h(5) = 39.
- Structure (p. 133–134) [P]: "The structure is thus a sequence of non-overlapping bands until k = [√n + 2] at which time a transition occurs to a continuum of values which persist until C(n,2) − 4. The remaining two values at the top are C(n,2) − 2 and C(n,2)." Five cases according to f(n) = [√n + 2]² − n ∈ {2, 1, 0, −1, < −1}; last gap before the continuum (p. 134): Cases 1&2: continuum = {m : M_max([√n+2] − 1) − 3 < m < C(n,2) − 3}; Cases 3&4: {m : M_max([√n+2] − 1) − 1 < m < C(n,2) − 3}; Case 5: {m : M_min([√n+2]) − 1 < m < C(n,2) − 3}. "From these expressions we obtain the best value of c = 1 in the cn^{3/2} bound to the bottom of the continuum proved by Erdős [5]."

### (b) m_4 = 2n − 2

p. 134 [P], displayed without any stated condition on n:
 m_1^{(n)} = 1, m_2^{(n)} = n, m_3^{(n)} = 2n − 4, m_4^{(n)} = 2n − 2.
followed by "For i > 4, we determine a j such that i is between h(j) and h(j + 1). Provided the resulting j is less than [√n + 2] − 1, we use (1a) m_i^{(n)} = M_max(j) + i − h(j) − 2 for h(j − 1) < i ≤ h(j) − 2; (1b) m_i^{(n)} = M_max(j) − 2 for i = h(j) − 1; (1c) m_i^{(n)} = M_max(j) for i = h(j). For larger j, we again have to distinguish between the five cases." The whole list is under the paper's blanket assumption "for large n" ("These formulas allow us to construct tables of m values for sufficiently large values of n", p. 136; "a complete answer to Grünbaum's problem for n ≥ n*", p. 137). The paper nowhere gives an explicit n for which m_4 = 2n − 2 is proven; the band-2 values {2n−4, 2n−2} = {M_min(2), M_max(2)} are attained for every n ≥ 4 (trivially), and m_3 = 2n − 4 as the *third smallest* value needs Elliott's n ≥ 10 (see §3), m_4 = 2n − 2 as the *fourth* needs in addition M_min(3) = 3n − 8 > 2n − 2, i.e. n > 6, plus the absence of stray values from high-k bands below 2n − 2 — which for small n is exactly the unresolved part (see Figure 5: for n = 7, 8 the hatched "extra" values sit immediately above the dots at 2n−4/2n−2). The paper does not state a threshold.

### (c) Figure 5 (p. 137): possible values of m for n ≤ 12

The figure is a dot/strip plot on an m-axis (0 to ~70, ticks every 10), one row per n = 3, …, 12; no numbers are printed on the rows, so the exact integers are **not legible** from the scan (resolution ≈ 9–10 px per unit of m). What is legible is the structure, which I describe row by row (positions estimated from the scan, with my own combinatorial sanity check where possible):

- n = 3: two isolated dots (m = 1, 3).
- n = 4: three dots (m = 1, 4, 6).
- n = 5: dot (1), a short solid bar (two adjacent values, 5–6), two dots (8, 10).
- n = 6: dot (1), dot (6), solid bar (≈ 7–11), two dots (≈ 13, 15). [Hand check: 6 points give 1, 6, 7, 8, 9, 10, 11, 13, 15; 12 and 14 impossible.]
- n = 7: dot (1), dot (7), a cross-hatched block (one or two "extra" values just below the continuum, ≈ 8–9), solid continuum bar up to ≈ 17, then two dots (19, 21).
- n = 8: dot (1), dot (8), hatched block (≈ 11–12), continuum to ≈ 24, dots (26, 28).
- n = 9: dot (1), dot (9), small dots at ≈ 14 and 16 (band 2: 2n−4, 2n−2) immediately followed by two hatched blocks (≈ 17–19), continuum to ≈ 32, dots (34, 36).
- n = 10: dot (1), dot (10), dots ≈ 16, 18, hatched block ≈ 21–22, continuum to ≈ 41, dots (43, 45).
- n = 11: dot (1), dot (11), dots ≈ 18, 20, two hatched blocks ≈ 24–27, continuum to ≈ 51, dots (53, 55).
- n = 12: dot (1), dot (12), dots ≈ 20, 22, hatched block ≈ 28–30 (wider), continuum to ≈ 62, dots (64, 66).

Caption [P]: "Figure 5 – Possible values of m for n ≤ 12. Values predicted from formulas for large n are shown as before; 'extra' values from low end of high k bands are shown crosshatched and elongated." Text (p. 137): "Figure 5 shows an enlargement of the upper corner of figure 4 showing the values of m for n ≤ 12. The values predicted from the above formulas for large n are shown as before, the 'extra' values resulting from the low end of high k bands are shaded and elongated for emphasis. Note that these values are all at the lower end of the continuum leading down from C(n,2)." So for n ≤ 12 the figure is: {1} ∪ {n} ∪ (band-2 values 2n−4, 2n−2 once they separate, n ≥ 9) ∪ ("extra" values) ∪ (continuum up to C(n,2) − 4) ∪ {C(n,2) − 2, C(n,2)}. The paper does not say whether Figure 5 was produced by exhaustive enumeration or by hand; Figure 1 (n = 22–28) carries the explicit warning "This figure may be omitting some m values from the lower end of high k bands." Exact value sets for n ≤ 12 would have to be recomputed (e.g. from the OEIS arrangement data / our own enumeration).

### (d) n*

No definition beyond "for n ≥ n*" and no numerical bound. p. 137 [P]: "Although the above gives a complete answer to Grünbaum's problem for n ≥ n*, it leaves the problem for n < n* open. This case requires a detailed analysis of the lower end of the high k bands and appears to be difficult. … The size of n* is unknown but it is likely to be small." Lemma 4 is the only place where "n sufficiently large" is used essentially (via Beck's theorem with its unspecified constant), so n* is in principle computable only in terms of Beck's constant.

### (e) Counts of attainable values

The paper gives the band counts "2·C(k,2) − 1 for k ≥ 3" and the cumulative count h(j) = 4 + j(j+2)(j−2)/3 for the first j + 1 bands (j ≥ 2) [P], but **no total count** of attainable m for any specific n, and no table of counts. (For large n one could assemble the total from h([√n+2] − 1 or −2) plus the length of the continuum C(n,2) − 3 − (bottom of continuum) minus 2 gaps, plus the two top values — the paper does not do this.) The closing paragraph asks instead for the "density of states", i.e. the multiplicities of each value.

Other verified details: Figure 1 (p. 130) shows the spectra for n = 22…28; Figure 4 (p. 136) shows m versus n for m ≤ ~400 with bands k = 0…7 as lines of slope k and width 2C(k,2) − 1; the top gaps M_max(k) − 1 lie on m = kn − k² + C(k,2), "nearly coincide with the tangents m = kn − k² + C(k,2) − 1/8 to the parabola m = C(n,2)". Authors' affiliations: San Diego State Univ.; Hungarian Academy of Sciences. Received March 19, 1986; revised March 4, 1987. References [1]–[8]: Beck 1983; Cordovil 1980; Donald–Elwin–Hager–Salamon 1984; Elliott 1967 (cited with pp. 181–189, a typo for 181–188); Erdős 1972; Grünbaum 1972; Kelly–Moser 1958; Szemerédi–Trotter 1983.

---

## 3. Elliott 1967 — does it contain the 2n − 4 lines theorem? YES.

Source [P]: P. D. T. A. Elliott (Nottingham), "On the number of circles determined by n points", *Acta Math. Acad. Sci. Hungar.* 18 (1–2) (1967), 181–188 ("Presented by P. Erdős"). DOI 10.1007/BF02020972. Read from the digitised volume at the MTA repository: https://real-j.mtak.hu/7414/ (file MTA_ActaMathHung_18.pdf, PDF pages 187–194; text layer present).

Verbatim statements:

- p. 185: "**Theorem 3.** Let S be a set of n points, no n − 1 of which lie on a straight line. Then S determines at least 2n − 4 distinct lines if n ≥ 10."
- p. 185: "**Lemma 4.** Let S determine a line containing exactly n − r points of S. Then S determines at least r(n − r) − ½ r(r − 1) + 1 distinct lines. Proof. This is Lemma 4.1 of [1]." ([1] = Kelly–Moser.)
- p. 185: "We define a δ-configuration to be two ordinary lines with a point of S in common." "**Lemma 5.** If |S| = n ≥ 10, and not all the points of S lie on a straight line, then either S determines a δ-configuration, or t ≥ 2n − 4." (Proof: cases n ≥ 20, n = 18, 16, and "We are left to consider the cases n = 12, 14. We do not carry out the details as they are simpler.")
- p. 186–187: "Proof of Theorem 3. The proof is by induction on all sets S of desired type with |S| = n, and we know from the work of Kelly and Moser that the proposition stated in the enunciation of the theorem holds if n = 10. Assume therefore that we have proved the result for sets of cardinality up to n − 1. …" (induction step: remove a point of a δ-configuration, or apply Lemma 4).
- p. 182 (context, quoting Kelly–Moser): "**Lemma 1.** If at most n − k points of S are collinear and 2n ≥ 3(3k − 2)² + 3k − 1 then t ≥ kn − ½(k − 1)(3k + 2). In the case k = 2 we see that t ≥ 2n − 4 if n ≥ 27, and for such values of n this result is easily seen to be best possible. By modifying their proof in individual cases they could show that if 7 ≤ n ≤ 9, t ≥ 2n − 5, and if n = 10 then t ≥ 2n − 4. They conjectured that this final inequality held if 10 < n < 27. We shall prove this as Theorem 3."
- p. 181 (introduction): "…it was shown that in the above circumstances S determined at least n distinct lines, and later, that if no n − 1 points of S lay on the same line and n was sufficiently large, then S determined at least 2n − 4 straight lines, and so on."

So Salamon–Erdős's attribution ("Elliot [4] proved this for n ≥ 10") is **accurate**: Elliott's Theorem 3 closes the gap 10 < n < 27 left by Kelly–Moser's Corollary 4.1 (n ≥ 27) and their special analyses (n = 7, 8, 9: ≥ 2n − 5, sharp; n = 10: ≥ 16). Result: for every n ≥ 10, n points with no n − 1 collinear determine ≥ 2n − 4 lines, sharp for all n (Kelly–Moser Fig. 4.2); for n = 7, 8, 9 the sharp bound is 2n − 5.

Other content of Elliott's paper worth noting [P]:
- Theorem 1 (p. 182): n points in the Euclidean plane not all on a circle or a line, n > 3, determine at least 2n(n − 1)/63 circles containing exactly three points (ordinary circles). Theorem 2: under the same hypotheses with n > 393, at least C(n−1, 2) distinct circles (this is the statement later found to be slightly wrong — correct bound C(n−1,2) + 1 − ⌊(n−1)/2⌋, Purdy–Smith 2010, Bálint–Bálintová 1994; cf. erdosproblems.com/506). Elliott notes Segre's cube counterexample for n = 8 and guesses the true ordinary-circle count is n²/6 + O(n).
- p. 184: "Conjecture [of Erdős]. There exists a constant c > 0, independent of n, k so that if there are given n points in the plane, no n − k of them on a straight line, then the points determine more than ckn lines." (Later proved by Beck 1983.) Also: if |S| > c_5|T| > c_6 and S not collinear, S generates at least |S| − |T| lines not meeting T; Lemma 3 (p. 185): n > 2 points not all on a line, P ∉ S: at least n − 1 distinct lines not meeting P (and n lines if n ≥ 4 unless n − 1 points are collinear).

---

## Files

- Hirzebruch 1983 PDF and page renders: C:\Users\Gwynerva\.claude\projects\C--Users-Gwynerva-Desktop-intersecting-lines\38efbac2-7057-437a-ba72-9f3296a3eedb\tool-results\webfetch-1792934823433-8874zx.pdf, …\hirz_imgs\p20.png, p21.png, p28.png (pp. 132, 133, 140).
- Pokora EJC survey PDF/text: …\tool-results\webfetch-1792934743787-tgsz39.pdf, pokora_ejc.txt, pok_imgs\p03.png, p08.png, p09.png.
- Salamon–Erdős page scans: …\tool-results\se_imgs\p01.jpg … p10.jpg (pp. 129–138), fig5_zoom.png.
- Elliott 1967: C:\Users\Gwynerva\AppData\Local\Temp\claude\C--Users-Gwynerva-Desktop-intersecting-lines\38efbac2-7057-437a-ba72-9f3296a3eedb\scratchpad\acta18\elliott.txt (text of pp. 181–188) and imgs\p186.png … p193.png; the full volume PDF (198 MB) is in the same folder.
