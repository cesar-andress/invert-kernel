#!/usr/bin/env bash
# Validate that MANIFEST_ZENODO.txt inclusion entries exist and warn about release exclusions.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/repo_root.sh"
cd "${INVERT_REPO_ROOT}"

manifest="MANIFEST_ZENODO.txt"
fail=0

echo "==> Checking MANIFEST inclusions in ${manifest}"
while IFS= read -r line; do
  [[ "${line}" =~ ^\+[[:space:]] ]] || continue
  entry="${line#+ }"
  [[ "${entry}" == *:* ]] && continue   # metadata lines (VERSION:, etc.)
  [[ "${entry}" == *"*"* ]] && continue # globs not expanded here
  [[ "${entry}" == */ ]] && entry="${entry%/}"
  if [[ ! -e "${entry}" ]]; then
    echo "MISSING inclusion: ${entry}" >&2
    fail=1
  fi
done < "${manifest}"

echo "==> Checking common release exclusions (should NOT be uploaded)"
for bad in .git .venv .pytest_cache src/invert.egg-info; do
  if [[ -e "${bad}" ]]; then
    echo "WARN present locally (exclude from Zenodo zip): ${bad}"
  fi
done

if [[ "${fail}" -ne 0 ]]; then
  echo "Manifest validation failed." >&2
  exit 1
fi
echo "Manifest validation passed (static paths only; globs not expanded)."
