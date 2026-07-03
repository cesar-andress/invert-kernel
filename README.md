# INVERT Kernel

## Replication Package

**Release:** v1.0.0 (frozen **Core v2** implementation)  
**Zenodo DOI:** [10.5281/zenodo.21063175](https://doi.org/10.5281/zenodo.21063175)

**Paper:** *INVERT Kernel: A Methodology for Contract-Bound Process Auditing of Outcome-Equivalent Code* (ACM TOSEM; LaTeX maintained separately from this repository).

> **What this repository is.** This is the **INVERT Kernel replication package** — the public home for reproducing the paper’s audit methodology. The bundled code, data, and reports implement the frozen **Core v2** artifact (an internal protocol version identifier, not a separate product line). There is no separate “Core v1” or “Core v3” release in this deposit; **Core v2** names the frozen implementation generation archived here.

---

## What this repository is (three layers)

| Layer | Name | In this package |
|-------|------|-----------------|
| **Methodology** | **INVERT Kernel** | Specification concepts: trace contract, validity/recovery firewall, frozen detectors, abstention, negative controls, stripping probes. Documented in the paper §Kernel; **not** a separate codebase. |
| **Instantiation** | **Family 1** | Five controlled task classes (A–E), preregistered JSON tasks, harnesses, and frozen generalization runs B–E. |
| **Artifact (frozen implementation)** | **Core v2** | Internal version of the replication artifact in this repository: archived generated code, per-run CSVs/reports, detector metadata, verification scripts, checksum baseline (`data/core_v2/`, `results/core_v2/`). |

**Core v2** is the frozen **implementation generation** of Kernel-compliant auditing for **Family 1** in this package. It does not include LPR, external benchmark studies, or legacy prototype confirmatory claims.

---

## What verification proves

Default verification confirms **without LLM regeneration**:

1. **Fixture integrity** — smoke-test exercises frozen detectors and oracles on deterministic fixtures.
2. **Frozen instrument hashes** — `frozen_detector_metadata.json` matches current shared detector sources; per-run `stripping.py` freeze-time hashes match `ARTIFACTS.md` inventory.
3. **Archived confirmatory outputs** — SHA256 of key reports/CSVs matches `KEY_OUTPUTS.sha256`.
4. **Aggregation consistency** — `summarize-core-v2` rebuilds cross-run tables from archived per-run CSVs only.
5. **(Full path only)** pytest suite + Class C pole audit + supplementary figure export.

Verification does **not** prove ecological validity, arbitrary-code recovery, or benchmark superiority (paper non-claims).

---

## What verification does **not** do by default

| Action | Default? | Notes |
|--------|----------|-------|
| Call Ollama / cloud LLM APIs | **No** | Archived `data/core_v2/code/` is bundled |
| Regenerate model outputs | **No** | Optional shell scripts under `scripts/run_core_v2_*` |
| Re-run `analyze-run` on all frozen code | **No** | Set `INVERT_VERIFY_REPLAY=1` for detector replay (may refresh CSVs) |
| Require API keys | **No** | |

---

## 10–15 minute artifact review path

**First-time setup (~5–10 min):**

```bash
cd /path/to/invert-kernel    # repository root (this directory)
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

**Quick verification (~2–5 min after setup):**

```bash
bash scripts/verify_artifact_quick.sh
```

Runs: `smoke-test` → detector metadata hash check → checksum diff → `summarize-core-v2`.

**Full verification (~5 min after setup):**

```bash
bash scripts/verify_artifact.sh
```

Adds: `pytest` (187 tests) → Class C pole-asymmetry audit → figure export.

See **`ARTIFACT_QUICKSTART.md`** for step-by-step reviewer instructions.

---

## Smoke vs checksum vs full

| Command | Purpose | Time (after install) |
|---------|---------|----------------------|
| `invert-core smoke-test` | Fixture detectors + oracles | ~1 s |
| `bash scripts/verify_detector_hashes.sh` | Frozen metadata vs sources | ~1 s |
| `bash scripts/checksum_key_outputs.sh \| diff - KEY_OUTPUTS.sha256` | Confirmatory output digests | ~1 s |
| `bash scripts/verify_artifact_quick.sh` | Recommended reviewer path | ~2–5 s |
| `bash scripts/verify_artifact.sh` | Full ACM artifact check | ~4–5 s |
| `INVERT_VERIFY_REPLAY=1 bash scripts/verify_artifact.sh` | Re-analyze archived code | minutes |

---

## Detector hash checking

Each frozen generalization run stores `results/core_v2/runs/<run_id>/frozen_detector_metadata.json` with:

- `git_commit` — repository state at freeze (historical; single-commit Zenodo bundle may not contain full git history)
- `detector_files_hash` — SHA256 per detector module at freeze time
- `timestamp` — UTC freeze marker

**Verify:**

```bash
bash scripts/verify_detector_hashes.sh
```

Shared modules (`integration.py`, `quadrature.py`, `eager_lazy.py`, `bfs_dfs.py`, `deterministic_randomized.py`) must match **current** sources. `stripping.py` may differ between Class D and Class E freeze times; metadata is checked against `ARTIFACTS.md` inventory; **archived per-run CSVs** (checksum-verified) are authoritative for paper numbers.

Full hash inventory: **`ARTIFACTS.md`** §Frozen detector metadata.

---

## Paper figures and tables → files

See **`PAPER_TO_ARTIFACT_MAP.md`** for claim-level mapping (manuscript label → artifact path → verification command).

Quick index:

| Manuscript | Artifact source |
|------------|-----------------|
| `tab:frozen-confirmatory`, `tab:app:frozen-evidence` | `results/core_v2/core_v2_decision_report.md`, per-run `*_report.md` |
| `tab:pole-asymmetry-main`, Class C controls | `.../eager_lazy_pole_asymmetry.{md,csv}` |
| `tab:failures`, `tab:anomaly-catalog` | Run reports + `core_v2_decision_report.md` |
| `fig:strip-curves` (appendix) | `python scripts/export_paper_figures.py` → `results/core_v2/figures/strip_level_recovery_curves.png` |
| Protocol tables (`tab:detectors`, `tab:stripping`) | `src/invert_core/detectors/`, `prereg/normalizations.md` |

LaTeX/TikZ figures (`fig:pipeline`, etc.) are compiled from the separate paper tree.

---

## Frozen generalization run IDs (Family 1 confirmatory)

| Class | Run ID |
|-------|--------|
| B | `core_v2_generalization_local_quadrature_001` |
| C | `core_v2_generalization_local_eager_lazy_001` |
| D | `core_v2_generalization_local_bfs_dfs_001` |
| E | `core_v2_generalization_local_deterministic_randomized_001` |

Class A: pilots only; no frozen generalization in confirmatory readout.

---

## Repository layout

```
├── README.md                      # this file
├── ARTIFACT_QUICKSTART.md         # 10–15 min reviewer path
├── PAPER_TO_ARTIFACT_MAP.md       # manuscript ↔ artifact mapping
├── REPRODUCIBILITY.md             # command matrix
├── ARTIFACTS.md                   # inventory + detector hashes
├── KEY_OUTPUTS.sha256             # checksum baseline
├── configs/                       # YAML run configurations
├── scripts/
│   ├── verify_artifact_quick.sh   # recommended quick path
│   ├── verify_artifact.sh         # full verification
│   ├── verify_detector_hashes.sh
│   └── checksum_key_outputs.sh
├── prereg/                        # task registry, strip definitions
├── data/core_v2/                  # archived LLM outputs + generated code
├── src/invert_core/               # frozen Core v2 implementation (CLI, detectors, oracles)
├── tests/core_v2/                 # pytest suite
└── results/core_v2/               # reports, CSVs, frozen metadata
```

---

## Installation

**Requirements:** Python ≥ 3.10 (tested on 3.12), `git` optional.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

---

## Key reports (read-only)

| Output | Path |
|--------|------|
| Cross-run decision report | `results/core_v2/core_v2_decision_report.md` |
| Dimension summary | `results/core_v2/core_v2_dimension_summary.csv` |
| Model × dimension | `results/core_v2/core_v2_model_dimension_summary.csv` |
| Per-run reports | `results/core_v2/runs/<run_id>/*_report.md` |
| Class C pole audit | `.../eager_lazy_pole_asymmetry.md` |

---

## CLI

```bash
invert-core --help    # generate, analyze-run, summarize-core-v2, smoke-test, …
```

Legacy `invert` CLI (prototype) is bundled but not used for Family 1 confirmatory claims.

---

## Further documentation

Scope boundaries for confirmatory vs exploratory material: this README (§What verification proves), `ARTIFACTS.md`, and `docs/EXTERNAL_FEASIBILITY_NOTE.md`.

- `ARTIFACT_QUICKSTART.md` — artifact evaluator quick path
- `PAPER_TO_ARTIFACT_MAP.md` — tables/figures/claims → files
- `REPRODUCIBILITY.md` — per-run regeneration commands
- `ARTIFACTS.md` — file inventory
- `docs/EXTERNAL_FEASIBILITY_NOTE.md` — exploratory external-validation boundary (non-confirmatory)
- `PAPER_ARTIFACTS.md` — legacy alias; see `PAPER_TO_ARTIFACT_MAP.md`

---

## Zenodo packaging

`MANIFEST_ZENODO.txt` lists intended inclusions and exclusions for the Zenodo archive. **Do not upload** `.git/`, `.venv/`, `.pytest_cache/`, `__pycache__/`, or `*.egg-info/`. Validate static paths before upload:

```bash
bash scripts/validate_zenodo_json.sh
bash scripts/validate_release_manifest.sh
```

---

## Citation & license

**Artifact:** INVERT Kernel — Replication Package v1.0.0 (frozen Core v2 implementation) — DOI [10.5281/zenodo.21063175](https://doi.org/10.5281/zenodo.21063175).  
**License:** MIT (`LICENSE`). See `CITATION.cff`.
