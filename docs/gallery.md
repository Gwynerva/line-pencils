---
description: "Interactive drawings of every known way 1 to 14 lines can meet: symmetric drawings where we found them, and the exact certified arrangements. Click a point to see which lines pass through it."
---

# Gallery

Every pencil type that is known to be realizable, for 1 to 14 lines. Choose the style (Beautiful or Exact, explained
below the gallery) and the number of lines; click a drawing to enlarge it, see the exact coefficients of its
certificate, and point at an intersection to light up the lines through it.

Points on more lines are drawn larger. Within each drawing the shade also grows with the number of lines, from the
lightest to the darkest blue present; the enlarged view lists what each shade means.

<div id="lp-gallery"><p>Loading the drawings…</p></div>

**Beautiful** (the default) shows, where we found one, a symmetric drawing of the type: whole orbits of a symmetric
set of lines, taken from regular polygons and their star polygons, from the planes perpendicular to the symmetry axes
of the icosahedron and the octahedron, and from plane sections of the mirrors of 4-dimensional root systems
(`scripts/symmetric_drawings.py`). No two lines are parallel, as the problem requires. Such a drawing is a
floating-point realization of the same type, checked with the same tolerance as the exact drawing; the arrangement
of the certificate need not be a projective image of it. Types without a symmetric drawing are shown exactly.

**Exact** shows the certified arrangement: a projective image of the certified coordinates, chosen so that all
intersection points are visible and well separated; the incidences are exactly those of the certificate. A field such as ℚ(√5) next to a type means
that the certificate uses that square root; the field is the one in which the example was found, and only for the
pentagram {5, 3<sup>10</sup>, 2<sup>5</sup>} is the irrationality known to be necessary. For n = 13 the list is a lower bound: 39 types are
still undecided ([open problems](open.md)); for n = 14 only the types found so far are shown.
