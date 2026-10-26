"""Generate the OEIS a-files (supplementary tables) for the three sequences.

usage: python scripts/oeis_afiles.py            -> writes oeis/a399464.txt, oeis/a400149.txt, oeis/a399605.txt

Sources: data/results/classification_n{n}.json (one record per arithmetically admissible type, with
'linear_space' in YES/NO/None and 'verdict' in real / melchior / csima-sawyer / non-orientable / ...).
  A400149 (b): types with linear_space == "YES", n <= 12.
  A399464 (c): types with verdict == "real", n <= 11.
  A399605 (d): numbers of intersection points binomial(n,2) - Sum binomial(k_i,2) + r over the realizable types,
               n <= 13 (for n = 12, 13 the undecided types do not add new values; this is checked against
               data/results/sequences.json and the known terms).
The script fails loudly if a count disagrees with the published terms.
"""
import json, os, sys
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "oeis")

B = [1, 1, 2, 3, 5, 9, 17, 29, 56, 106, 202, 384]
C = [1, 1, 2, 3, 5, 9, 16, 28, 53, 98, 180]
D = [1, 1, 2, 3, 5, 9, 13, 18, 24, 30, 38, 46, 56]


def rows(n):
    with open(os.path.join(ROOT, "data", "results", "classification_n%d.json" % n)) as f:
        return json.load(f)


def fmt(t):
    """{} / {5, 3^10} notation, sizes in decreasing order."""
    if not t:
        return "{}"
    parts, i, t = [], 0, sorted(t, reverse=True)
    while i < len(t):
        j = i
        while j < len(t) and t[j] == t[i]:
            j += 1
        parts.append(str(t[i]) if j - i == 1 else "%d^%d" % (t[i], j - i))
        i = j
    return "{" + ", ".join(parts) + "}"


def typekey(t):
    return (-len(t), sorted(t, reverse=True))


def points(n, t):
    return comb(n, 2) - sum(comb(k, 2) for k in t) + len(t)


def write(name, header, lines):
    fn = os.path.join(OUT, name)
    with open(fn, "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(header + lines) + "\n")
    print("wrote", fn, len(lines), "lines")


def main():
    note = ["# Notation: {5, 3^10} is the multiset with one 5 and ten 3's; {} is the empty multiset.",
            "# Each line: n: a(n) multisets, in order of decreasing number of parts, then lexicographically.", "#"]
    # A400149
    out = ["# A400149: multisets of sizes of the lines with at least three points of a linear space on n points",
           "# (the ways n lines could meet if the only rule were that two lines meet at most once)."] + note
    for n in range(1, 13):
        ts = [r["type"] for r in rows(n) if n <= 2 or r["linear_space"] == "YES"]
        assert len(ts) == B[n - 1], (n, len(ts), B[n - 1])
        ts.sort(key=typekey)
        out.append("%d: %s" % (n, ", ".join(fmt(t) for t in ts)))
    write("a400149.txt", [], out)
    # A399464
    out = ["# A399464: multisets of the numbers of lines through the intersection points (with at least three lines)",
           "# of n lines in the plane, no two parallel; all a(n) realizable multisets for n <= 11."] + note
    reals = {}
    for n in range(1, 14):
        reals[n] = [r["type"] for r in rows(n) if r["verdict"] == "real"]
    for n in range(1, 12):
        ts = reals[n]
        assert len(ts) == C[n - 1], (n, len(ts), C[n - 1])
        ts.sort(key=typekey)
        out.append("%d: %s" % (n, ", ".join(fmt(t) for t in ts)))
    write("a399464.txt", [], out)
    # A399605
    out = ["# A399605: the numbers of intersection points that n lines in the plane, no two parallel, can have.",
           "# Each line: n: the a(n) attainable values, in increasing order.", "#"]
    for n in range(1, 14):
        vals = sorted({points(n, t) for t in reals[n]})
        if n == 1:
            vals = [0]
        assert len(vals) == D[n - 1], (n, len(vals), D[n - 1], vals)
        out.append("%d: %s" % (n, ", ".join(map(str, vals))))
    write("a399605.txt", [], out)


if __name__ == "__main__":
    main()
