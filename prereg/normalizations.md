# INVERT Kernel — Core v2 stripping normalizations (Family 1)

Deterministic transforms applied cumulatively by level.

## Levels (cumulative)

| Level | Transforms applied |
|-------|-------------------|
| `raw` | None |
| `no_comments` | Remove `#` comments and module/class/function docstrings via AST |
| `renamed` | + deterministic α-renaming of user identifiers to `x0`, `x1`, … |
| `no_imports` | + remove all `import` / `from … import` nodes |
| `format_normalized` | + `ast.parse` → `ast.unparse` canonical formatting |

## Invariants

- Stripping is **deterministic** (same input → same output).
- Stripping never executes code.
- Process signatures for F1.1 (derivative evaluations per step, RK4 weighted sum)
  must survive all levels except where noted in prereg.

## Ablation order for verification

```text
raw → no_comments → renamed → no_imports → format_normalized
```

## Implementation

`invert_core.stripping.strip_code(code, level)`

CLI: `invert-core strip <file.py> --level <level>`
