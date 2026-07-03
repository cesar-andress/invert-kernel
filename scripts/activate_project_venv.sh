#!/usr/bin/env bash
# Source the INVERT Kernel venv. Usage: source scripts/activate_project_venv.sh
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
  echo "Missing $VENV_DIR — run: $ROOT/scripts/setup_project_venv.sh" >&2
  return 1 2>/dev/null || exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
