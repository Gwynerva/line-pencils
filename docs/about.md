# About

**How n Lines Can Meet** is an open mathematical notebook. It grew out of a school-level question —
*n lines, no two parallel: how many lines can meet at each point?* — and the discovery that three of the natural
integer sequences it produces were absent from the OEIS.

## Who did what

The questions were posed by Petra Radko (GitHub: Gwynerva), who also fixed the scope of the project and the
standards of rigour (exact certificates, a single verifier, every claim labelled). **All of the work itself — the
mathematics (theorems, proofs, conjectures), the programs, the computations, the figures and the text of this site —
was carried out by Claude Code (Anthropic's Claude models)**, with the author's original exploratory scripts and data
as the starting point. Errors are therefore Claude's; the reader is invited to re-run the verifier and the proofs.

## How to cite

> Petra Radko, *How n Lines Can Meet: pencil types of line arrangements and the integer sequences they generate*, 2026.
> https://gwynerva.github.io/line-pencils/ — code and data: https://github.com/Gwynerva/line-pencils

BibTeX:

```bibtex
@misc{gwynerva2026lines,
  author = {Petra Radko},
  title  = {How n Lines Can Meet: pencil types of line arrangements and the integer sequences they generate},
  year   = {2026},
  howpublished = {\url{https://gwynerva.github.io/line-pencils/}},
  note   = {Code and data: \url{https://github.com/Gwynerva/line-pencils}}
}
```

## Licence

Text, figures and data on this site and in the repository (`docs/`, `data/`, `notes/`): [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/).
Code (`verifier/`, `engine/`, `scripts/`): MIT.

## Reproducibility

Everything stated here is either proved on the site, cited with full references, or computed by code in the
repository with logs and exact certificates. The verifier runs automatically on every change of the repository.
Corrections and questions are welcome as issues on GitHub.

## Acknowledgements

Computations used python-sat with CaDiCaL, NumPy, SciPy, SymPy, NetworkX and GCC. The site is built with Zensical;
formulas are rendered by MathJax. The literature was checked against the original papers where
they are available online (Kelly–Moser 1958, Erdős 1972, Salamon–Erdős 1988, Elliott 1967, Hirzebruch 1983, Green–Tao 2013).
