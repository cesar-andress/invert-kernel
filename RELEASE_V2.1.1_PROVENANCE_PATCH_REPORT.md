# RELEASE_V2.1.1_PROVENANCE_PATCH_REPORT

**Date:** 2026-09-28  
**Repository:** `cesar-andress/invert-kernel`  
**Local path:** `/home/cesar/papers/invert/invert-kernel-migration`  
**Nature:** Provenance/documentation patch only (no scientific revision)

## v2.1.0 protection

| Item | Value |
|------|-------|
| Tag object (unchanged) | `bde6b469b5347fca33b4fbdec0b06d48bd837f9c` |
| Tagged commit (unchanged) | `68a1d31ec121a8666ecc02bd67c7f934326394f0` |
| Tag moved/deleted/recreated | **NO** |

## Archive-write recovery

| Field | Value |
|-------|-------|
| Recovered | YES |
| Full SHA-256 | `24617de8e91c0d47902f2d72f39ec9620dfcc65096e26355bb91615297b3db06` |
| Source repository | `cesar-andress/invert` |
| Source path | `src/invert_core/stripping.py` |
| Source commit | `aa2d9152a905c0bc57697dd99729d27f1e60ae10` |
| Snapshot path | `provenance/stripping/archive_write_24617de8e91c0d47/stripping.py` |
| `PUBLIC_API_PRESERVE` | **Absent** |
| `strip_code(..., dimension=)` | **Absent** |
| Rename path | `_rename_identifiers(code)` with no preserve list (renames Class C `FeaturePipeline` / `get_feature_*`) |

## Three-state table

| Role | SHA-256 prefix | Snapshot |
|------|----------------|----------|
| archive-write | `24617de8…` | `archive_write_24617de8e91c0d47/` |
| historical-analysis | `5032952f…` | `historical_5032952fceaf4c6b/` |
| current | `aace1f27…` | `current_aace1f27a9199db7/` |

Files: `provenance/stripping/STRIPPING_PROVENANCE.csv`, updated `provenance/stripping/README.md`.

## Role corrections

Active docs updated so `5032952f…` is **not** described as the archive-write / no-preserve producer of archived B/C trees.

Historical release snapshots intentionally retained (not rewritten):
- `release/v2.0.1_manifest.csv` still contains the older incorrect purpose string.

## Gates

| Gate | Result |
|------|--------|
| Archived `data/core_v2` transformed trees modified | NO |
| Offline verifier | PASS (450 / 1800 / 630 / 0.350; B 90/90/15; C 120/120/5; D 120/120/12; E 120/120/12) |
| pytest | PASS (226 passed) |
| Public hygiene (no LaTeX/agent config in tracked tree) | PASS |
| Manuscript science edited | NO |

## Release artifacts

- `release/v2.1.1_manifest.csv`
- `release/RELEASE_NOTES_v2.1.1.md`
- Metadata bumped to v2.1.1: `CITATION.cff`, `.zenodo.json`, `pyproject.toml`, `README.md`, `CHANGELOG.md`, `REPRODUCIBILITY.md`, `MIGRATION_PROVENANCE.md`

## Zenodo / GitHub

Recorded in the closing checklist after push/release attempt.
Concept DOI remains `10.5281/zenodo.21154895`. Version DOI not invented.
