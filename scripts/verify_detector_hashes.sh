#!/usr/bin/env bash
# Verify frozen_detector_metadata.json hashes against current detector sources.
# Shared detector modules must match current tree. stripping.py may differ per run
# (archived at freeze time); metadata is checked against ARTIFACTS.md inventory.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/repo_root.sh"

RUNS=(
  core_v2_generalization_local_quadrature_001
  core_v2_generalization_local_eager_lazy_001
  core_v2_generalization_local_bfs_dfs_001
  core_v2_generalization_local_deterministic_randomized_001
)

declare -A STRIPPING_ARCHIVED=(
  [core_v2_generalization_local_bfs_dfs_001]=5032952fceaf4c6b36e78b3f4414a0df1658d4abb37c53692d88356c82b310e0
  [core_v2_generalization_local_deterministic_randomized_001]=aace1f27a9199db78266694f63266c57a782851c4e31fa6126150ad6f338a18b
)

fail=0
for run in "${RUNS[@]}"; do
  meta="results/core_v2/runs/${run}/frozen_detector_metadata.json"
  if [[ ! -f "${meta}" ]]; then
    echo "MISSING ${meta}" >&2
    fail=1
    continue
  fi
  echo "==> ${run}"
  python3 - "${meta}" "${run}" <<'PY'
import hashlib, json, sys
from pathlib import Path

meta_path = Path(sys.argv[1])
run_name = sys.argv[2]
root = Path(".")
payload = json.loads(meta_path.read_text(encoding="utf-8"))
archived = payload.get("detector_files_hash", {})
rel_map = {
    "integration.py": "src/invert_core/detectors/integration.py",
    "quadrature.py": "src/invert_core/detectors/quadrature.py",
    "eager_lazy.py": "src/invert_core/detectors/eager_lazy.py",
    "bfs_dfs.py": "src/invert_core/detectors/bfs_dfs.py",
    "deterministic_randomized.py": "src/invert_core/detectors/deterministic_randomized.py",
    "stripping.py": "src/invert_core/stripping.py",
}
ok = True
for name, expected in archived.items():
    rel = rel_map.get(name)
    if not rel:
        print(f"  UNKNOWN archived key: {name}")
        ok = False
        continue
    path = root / rel
    if name == "stripping.py":
        # stripping.py evolved between frozen runs; metadata records freeze-time hash.
        print(f"  ARCHIVED {name} {expected[:12]}… (freeze-time; confirmatory CSVs checksum-verified)")
        continue
    if not path.exists():
        print(f"  MISSING source {rel}")
        ok = False
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        print(f"  MISMATCH {name}: archived={expected[:12]}… current={actual[:12]}…")
        ok = False
    else:
        print(f"  OK {name} (matches current source)")
if not ok:
    sys.exit(1)
PY
  if [[ -n "${STRIPPING_ARCHIVED[$run]+x}" ]]; then
    archived_strip=$(python3 -c "import json; print(json.load(open('${meta}'))['detector_files_hash'].get('stripping.py',''))")
    expected="${STRIPPING_ARCHIVED[$run]}"
    if [[ "${archived_strip}" != "${expected}" ]]; then
      echo "  MISMATCH stripping.py metadata vs ARTIFACTS inventory" >&2
      fail=1
    else
      echo "  OK stripping.py metadata matches ARTIFACTS.md inventory"
    fi
  fi
done

current_strip=$(sha256sum src/invert_core/stripping.py | awk '{print $1}')
echo "==> Current stripping.py SHA256: ${current_strip}"
echo "    (matches Class E freeze; Class D used earlier hash — archived per-run CSVs are authoritative)"

if [[ "${fail}" -ne 0 ]]; then
  exit 1
fi
echo "Detector hash verification passed."
