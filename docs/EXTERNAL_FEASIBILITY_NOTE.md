# External Feasibility Note (Exploratory — Non-Confirmatory)

**Package:** INVERT Kernel — Replication Package v1.0.0  
**Status:** Scope documentation only — **not** confirmatory evidence  
**Paper reference:** limitations §External corpora; threats §Trace-contract dependence (`externalclosure` macro)

---

## Purpose

This note documents why **external benchmark snippets** and third-party code corpora are **out of scope** for the v1.0.0 Zenodo deposit and for Section 6 confirmatory readouts in the companion TOSEM manuscript.

The INVERT Kernel evaluates process signatures **under a declared trace contract**. Family 1 detectors were frozen against preregistered harness APIs (`visit_fn` callbacks, partial-demand getters, etc.). Applying those same frozen detectors to arbitrary external code without a matching contract would not yield interpretable pole labels.

---

## What was explored (not bundled)

Development included **exploratory feasibility probes** on external snippets (including competition-style benchmarks and EffiBench-style corpora) to test whether:

1. Class D (BFS/DFS) visit-order detectors could read traces from code that does not expose the `GraphTraversal.visit_fn` contract.  
2. Class E (deterministic vs randomized) cross-run identity detectors could read traces from code that does not expose the `ItemProcessor.visit_fn` contract.

**Observed boundary:** On snippets without the protocol-defined harness surface, frozen detectors **abstain** (`ambiguous`) or fail Stage 1 behavioral validation — they do not assign false poles. Adapter-based rewriting of external code to inject callbacks was rejected as a confirmatory path because it reintroduces co-design between task and detector.

Raw probe logs, third-party repository clones, and go/no-go JSON from these pilots are **excluded** from this replication package (see `MANIFEST_ZENODO.txt` §EXCLUDED). They do not affect any number in the frozen generalization runs B–E.

---

## Confirmatory evidence in this package

Confirmatory statistics bind **only** to four frozen Ollama-local generalization runs:

| Class | Run ID |
|-------|--------|
| B | `core_v2_generalization_local_quadrature_001` |
| C | `core_v2_generalization_local_eager_lazy_001` |
| D | `core_v2_generalization_local_bfs_dfs_001` |
| E | `core_v2_generalization_local_deterministic_randomized_001` |

Verification: `bash scripts/verify_artifact_quick.sh` (no external data required).

---

## Class E API repair (related boundary, confirmatory context)

The Class E **process-function pilot** (`core_v2_deterministic_randomized_pilot_local_001`) documented an ambiguous API relative to the trace contract (**0/120 valid** artifacts). The repair to a `visit_fn` interface occurred **before** the frozen generalization run. Diagnosis export:

`results/core_v2/runs/core_v2_deterministic_randomized_pilot_local_001/deterministic_randomized_diagnosis.md`

This pilot boundary is cited in the paper `tab:failures` and `tab:anomaly-catalog`; it is **not** an external-corpus claim.

---

## Future work (explicitly deferred)

Independent corpora would require:

1. A trace contract defined and frozen **before** evaluation.  
2. Behavioral oracles stated for that corpus.  
3. A new Kernel instantiation (not Family 1 pole labels).  

None of that is required to reproduce or verify the methodological claims bounded in the paper Claim Map.

---

## See also

- `ARTIFACTS.md` §External validation (out of scope for the companion TOSEM manuscript)  
- `PAPER_TO_ARTIFACT_MAP.md` §Explicitly out of scope  
- Paper §Limitations (`sec:limitations:non-claims`) — no benchmark superiority, no ecological validity, no hidden-test prediction
