# INVERT Kernel — frozen Core v2 results (v1.0.0)

Outputs from `invert-core` commands land under this directory (`results/core_v2/`). **Core v2** is the internal frozen implementation version; confirmatory paper claims use the four **Family 1** frozen generalization run directories listed in the repository `README.md`.

## Cross-run summaries

| File | Regenerate |
|------|------------|
| `core_v2_decision_report.md` | `invert-core summarize-core-v2` |
| `core_v2_dimension_summary.csv` | `invert-core summarize-core-v2` |
| `core_v2_model_dimension_summary.csv` | `invert-core summarize-core-v2` |

## Per-run directories

`runs/<run_id>/` contains detection CSVs, valid-only summaries, dimension reports, and (for frozen generalization) `frozen_detector_metadata.json`.

## Figures

`figures/strip_level_recovery_curves.png` — exported by `python scripts/export_paper_figures.py` (see `PAPER_TO_ARTIFACT_MAP.md`).

## Verification

```bash
bash scripts/verify_artifact.sh
bash scripts/checksum_key_outputs.sh   # compare to ../KEY_OUTPUTS.sha256 at repo root
```
