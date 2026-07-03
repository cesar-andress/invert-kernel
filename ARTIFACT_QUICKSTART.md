# Artifact Quickstart (10–15 minutes)

**Package:** INVERT Kernel — Replication Package v1.0.0  
**Frozen implementation:** Core v2 (internal protocol version)  
**Audience:** TOSEM / ACM artifact evaluators  
**Policy:** Read-only verification by default — no LLM calls, no API keys.

---

## Conceptual hierarchy

| Layer | Name | In this repository |
|-------|------|-------------------|
| Methodology | **INVERT Kernel** | Documented in the paper; concepts exercised by verification |
| Instantiation | **Family 1** | Preregistered tasks and frozen generalization runs B–E |
| Frozen artifact | **Core v2** | This package’s archived `data/core_v2/` and `results/core_v2/` tree |

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python ≥ 3.10 | Tested on 3.12; `python3 --version` must be 3.10+ (`verify_artifact*.sh` checks this) |
| `bash`, `sha256sum` | Linux/macOS standard; WSL OK |
| Disk space | ~200 MB extracted (code + archived outputs) |
| Network | Only for `pip install` (PyPI); verification itself is offline |
| Ollama / API keys | **Not required** for default verification |

**Obtain the package:** download and extract the Zenodo archive, or clone the repository. All commands below assume your shell’s working directory is the **package root** (the directory containing `pyproject.toml` and `README.md`).

---

## Step 1 — First-time setup (~5–10 min)

```bash
cd /path/to/invert-kernel    # package root
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e ".[dev]"
```

**Expected:** `invert-core --help` prints the Core v2 CLI usage without error.

---

## Step 2 — Quick verification (~2–5 s after setup)

```bash
bash scripts/verify_artifact_quick.sh
```

**What it runs (in order):**

1. `invert-core smoke-test` — fixture detectors and behavioral oracles  
2. `bash scripts/verify_detector_hashes.sh` — frozen metadata vs current detector sources  
3. `bash scripts/checksum_key_outputs.sh | diff - KEY_OUTPUTS.sha256` — confirmatory output digests  
4. `invert-core summarize-core-v2` — re-aggregate archived per-run CSVs only  

**Expected final line:**

```
Quick artifact verification passed.
```

**On failure:** see [Troubleshooting](#troubleshooting) below.

---

## Step 3 — Full verification (~4–5 s after setup)

```bash
bash scripts/verify_artifact.sh
```

**Adds to the quick path:**

- `pytest` — **187 tests** (as of v1.0.0)  
- Class C pole-asymmetry audit (regenerates `eager_lazy_pole_asymmetry.{md,csv}` from archived detection CSVs)  
- `python scripts/export_paper_figures.py` → `results/core_v2/figures/strip_level_recovery_curves.png`  
- Checksum diff (again, after aggregation)

**Expected final line:**

```
Artifact verification passed.
```

---

## Step 4 — Spot-check paper claims (~5 min)

Open these files and compare to the manuscript (Family 1 readout tables):

| Paper table / claim | Artifact file |
|---------------------|---------------|
| `tab:frozen-confirmatory` (Stage 1 + survival) | `results/core_v2/core_v2_decision_report.md` |
| `tab:pole-asymmetry-main` | `results/core_v2/runs/core_v2_generalization_local_eager_lazy_001/eager_lazy_pole_asymmetry.md` |
| `tab:control-audit-readout` | Class C: `.../eager_lazy_full_demand_control.csv`; Class D: `.../bfs_dfs_negative_control.csv`; Class E: `.../deterministic_randomized_fixed_seed_control.csv` |
| Appendix strip curves | `results/core_v2/figures/strip_level_recovery_curves.png` (after full verify) |

Full claim-level index: **`PAPER_TO_ARTIFACT_MAP.md`**.

---

## Optional — detector replay (not default)

To re-run `analyze-run` on archived generated code (may refresh CSVs if detector sources changed after freeze):

```bash
INVERT_VERIFY_REPLAY=1 bash scripts/verify_artifact.sh
```

Default v1.0.0 artifact evaluation uses **checksum-verified archived CSVs**, not replay.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `error: Python >= 3.10 required` | System `python3` is too old | Install Python 3.10+; create venv with `python3.12 -m venv .venv` |
| `pip install` fails on `setuptools>=61.0` | Ancient pip on old Python | Use Python 3.10+; run `pip install --upgrade pip` before editable install |
| `invert-core: command not found` | venv not activated or install skipped | `source .venv/bin/activate && pip install --upgrade pip && pip install -e ".[dev]"` |
| `MISSING results/core_v2/...` in checksum step | Incomplete Zenodo download | Re-download; confirm `MANIFEST_ZENODO.txt` inclusions |
| Checksum `diff` fails after local edits | Modified confirmatory outputs | Restore from archive or re-download |
| `pytest` import errors | Wrong working directory | `cd` to package root (where `pyproject.toml` lives) |
| `git_commit` is `unknown` in newly written metadata | Zenodo bundle has no `.git` (expected) | Does not affect default verification; archived `frozen_detector_metadata.json` in run dirs retain freeze-time commits |
| Detector hash `MISMATCH` on shared modules | Local edits to `src/invert_core/detectors/` | Do not edit detector sources when verifying; use pristine bundle |

---

## What this package does **not** require

- Ollama or cloud LLM APIs (archived `data/core_v2/code/` is bundled)  
- Regenerating model outputs  
- Access to the separate LaTeX paper tree (figures compiled from TikZ live outside this deposit)

---

## Further reading

| Document | Purpose |
|----------|---------|
| `README.md` | Package overview and layout |
| `REPRODUCIBILITY.md` | Per-run replay and optional regeneration commands |
| `ARTIFACTS.md` | File inventory and detector hash table |
| `PAPER_TO_ARTIFACT_MAP.md` | Manuscript label → file → verify command |
| `docs/EXTERNAL_FEASIBILITY_NOTE.md` | Exploratory external-validation boundary (non-confirmatory) |
| `MANIFEST_ZENODO.txt` | Intended Zenodo inclusions/exclusions |

**Citation:** `CITATION.cff` — DOI [10.5281/zenodo.21063175](https://doi.org/10.5281/zenodo.21063175).
