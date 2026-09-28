# INVERT v2.0.0 release notes

**Title:** INVERT: Controlled Process-Signature Auditing — Replication Package v2.0.0

## Contents

This release supports the Information and Software Technology manuscript on controlled process-signature auditing.

It adds deterministic offline analyses performed **without new model generation**:

- separate behavioral re-oracling of archived transformed sources;
- corrected transformation provenance (historical vs current stripping);
- baseline and evidence-removal control comparisons;
- unconditional/conditional auditor stability;
- failure taxonomy;
- design/hash-distinct archive counts;
- one-command headline verifier: `python scripts/verify_v2_offline_headlines.py`.

## What did not change

- Historical generated and transformed archives remain byte-identical.
- Historical Zenodo record `10.5281/zenodo.21063175` is not overwritten.
- No LLM regeneration campaign was run for this revision.

## Reproduce without models

See `REPRODUCIBILITY.md`.
