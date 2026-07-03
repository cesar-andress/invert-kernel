#!/usr/bin/env bash
# TOSEM artifact quick path (~2–5 min after editable install; ~10–15 min including first-time setup).
# Read-only with respect to LLM outputs: no Ollama, no API keys, no analyze-run replay.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/repo_root.sh"

python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
  || { echo "error: Python >= 3.10 required (see README.md)" >&2; exit 1; }

echo "==> INVERT Core v2 quick artifact verification"
echo "==> Python $(python3 --version)"
echo "==> Repository root: ${INVERT_REPO_ROOT}"

echo "==> invert-core smoke-test (fixture detectors + oracles)"
invert-core smoke-test

echo "==> frozen detector metadata hash check"
bash scripts/verify_detector_hashes.sh

echo "==> checksum key confirmatory outputs"
bash scripts/checksum_key_outputs.sh | diff - KEY_OUTPUTS.sha256

echo "==> summarize-core-v2 (re-aggregate archived per-run CSVs only)"
invert-core summarize-core-v2

echo ""
echo "Quick artifact verification passed."
echo "For full suite (pytest + pole audit + figure export): bash scripts/verify_artifact.sh"
