#!/usr/bin/env bash
# One-shot ACM/Zenodo artifact verification (no LLM regeneration).
# Default: read-only checks. Set INVERT_VERIFY_REPLAY=1 to re-run analyze-run (may refresh CSVs).
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/repo_root.sh"

python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
  || { echo "error: Python >= 3.10 required (see README.md)" >&2; exit 1; }

echo "==> Python $(python3 --version)"
echo "==> Repository root: ${INVERT_REPO_ROOT}"

echo "==> invert-core smoke-test"
invert-core smoke-test

echo "==> frozen detector metadata hash check"
bash scripts/verify_detector_hashes.sh

echo "==> pytest"
pytest -q

if [[ "${INVERT_VERIFY_REPLAY:-0}" == "1" ]]; then
  echo "==> INVERT_VERIFY_REPLAY=1: regenerate confirmatory tables (analysis replay)"
  bash scripts/regenerate_confirmatory_tables.sh
else
  echo "==> Skipping analyze-run replay (set INVERT_VERIFY_REPLAY=1 to enable)"
  echo "==> summarize-core-v2 (aggregation only)"
  invert-core summarize-core-v2
  python -c "
from invert_core.audit_eager_lazy_pole_asymmetry import run_eager_lazy_pole_asymmetry_audit
from invert_core.tasks import project_root
r = run_eager_lazy_pole_asymmetry_audit('core_v2_generalization_local_eager_lazy_001', project_root())
print('Pole audit:', r.md_path if r else 'skipped')
"
fi

echo "==> checksum key outputs"
bash scripts/checksum_key_outputs.sh | diff - KEY_OUTPUTS.sha256

echo "==> export paper figures from archived CSVs"
python scripts/export_paper_figures.py

echo ""
echo "Artifact verification passed."
