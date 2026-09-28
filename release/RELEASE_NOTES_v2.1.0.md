# INVERT: Controlled Process-Signature Auditing — Replication Package v2.1.0

Replication package for the manuscript:

“Auditing Process Signatures in Behaviorally Equivalent Generated Code:
A Controlled Empirical Protocol.”

This release archives the generated programs, transformed artifacts, traces,
task configurations, deterministic auditors, baseline analyses, provenance
metadata, and offline validation scripts supporting the study.

Version **2.1.0** is the **canonical public package** on
`cesar-andress/invert-kernel`. It migrates the validated scientific contents of
`cesar-andress/invert` tag **v2.0.1** (commit
`015df20186551c07579e66265785190f49a1767c`) without changing scientific results.

It includes:

- 450 raw consistency checks;
- 1,800 transformed-artifact behavioral re-oracle checks;
- 630 transformed checks failing behavioral preservation after a historical
  public-API renaming defect propagated through cumulative transformation levels;
- evidence-removal baseline analyses;
- unconditional and behavior-preserving auditor-stability summaries;
- failure-taxonomy outputs;
- headline-result traceability.

All headline results can be verified from archived artifacts without new LLM
generation or paid API calls.

```bash
pytest -q
python scripts/verify_v2_offline_headlines.py
```

See `REPRODUCIBILITY.md` and `MIGRATION_PROVENANCE.md`.
