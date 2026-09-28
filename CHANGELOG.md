# Changelog

## v2.1.1 — 2026-09-28

Provenance/documentation patch over v2.1.0. Scientific contents and results unchanged.

- Archives the exact archive-write stripping implementation (`24617de8…`) that produced historical Class B/C transformed trees
- Corrects public role labels: `5032952f…` is a historical-analysis/re-stripping snapshot that already contains `PUBLIC_API_PRESERVE`, not the archive-write producer
- Adds `provenance/stripping/STRIPPING_PROVENANCE.csv` and a three-state README
- Extends `scripts/verify_v2_offline_headlines.py` to check all three stripper snapshot hashes
- Headline offline evidence unchanged (450/1800/630; 35.0%; design counts B–E unchanged)
- Concept DOI unchanged: `10.5281/zenodo.21154895`

## v2.1.0 — 2026-09-28

Canonical public replication package on `cesar-andress/invert-kernel`.

- Migrates validated scientific contents of `cesar-andress/invert` tag `v2.0.1` (commit `015df20186551c07579e66265785190f49a1767c`)
- Scientific offline evidence unchanged (450/1800/630; 35.0%; design counts B–E unchanged)
- Public hygiene tree (no manuscript LaTeX; no local agent configuration)
- Concept DOI for this repository: `10.5281/zenodo.21154895`

## v2.0.1 — 2026-09-28

Public-hygiene replication release for the IST manuscript.

- Same offline scientific evidence as the internal v2.0.0 freeze (450/1800/630; 35.0%)
- Removed manuscript LaTeX drafts and `.cursor` agent rules from the public tree
- Supersedes v2.0.0 for GitHub Release / Zenodo archival publication
- Historical Zenodo version DOI `10.5281/zenodo.21063175` unchanged
- Concept DOI `10.5281/zenodo.21063174`

## v2.0.0 — 2026-09-28

Replication package supporting the IST manuscript after offline scientific closure.

- Archive-as-written re-oracling (2250 checks; 1800 transformed; 630 failures)
- Class-C format_normalized provenance clarification
- Cumulative renaming-defect mechanism documentation
- Design counts and hash-distinct valid counts
- Baseline/control comparator analyses
- Unconditional/conditional auditor stability and failure taxonomy
- Historical (`5032952f…`) and current (`aace1f27…`) stripping snapshots
- `scripts/verify_v2_offline_headlines.py` no-model verifier

Historical Zenodo version DOI `10.5281/zenodo.21063175` is unchanged.

## v1.0.1 — 2026-06-30

Metadata correction release; confirmatory science artifacts unchanged from v1.0.0.

## v1.0.0 — 2026-06-30

Initial public replication deposit.
