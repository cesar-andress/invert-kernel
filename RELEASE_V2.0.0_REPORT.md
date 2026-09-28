# INVERT RELEASE v2.0.0 REPORT

**Date:** 2026-09-28  
**Repository:** `cesar-andress/invert`  
**Title:** INVERT: Controlled Process-Signature Auditing — Replication Package v2.0.0

## Release identity

| Item | Value |
|------|-------|
| Pre-release branch | `main` |
| Pre-release HEAD (work start) | `e8cb8a716df01461f5cec8b0792911d66ca81fa0` |
| Release commit | `851949fe1ea706ebe845b51726a96163bec08c42` |
| Annotated tag | `v2.0.0` |
| Tag object SHA | `83e16f08c3d19da1fcb90469daa0b8fc12ffd8ba` |
| Tagged commit SHA | `851949fe1ea706ebe845b51726a96163bec08c42` |
| Existing v2.0.0 before phase | **NO** |
| Historical tags modified | **NO** |

## Push / GitHub / Zenodo

| Step | Status |
|------|--------|
| `git push origin main` | YES (`d523e0e..851949f`) |
| `git push origin v2.0.0` | YES (new annotated tag) |
| GitHub Release API | **MANUAL ACTION REQUIRED** (`gh`/`GITHUB_TOKEN` → HTTP 404 for private `cesar-andress/invert`) |
| Zenodo workflow | **MANUAL** (no `ZENODO_*` env; see `release/ZENODO_MANUAL_NEW_VERSION.md`) |
| Zenodo v2.0.0 published | **NO / MANUAL ACTION REQUIRED** |
| Zenodo version DOI | **PENDING** |
| Concept DOI | `10.5281/zenodo.21063174` |
| Historical version DOI (immutable) | `10.5281/zenodo.21063175` |
| Post-release DOI-sync commit | **PENDING** (after Zenodo version DOI) |
| v2.0.0 tag unchanged | **YES** (must remain immutable) |

## Verification

| Check | Result |
|-------|--------|
| `python scripts/verify_v2_offline_headlines.py` | PASS |
| Raw / transformed / failures / rate | 450 / 1800 / 630 / 35.0% |
| B/C/D/E generated/valid/hash-distinct-valid | 90/90/15; 120/120/5; 120/120/12; 120/120/12 |
| Historical stripper SHA-256 | `5032952fceaf4c6b36e78b3f4414a0df1658d4abb37c53692d88356c82b310e0` |
| Current stripper SHA-256 | `aace1f27a9199db78266694f63266c57a782851c4e31fa6126150ad6f338a18b` |
| `pytest -q` | PASS — 230 passed, 0 failed, 1 warning |
| Secret/privacy audit (staged release) | PASS (local path scrubbed; no `.env`; LPR dirt excluded) |
| License | MIT; no HumanEval+ tree bundled |

## Contents summary

- Byte-identical archived trees under `data/core_v2/` (already in repo history)
- Provenance snapshots under `provenance/stripping/`
- Canonical CSVs under `results/paper_audit_canonical/`
- Offline scripts: `scripts/phase2_offline_validation.py`, `scripts/phase5_review_closure.py`, `scripts/verify_v2_offline_headlines.py`
- Docs: `REPRODUCIBILITY.md`, `CHANGELOG.md`, `release/RELEASE_NOTES_v2.0.0.md`, `release/v2.0.0_manifest.csv` (32 entries)

## Manual actions still required

1. Create GitHub Release for tag `v2.0.0` in the GitHub UI (API token lacks repo access).
2. Zenodo → New version under concept `21063174` using the `v2.0.0` archive; do not edit `21063175`.
3. Record the new version DOI; DOI-sync commit on `main` (README/`CITATION.cff`/manuscript) **without moving the tag**.
4. Phase 7: IST submission packaging (not done here).

## Scientific blockers

**NONE** for the frozen offline evidence. Publication packaging blocked only on Zenodo version DOI assignment + GitHub Release metadata.
