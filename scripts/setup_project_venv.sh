#!/usr/bin/env bash
# Create an isolated Python venv for INVERT Kernel (Core v2).
# Usage: ./scripts/setup_project_venv.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR=".venv"

if [[ -f "$ROOT/.python-version" ]]; then
  PYVER="$(tr -d '[:space:]' < "$ROOT/.python-version")"
  if command -v "python${PYVER}" >/dev/null 2>&1; then
    PYTHON="python${PYVER}"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
  else
    echo "No python interpreter found" >&2
    exit 1
  fi
else
  PYTHON="${PYTHON:-python3}"
fi

echo "Root:     $ROOT"
echo "Venv:     $VENV_DIR"
echo "Python:   $($PYTHON --version)"

cd "$ROOT"
rm -rf "$VENV_DIR"
"$PYTHON" -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install -U pip wheel setuptools
python -m pip install -e ".[dev]"

echo ""
echo "Done. Activate with:"
echo "  source $ROOT/$VENV_DIR/bin/activate"
