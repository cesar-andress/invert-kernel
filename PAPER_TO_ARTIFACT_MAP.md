# Paper → Artifact Map

Maps ACM TOSEM manuscript claims to files in the **INVERT Kernel — Replication Package** (frozen **Core v2** implementation) and the command that verifies each claim.

**Release:** INVERT Kernel — Replication Artifact v1.0.0  
**Zenodo:** [10.5281/zenodo.21154896](https://doi.org/10.5281/zenodo.21154896)  
**GitHub release:** [v1.0.0](https://github.com/cesar-andress/invert-kernel/releases/tag/v1.0.0)  

**Paper title:** *INVERT Kernel: A Methodology for Contract-Bound Process Auditing of Outcome-Equivalent Code*  
**LaTeX:** maintained separately from this repository.  
**Policy:** Confirmatory statistics use four frozen generalization runs only (Classes B–E). No LLM calls required for verification.

**Legend — verification commands:**

| Command | Meaning |
|---------|---------|
| `quick` | `bash scripts/verify_artifact_quick.sh` |
| `full` | `bash scripts/verify_artifact.sh` |
| `checksum` | `bash scripts/checksum_key_outputs.sh \| diff - KEY_OUTPUTS.sha256` |
| `hashes` | `bash scripts/verify_detector_hashes.sh` |
| `inspect` | Manual read of listed file(s) |
| `code` | Source inspection, no numeric recompute |

---

## Kernel methodology (paper specification)

| Manuscript claim / table | Table/Figure | Artifact file(s) | Verify |
|--------------------------|--------------|------------------|--------|
| Kernel outcome taxonomy | `tab:protocol-outcomes`, `tab:audit-layers` | `src/invert_core/analyze_run.py`, `src/invert_core/summarize_core_v2.py` | `code` + `full` |
| Behavioral oracles (Stage 1) | `tab:behavioral-oracles` | `src/invert_core/*_behavioral.py` | `quick` (smoke-test) |
| Frozen detectors by dimension | `tab:detectors` | `src/invert_core/detectors/*.py` | `hashes` |
| Stripping levels | `tab:stripping` | `prereg/normalizations.md`, `src/invert_core/stripping.py` | `code` |
| Survival rule | `tab:survival-rule` | `src/invert_core/summarize_core_v2.py` | `full` |
| Negative controls | `tab:controls`, `tab:controls-split` | `src/invert_core/detectors/*`, control CSVs in run dirs | `inspect` + `full` |
| Kernel invariants | `tab:kernel-invariants` | Paper + this package layout | `inspect` |

---

## Family 1 instantiation readout (confirmatory)

| Manuscript claim / table | Table/Figure | Artifact file(s) | Verify |
|--------------------------|--------------|------------------|--------|
| Frozen run IDs | `tab:frozen-runs` | `configs/core_v2_generalization_local_*.yaml`, `results/core_v2/runs/` | `inspect` |
| Family 1 master structure | `tab:invert-master` | `prereg/core_v2_tasks.json`, `data/core_v2/tasks/*.json` | `inspect` |
| Protocol execution snapshot | `tab:frozen-confirmatory` | `core_v2_decision_report.md`, per-run `*_report.md` | `checksum` + `inspect` |
| Appendix frozen evidence | `tab:app:frozen-evidence` | `results/core_v2/core_v2_decision_report.md` | `quick` (summarize) |
| Development inventory | `tab:dimension-snapshot` | `results/core_v2/core_v2_dimension_summary.csv` | `quick` |
| Class B quadrature readout | (in `tab:frozen-confirmatory`) | `runs/core_v2_generalization_local_quadrature_001/quadrature_report.md` | `checksum` |
| Class C aggregate recovery | `tab:class-c-recovery` | `.../eager_lazy_report.md`, `eager_lazy_valid_only_summary.csv` | `checksum` |
| Class C pole asymmetry | `tab:pole-asymmetry-main`, `tab:app:pole-partial` | `.../eager_lazy_pole_asymmetry.{md,csv}` | `full` (pole audit) |
| Class C full-demand control | `tab:app:pole-full-demand` | `.../eager_lazy_full_demand_control.csv` | `inspect` |
| Class D branching graph | `tab:class-d-recovery` | `.../bfs_dfs_report.md` | `checksum` |
| Class D linear-chain control | §Results controls | `.../bfs_dfs_negative_control.csv` | `inspect` |
| Class E variability | `tab:class-e-recovery` | `.../deterministic_randomized_report.md` | `checksum` |
| Class E fixed-seed control | §Results controls | `.../deterministic_randomized_fixed_seed_control.csv` | `inspect` |
| Class E API repair boundary | `tab:failures`, `tab:anomaly-catalog` | `results/core_v2/runs/core_v2_deterministic_randomized_pilot_local_001/deterministic_randomized_diagnosis.md` | `inspect` |
| Dynamic class aggregate | `tab:dynamic-ce-summary` | `core_v2_dimension_summary.csv` | `quick` |
| Documented failures | `tab:failures` | `core_v2_decision_report.md`, run reports | `inspect` |
| Anomaly/abstention catalog | `tab:anomaly-catalog` | Same sources as above (interpretability index) | `inspect` |
| Model × dimension breakdown | (prose) | `core_v2_model_dimension_summary.csv` | `quick` |

---

## Threats, limitations, reproducibility

| Manuscript claim / table | Table/Figure | Artifact file(s) | Verify |
|--------------------------|--------------|------------------|--------|
| Claim / falsification maps | `tab:claim-map`, `tab:falsification-map` | Methodology + archived outcomes | `inspect` |
| Frozen detector metadata schema | `tab:app:metadata-schema` | `runs/*/frozen_detector_metadata.json` | `hashes` |
| Artifact index | `tab:app:artifact-index` | This repository tree | `inspect` |
| Data availability | §Data Availability | Zenodo DOI bundle + `verify_artifact.sh` | `full` |

---

## Figures

| Manuscript figure | Status | Artifact / command | Verify |
|-------------------|--------|-------------------|--------|
| `fig:pipeline`, `fig:family1-map`, `fig:controls-logic` | LaTeX/TikZ in paper repo | Not in replication package | N/A |
| `fig:process-traces` | LaTeX + archived traces | Run detection CSVs under `data/core_v2/` | `inspect` |
| `fig:strip-curves` / `fig:app:strip-*` | Appendix | `python scripts/export_paper_figures.py` → `results/core_v2/figures/strip_level_recovery_curves.png` | `full` |
| `fig:app:negative-controls` | LaTeX placeholder | Class C control CSVs + pole audit | `inspect` |

---

## Explicitly out of scope in this package

| Topic | Paper reference | In artifact? | Verify |
|-------|-----------------|--------------|--------|
| LPR / latent process risk | `sec:limitations:non-claims` | **No** | — |
| External benchmark validation | `externalclosure` note | `docs/EXTERNAL_FEASIBILITY_NOTE.md` (non-confirmatory) | `inspect` |
| Legacy `invert` prototype runs | — | Bundled, not confirmatory | — |
| LLM re-generation | Optional scripts | **Not** default verification | — |

---

## One-line reviewer checklist

```bash
pip install -e ".[dev]" && bash scripts/verify_artifact_quick.sh && bash scripts/verify_artifact.sh
```

Then spot-check `core_v2_decision_report.md` and `eager_lazy_pole_asymmetry.md` against paper Table `tab:frozen-confirmatory` and `tab:pole-asymmetry-main`.
