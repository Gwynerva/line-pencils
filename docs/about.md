---
description: "Who contributed to this project, how to cite it, the licence, and how the results can be reproduced."
---

# About

**How n Lines Can Meet** is an open mathematical notebook. It grew out of a school-level question —
*n lines, no two parallel: how many lines can meet at each point?* — and the discovery that three of the natural
integer sequences it produces were absent from the OEIS. They are now OEIS entries A400149, A399464 and A399605.

## Who contributed

### People

- **Petra Radko** posed the original question, provided the exploratory scripts and data, and set the verification standards.
- **Mark Kim** computed $b(13)=729$, $b(14)=1357$, and $b(15)=2558$ and published the preprint, code, and classifications.
  [Preprint](https://doi.org/10.5281/zenodo.24567131) · [Code and tables](https://github.com/marik-11/linear_space_types)

### AI agents

- **Claude Code (Anthropic)** developed the project's original proofs, programs, computations, illustrations, and write-up.
- **Codex (OpenAI)** checked Kim's tables against the project data, reproduced all 4,843 decisions for $n=14$,
  checked the consequences for intersection counts, and updated the documentation.

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

The site links to proofs, certificates, computational methods, and published results. GitHub Actions runs the
certificate verifier on pushes and pull requests. See [Data and verification](data.md) for the commands.
Corrections and questions are welcome as issues on GitHub.

## Acknowledgements

Computations used python-sat with CaDiCaL, NumPy, SciPy, SymPy, NetworkX and GCC. The site is built with Zensical;
formulas are rendered by MathJax. The literature was checked against the original papers where
they are available online (Kelly–Moser 1958, Erdős 1972, Salamon–Erdős 1988, Elliott 1967, Hirzebruch 1983, Green–Tao 2013).
