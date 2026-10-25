---
description: "All known terms of the four sequences about how n lines can meet, with the evidence behind each term and the terms that are still open."
---

# The four sequences

All known terms of the four sequences, with the evidence behind each. Intervals mark terms that are not yet known
exactly. All sequences are indexed by the number of lines $n \ge 1$. Labels: <span class="status-proved">proved</span>,
<span class="status-computed">computer-verified</span>, <span class="status-bound">bound</span>.

--8<-- "sequences.md"

How each column is established:

* **$a(n)$** is a count of partitions and is <span class="status-proved">proved</span> for every $n$ by the identity with
  A072964 ([details](arithmetic.md)).
* **$b(n)$** is <span class="status-computed">computer-verified</span>: an exhaustive search over linear spaces decides every
  admissible type, with no time-outs, and a SAT solver re-derives the same answers ([details](combinatorial.md)).
* **$c(n)$** for $n \le 11$ is <span class="status-computed">computer-verified</span>: every realizable type has an exact
  certificate checked by the verifier, every other type is excluded by a theorem or by the exhaustive orientability
  search. For $n = 12$: 335 certificates and 2 undecided types ([details](realizable.md)); for $n = 13$: 600
  certificates and 59 undecided types.
* **$d(n)$** combines certificates (a value is attained) with theorems (a value is impossible); for $n \le 13$ every value
  is decided ([details](points.md)). The term $d(12) = 46$ uses the non-realizability of the three types with
  $21$ points: $\{4^9\}$ by a theorem, $\{5^2, 4^3, 3^6\}$ and $\{5^3, 3^9\}$ by the orientability search.

## What is not in the OEIS

The arithmetic sequence is A072964 shifted. The other three were searched for in the OEIS (full
sequences, subsequences of five consecutive terms, shifts): no entry matches. Two entries coincide with ours on a few
terms by accident and must not be confused with them: A129230 ($0, 1, 3, 5, 9, 13, 18, 24, 30, 38, 46, 55, \dots$, a
golden-ratio floor sum) agrees with $d(n)$ for $n \le 12$ and differs at $n = 13$ ($55 \ne 56$); A005834
($0, 2, 2, 5, 8, 16, 28, 53, 98, 183, \dots$) contains $16, 28, 53, 98$ and then $183 \ne 180$.
