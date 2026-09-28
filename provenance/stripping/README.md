# Stripping implementation provenance

## Snapshots

| Label | Content SHA-256 | Role |
|-------|-----------------|------|
| `historical_5032952fceaf4c6b/` | `5032952fceaf4c6b36e78b3f4414a0df1658d4abb37c53692d88356c82b310e0` | Stripping source near Class C freeze; **no** public-API preserve for the archived B/C transformed trees used by re-oracling |
| `current_aace1f27a9199db7/` | `aace1f27a9199db78266694f63266c57a782851c4e31fa6126150ad6f338a18b` | Current `src/invert_core/stripping.py` with `PUBLIC_API_PRESERVE` for dynamic dimensions |

Historical snapshot recovered from git commit `6ed9512818619556f5c37d57379c1f35a59a2eff`.

## How each path was used

1. **Archived transformed trees** under `data/core_v2/stripped/<run>/<level>/` were produced historically **without** the later public-API preserve behavior for Classes B/C (and are the inputs to archive-as-written re-oracling).
2. **Historical analyzer path** for dynamic dimensions (`analyze_*` via `_read_code`) re-stripped from **raw** using `strip_code(..., dimension=...)`, which applies public-API preserve in the *current* code path. Those re-stripped bytes are **not** the archived transformed trees.
3. **Phase-5 / Phase-2 offline re-oracling** evaluates **archived transformed trees as stored** (archive-as-written). It does **not** replace those trees with current-stripper output.

These implementations are **not** equivalent. Do not conflate archive-as-written evidence with current re-strip behavior.
