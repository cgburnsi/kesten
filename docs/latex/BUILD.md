# LaTeX Build

Build the canonical manuscript from the sandbox using host-installed tools.

## Prerequisites
- `pdflatex` installed on host
- `latexmk` installed on host

## Build
From repo root:

```sh
tools/build_pdf.sh
```

Default source:
- `docs/latex/kesten_1968.tex`

Output:
- `docs/latex/kesten_1968.pdf`

## Build a different file
```sh
tools/build_pdf.sh docs/latex/your_file.tex
```

## Clean build artifacts
```sh
tools/build_pdf.sh clean
```

Or for a specific file:

```sh
tools/build_pdf.sh docs/latex/your_file.tex clean
```
