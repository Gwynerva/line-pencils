---
description: "Interactive drawings of the project's certified pencil types for 1 to 14 lines, with symmetric views where available. Hover over (or tap) an intersection point to see which lines pass through it."
---

# Gallery

The gallery shows the pencil types with certificates in this project, for 1 to 14 lines. Choose the number of
lines to see one card per type. Open a card to see the exact coefficients and switch between **Symmetric** and
**Exact** where both views are available. Hover over or tap a point to highlight the lines through it.

Points on more lines are drawn larger. Within each drawing the shade also grows with the number of lines, from the
lightest to the darkest blue present; the enlarged view lists what each shade means.

The drawings are grouped by their number of intersection points $f_0$. Through 13 lines, the groups cover all
[$d(n)$ possible counts](sequences/points.md). For 14 lines, the gallery shows 65 attained counts. Whether 28
points are possible remains open. The labels between groups explain the gaps.

<div id="lp-gallery"><p>Loading the drawings…</p></div>

**Symmetric** shows a drawing of the type with symmetry, where available. The drawings use whole orbits of a symmetric
set of lines, taken from regular polygons and their star polygons, from the planes perpendicular to the symmetry axes
of the icosahedron and the octahedron, and from plane sections of the mirrors of 4-dimensional root systems
(`scripts/symmetric_drawings.py`). No two lines are parallel, as the problem requires. Such a drawing is a
floating-point realization of the same type: its incidences are recomputed numerically, with the tolerance used for
all drawings. The certified arrangement need not be a projective image of it. Types without a symmetric drawing have
only the Exact view.

**Exact** displays the certificate's coefficients and draws a projective image chosen to make the intersection
points visible and well separated. The verifier checks the coefficients with exact arithmetic. The screen
drawing uses numerical coordinates. A label such as ℚ(√5) identifies the field used by that certificate.
The project proves that the pentagram type {5, 3<sup>10</sup>, 2<sup>5</sup>} requires irrational coordinates.
The gallery is complete through 12 lines. For 13 lines, [39 types remain undecided](open.md#2-thirteen-lines).
