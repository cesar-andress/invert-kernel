# ARTIFACT_VERIFY_REPORT — INVERT Kernel replication package

**Date:** 2026-07-03  
**Directory:** `/home/cesar/papers/invert/invert-kernel/invert-kernel`  
**Python:** 3.12.13 (`/usr/bin/python3.12 -m venv .venv`)

## Command

```bash
source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/verify_artifact.sh
```

## Result

| Step | Status | Detail |
|------|--------|--------|
| `invert-core smoke-test` | **PASS** | Integration, lock-control, shuffled-control fixtures |
| `pytest` | **PASS** | 187 tests in `tests/core_v2/` (2.67s) |
| `invert-core summarize-core-v2` | **PASS** | Regenerated cross-run summaries |
| Pole asymmetry audit | **PASS** | `eager_lazy_pole_asymmetry.md` written |
| `checksum_key_outputs.sh` | **PASS** | Matches `KEY_OUTPUTS.sha256` |
| `export_paper_figures.py` | **PASS** | `results/core_v2/figures/strip_level_recovery_curves.png` |
| **Overall** | **PASS** | `Artifact verification passed.` |

## Replay mode

`INVERT_VERIFY_REPLAY` was **not** set (default). No LLM regeneration or `analyze-run` replay was performed.

## Environment notes

- First venv attempt used system `python3` → Python 3.6 (too old); recreated with `python3.12`.
- Ollama and API keys **not required** for read-only verification.
- `.venv/` created locally for verification; excluded from replication bundle per policy.

## Post-copy edits

- Removed `[project.optional-dependencies] lpr` from `pyproject.toml`
- Set `testpaths = ["tests/core_v2"]`
- Simplified `setup_project_venv.sh` and `activate_project_venv.sh` (no LPR profile)
