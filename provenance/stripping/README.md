# Stripping implementation provenance

This directory archives **three** distinct `stripping.py` states used in the
INVERT evidence chain. They are not interchangeable.

## Three-state summary

| Role | Directory | SHA-256 | `PUBLIC_API_PRESERVE` |
|------|-----------|---------|------------------------|
| **archive-write** | `archive_write_24617de8e91c0d47/` | `24617de8e91c0d47902f2d72f39ec9620dfcc65096e26355bb91615297b3db06` | Absent |
| **historical-analysis** | `historical_5032952fceaf4c6b/` | `5032952fceaf4c6b36e78b3f4414a0df1658d4abb37c53692d88356c82b310e0` | Present (Class C/D) |
| **current** | `current_aace1f27a9199db7/` | `aace1f27a9199db78266694f63266c57a782851c4e31fa6126150ad6f338a18b` | Present (Class C/D/E) |

Machine-readable table: `STRIPPING_PROVENANCE.csv`.

## Why the distinction matters

1. **archive-write.** Exact historical module that wrote the archived Class B/C
   transformed trees under `data/core_v2/stripped/`. Identifier renaming has no
   public-API preserve list and `strip_code` has no `dimension=` argument, so
   oracle-required names (for example Class C `FeaturePipeline` / `get_feature_*`)
   are renamed. Archive-as-written re-oracling uses those trees as stored.
2. **historical-analysis.** Later historical module recovered from git commit
   `6ed9512818619556f5c37d57379c1f35a59a2eff`. Its body already defines
   `PUBLIC_API_PRESERVE` for `eager_vs_lazy` and `bfs_vs_dfs`. It is **not** the
   implementation that wrote the archived B/C transformed trees. Dynamic
   `analyze_*` paths can re-strip from raw with preserve; those bytes differ from
   the archived trees. Class C freeze metadata does not record the exact
   analysis-time module hash; this snapshot is the earliest preserve-bearing
   hash in the recovered lineage.
3. **current.** Head / release `src/invert_core/stripping.py` (and matching
   snapshot). Preserves Class C/D public APIs and additionally lists Class E.

Do **not** conflate archive-as-written evidence with analysis-time re-stripping
or with current re-strip output. Do **not** regenerate archived transformed trees.

## Recovery note (archive-write)

`archive_write_24617de8e91c0d47/stripping.py` was recovered byte-identical from
`cesar-andress/invert` commit `aa2d9152a905c0bc57697dd99729d27f1e60ae10`
(`src/invert_core/stripping.py`). See `SOURCE.txt` in that directory.
