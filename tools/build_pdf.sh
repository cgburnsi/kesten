#!/usr/bin/env sh
set -eu

# Build the canonical LaTeX manuscript via host latexmk from a Flatpak sandbox.
# Usage:
#   tools/build_pdf.sh
#   tools/build_pdf.sh clean
#   tools/build_pdf.sh /path/to/file.tex
#   tools/build_pdf.sh /path/to/file.tex clean

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DEFAULT_TEX="$ROOT_DIR/docs/latex/kesten_1968.tex"

TEX_FILE="$DEFAULT_TEX"
MODE="build"

if [ "$#" -ge 1 ]; then
  case "$1" in
    clean)
      MODE="clean"
      ;;
    *)
      TEX_FILE="$1"
      ;;
  esac
fi

if [ "$#" -ge 2 ]; then
  case "$2" in
    clean)
      MODE="clean"
      ;;
    *)
      echo "Unknown second argument: $2" >&2
      exit 2
      ;;
  esac
fi

if [ ! -f "$TEX_FILE" ]; then
  echo "TeX file not found: $TEX_FILE" >&2
  exit 1
fi

TEX_DIR=$(CDPATH= cd -- "$(dirname -- "$TEX_FILE")" && pwd)
TEX_BASE=$(basename -- "$TEX_FILE")

if [ "$MODE" = "clean" ]; then
  flatpak-spawn --host /bin/sh -lc "cd '$TEX_DIR' && latexmk -C '$TEX_BASE'"
  exit 0
fi

flatpak-spawn --host /bin/sh -lc "cd '$TEX_DIR' && latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error '$TEX_BASE'"
