# INVERT: Controlled Process-Signature Auditing — Replication Package v2.0.1

Replication package for the manuscript:

“Auditing Process Signatures in Behaviorally Equivalent Generated Code:
A Controlled Empirical Protocol.”

This release archives the generated programs, transformed artifacts, traces,
task configurations, deterministic auditors, baseline analyses, provenance
metadata, and offline validation scripts supporting the study.

Version 2.0.1 includes the final offline validation used in the manuscript,
including 450 raw consistency checks and 1,800 transformed-artifact behavioral
re-oracle checks, evidence-removal baseline analyses, unconditional and
behavior-preserving auditor-stability summaries, failure-taxonomy outputs, and
headline-result traceability.

Of the 1,800 transformed checks, 630 fail behavioral preservation. These failures
arise from a historical public-API renaming defect propagated through cumulative
transformation levels; the release preserves the historical transformed
artifacts exactly as archived and documents the historical/current stripping
implementations separately.

All headline results can be verified from archived artifacts without new LLM
generation or paid API calls.

The study is intentionally scoped to controlled, contract-bound process auditing
of generated Python code and does not claim general-purpose process recovery or
external transfer of the archived auditors.

## Relation to v2.0.0

Annotated tag `v2.0.0` is retained as an immutable internal historical tag.
**v2.0.1** is the public-hygiene release (manuscript drafts and local agent
configuration removed from the public tree). Publish GitHub Release / Zenodo
from **v2.0.1** only.

## Reproduce without models

```bash
pytest -q
python scripts/verify_v2_offline_headlines.py
```

See `REPRODUCIBILITY.md`.
