#!/usr/bin/env python3
"""Phase 2 zero-cost offline validation: strip re-oracling + simple baselines.

Frozen analysis plan: paper/audit/phase2_offline_analysis_plan.md
No LLM calls. Does not modify archived artifacts.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from invert_core.bfs_dfs_behavioral import run_bfs_dfs_behavioral_oracle
from invert_core.bfs_dfs_tasks import load_bfs_dfs_tasks
from invert_core.detectors.bfs_dfs import detect_bfs_dfs, is_genuine_bfs, is_genuine_dfs
from invert_core.detectors.deterministic_randomized import (
    detect_deterministic_randomized,
    is_genuine_deterministic,
    is_genuine_randomized,
)
from invert_core.detectors.eager_lazy import (
    detect_eager_lazy,
    is_genuine_eager,
    is_genuine_lazy,
)
from invert_core.detectors.quadrature import detect_quadrature
from invert_core.deterministic_randomized_behavioral import (
    run_deterministic_randomized_behavioral_oracle,
)
from invert_core.deterministic_randomized_tasks import load_deterministic_randomized_tasks
from invert_core.eager_lazy_behavioral import run_eager_lazy_behavioral_oracle
from invert_core.eager_lazy_tasks import load_eager_lazy_tasks
from invert_core.quadrature_behavioral import run_quadrature_behavioral_oracle
from invert_core.quadrature_tasks import load_quadrature_tasks
from invert_core.tasks import project_root

OUT = ROOT / "results" / "phase2_offline_validation"
PAPER_AUDIT = ROOT.parent / "paper" / "audit"
STRIP_LEVELS = ["raw", "no_comments", "renamed", "no_imports", "format_normalized"]

RUNS = {
    "B": {
        "run_id": "core_v2_generalization_local_quadrature_001",
        "dimension": "trapezoidal_vs_simpson",
        "class": "B",
    },
    "C": {
        "run_id": "core_v2_generalization_local_eager_lazy_001",
        "dimension": "eager_vs_lazy",
        "class": "C",
    },
    "D": {
        "run_id": "core_v2_generalization_local_bfs_dfs_001",
        "dimension": "bfs_vs_dfs",
        "class": "D",
    },
    "E": {
        "run_id": "core_v2_generalization_local_deterministic_randomized_001",
        "dimension": "deterministic_vs_randomized",
        "class": "E",
    },
}


def git_commit() -> str:
    head = ROOT / ".git" / "HEAD"
    try:
        ref = head.read_text().strip()
        if ref.startswith("ref:"):
            return (ROOT / ".git" / ref.split()[1]).read_text().strip()
        return ref
    except Exception:
        return "UNKNOWN"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def iter_stripped(run_id: str):
    base = ROOT / "data" / "core_v2" / "stripped" / run_id
    for strip in STRIP_LEVELS:
        sdir = base / strip
        if not sdir.is_dir():
            continue
        for py in sorted(sdir.rglob("rep_*.py")):
            # .../strip/model/task/method/rep_n.py
            method = py.parent.name
            task_id = py.parent.parent.name
            model = py.parent.parent.parent.name
            m = re.match(r"rep_(\d+)\.py$", py.name)
            if not m:
                continue
            yield {
                "strip_level": strip,
                "model": model,
                "task_id": task_id,
                "pole": method,
                "rep": int(m.group(1)),
                "path": py,
            }


def load_tasks():
    root = project_root()
    return {
        "B": {t.task_id: t for t in load_quadrature_tasks(root / "data/core_v2/tasks/quadrature_tasks.json")},
        "C": {t.task_id: t for t in load_eager_lazy_tasks(root / "data/core_v2/tasks/eager_lazy_tasks.json")},
        "D": {t.task_id: t for t in load_bfs_dfs_tasks(root / "data/core_v2/tasks/bfs_dfs_tasks.json")},
        "E": {
            t.task_id: t
            for t in load_deterministic_randomized_tasks(
                root / "data/core_v2/tasks/deterministic_randomized_tasks.json"
            )
        },
    }


def oracle_and_detect(klass: str, code: str, task, pole: str):
    notes = ""
    try:
        if klass == "B":
            o = run_quadrature_behavioral_oracle(code, task)
            d = detect_quadrature(code)
            label = d.method
            evidence = d.evidence if hasattr(d, "evidence") else {}
        elif klass == "C":
            o = run_eager_lazy_behavioral_oracle(code, task)
            d = detect_eager_lazy(code, task=task, demand_pattern="partial")
            label = d.method
            evidence = d.evidence
        elif klass == "D":
            o = run_bfs_dfs_behavioral_oracle(code, task)
            d = detect_bfs_dfs(code, task)
            label = d.method
            evidence = d.evidence
        else:
            o = run_deterministic_randomized_behavioral_oracle(code, task)
            d = detect_deterministic_randomized(code, task)
            label = d.method
            evidence = d.evidence
        amb = label == "ambiguous"
        correct = (not amb) and (label == pole)
        return {
            "oracle_pass": bool(o.behavioral_pass and o.parsed),
            "oracle_error": getattr(o, "error", None) or "",
            "detector_label": label,
            "detector_correct": correct,
            "ambiguous": amb,
            "evidence": evidence,
            "execution_error": "",
            "notes": notes,
        }
    except Exception as exc:
        return {
            "oracle_pass": False,
            "oracle_error": f"exception:{type(exc).__name__}",
            "detector_label": "error",
            "detector_correct": False,
            "ambiguous": True,
            "evidence": {},
            "execution_error": str(exc)[:300],
            "notes": "exception_during_oracle_or_detect",
        }


# ----- Baseline S (source-only), rules frozen in phase2 plan -----

def baseline_s_B(code: str) -> str:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "ambiguous"
    text = ast.dump(tree)
    # Simpson often has coefficients 4 and 2 in alternating pattern; trapezoidal weights ends
    has4 = "Constant(value=4" in text or "Num(n=4" in text
    has2 = "Constant(value=2" in text or "Num(n=2" in text
    name_hit_s = bool(re.search(r"simpson|Simpson", code))
    name_hit_t = bool(re.search(r"trapezoid|Trapezoid", code))
    # Prefer structural cues over names when both present
    if has4 and has2:
        return "simpson"
    if has2 and not has4:
        return "trapezoidal"
    if name_hit_s and not name_hit_t:
        return "simpson"
    if name_hit_t and not name_hit_s:
        return "trapezoidal"
    return "ambiguous"


def _calls_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name):
                names.add(n.func.id)
            elif isinstance(n.func, ast.Attribute):
                names.add(n.func.attr)
    return names


def baseline_s_C(code: str) -> str:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "ambiguous"
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        init_calls: set[str] = set()
        getter_calls: set[str] = set()
        for item in node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            calls = _calls_names(item)
            # feature callback attrs typically feature_a_fn etc or stored callables
            feat = {c for c in calls if "feature" in c.lower() or c.endswith("_fn")}
            if item.name == "__init__":
                init_calls |= feat
            elif item.name.startswith("get_"):
                getter_calls |= feat
        if init_calls and not getter_calls:
            return "eager"
        if getter_calls and not init_calls:
            return "lazy"
        if init_calls and getter_calls:
            # both: weak cue — abstain rather than tune
            return "ambiguous"
    return "ambiguous"


def baseline_s_D(code: str) -> str:
    lower = code.lower()
    has_deque = "deque" in lower or "queue" in lower
    has_dfs = bool(re.search(r"\bdfs\b|depth.?first|recursion|stack", lower))
    has_bfs = bool(re.search(r"\bbfs\b|breadth.?first", lower))
    if has_deque and not has_dfs:
        return "bfs"
    if has_dfs and not has_deque:
        return "dfs"
    if has_bfs and not has_dfs:
        return "bfs"
    # AST: while + pop(0) vs pop()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "ambiguous"
    pop0 = False
    pop_end = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "pop":
            if n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == 0:
                pop0 = True
            elif not n.args:
                pop_end = True
    if pop0 and not pop_end:
        return "bfs"
    if pop_end and not pop0:
        return "dfs"
    return "ambiguous"


def baseline_s_E(code: str) -> str:
    if not re.search(r"\bItemProcessor\b", code):
        return "ambiguous"
    if re.search(r"\brandom\b|\bshuffle\b|\bsample\b|\brandrange\b|\brandint\b", code):
        return "randomized"
    return "deterministic"


def baseline_s(klass: str, code: str) -> str:
    return {"B": baseline_s_B, "C": baseline_s_C, "D": baseline_s_D, "E": baseline_s_E}[klass](code)


def baseline_t(klass: str, detector_label: str, evidence: dict, pole: str) -> str:
    if klass == "B":
        return detector_label if detector_label in {"trapezoidal", "simpson", "ambiguous"} else "ambiguous"
    if klass == "C":
        if is_genuine_eager(evidence):
            return "eager"
        if is_genuine_lazy(evidence):
            return "lazy"
        return "ambiguous"
    if klass == "D":
        if is_genuine_bfs(evidence):
            return "bfs"
        if is_genuine_dfs(evidence):
            return "dfs"
        return "ambiguous"
    if is_genuine_deterministic(evidence):
        return "deterministic"
    if is_genuine_randomized(evidence):
        return "randomized"
    return "ambiguous"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    commit = git_commit()
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.time()
    tasks = load_tasks()

    reoracle_rows: list[dict] = []
    baseline_rows: list[dict] = []

    # Cache raw oracle by (klass, model, task, pole, rep)
    raw_oracle_cache: dict[tuple, bool] = {}

    for klass, meta in RUNS.items():
        run_id = meta["run_id"]
        print(f"Processing class {klass} {run_id}...", flush=True)
        arts = list(iter_stripped(run_id))
        # First pass: raw oracle cache
        for art in arts:
            if art["strip_level"] != "raw":
                continue
            code = art["path"].read_text(encoding="utf-8", errors="replace")
            task = tasks[klass].get(art["task_id"])
            if task is None:
                continue
            res = oracle_and_detect(klass, code, task, art["pole"])
            key = (klass, art["model"], art["task_id"], art["pole"], art["rep"])
            raw_oracle_cache[key] = res["oracle_pass"]

        for art in arts:
            task = tasks[klass].get(art["task_id"])
            code = art["path"].read_text(encoding="utf-8", errors="replace")
            key = (klass, art["model"], art["task_id"], art["pole"], art["rep"])
            if task is None:
                row = {
                    "run_id": run_id,
                    "class": klass,
                    "dimension": meta["dimension"],
                    "model": art["model"],
                    "task_id": art["task_id"],
                    "pole": art["pole"],
                    "rep": art["rep"],
                    "strip_level": art["strip_level"],
                    "raw_oracle_pass": "",
                    "stripped_oracle_pass": False,
                    "detector_label": "error",
                    "requested_pole": art["pole"],
                    "detector_correct": False,
                    "ambiguous": True,
                    "execution_error": "missing_task",
                    "notes": "task_id_not_in_task_file",
                }
                reoracle_rows.append(row)
                continue
            res = oracle_and_detect(klass, code, task, art["pole"])
            raw_pass = raw_oracle_cache.get(key, False)
            row = {
                "run_id": run_id,
                "class": klass,
                "dimension": meta["dimension"],
                "model": art["model"],
                "task_id": art["task_id"],
                "pole": art["pole"],
                "rep": art["rep"],
                "strip_level": art["strip_level"],
                "raw_oracle_pass": raw_pass,
                "stripped_oracle_pass": res["oracle_pass"],
                "detector_label": res["detector_label"],
                "requested_pole": art["pole"],
                "detector_correct": res["detector_correct"],
                "ambiguous": res["ambiguous"],
                "execution_error": res["execution_error"] or res["oracle_error"],
                "notes": res["notes"],
            }
            reoracle_rows.append(row)

            # Baselines on same artifact (all strip levels for S; T uses evidence)
            for bname, pred, info, rule_source in [
                (
                    "S_source_only",
                    baseline_s(klass, code),
                    "source_text_ast_only",
                    "phase2_offline_analysis_plan.md#baseline-s",
                ),
                (
                    "T_trace_direct",
                    baseline_t(klass, res["detector_label"], res["evidence"], art["pole"]),
                    "runtime_trace_evidence_fields_only",
                    "phase2_offline_analysis_plan.md#baseline-t",
                ),
                (
                    "B_behavior_only",
                    "ambiguous",
                    "behavioral_oracle_pass_bit_only",
                    "phase2_offline_analysis_plan.md#baseline-b",
                ),
            ]:
                abstain = pred == "ambiguous"
                correct = (not abstain) and (pred == art["pole"])
                baseline_rows.append(
                    {
                        "baseline": bname,
                        "class": klass,
                        "model": art["model"],
                        "strip_level": art["strip_level"],
                        "task_id": art["task_id"],
                        "pole": art["pole"],
                        "rep": art["rep"],
                        "prediction": pred,
                        "correct": correct,
                        "abstain": abstain,
                        "raw_oracle_pass": raw_pass,
                        "stripped_oracle_pass": res["oracle_pass"],
                        "information_used": info,
                        "rule_source": rule_source,
                        "outcome_tuned": False,
                    }
                )

    # Summaries
    summary_rows = []
    # group by class,pole,model,strip
    groups: dict[tuple, list] = defaultdict(list)
    for r in reoracle_rows:
        groups[(r["class"], r["pole"], r["model"], r["strip_level"])].append(r)
    for key, rs in sorted(groups.items()):
        klass, pole, model, strip = key
        n = len(rs)
        raw_valid = sum(1 for r in rs if r["raw_oracle_pass"] is True)
        strip_valid = sum(1 for r in rs if r["stripped_oracle_pass"] is True)
        strip_fail_from_raw = sum(
            1 for r in rs if r["raw_oracle_pass"] is True and r["stripped_oracle_pass"] is not True
        )
        det_on_raw_valid = [r for r in rs if r["raw_oracle_pass"] is True]
        det_on_pres = [r for r in rs if r["raw_oracle_pass"] is True and r["stripped_oracle_pass"] is True]
        def acc(xs):
            if not xs:
                return ""
            return f"{sum(1 for r in xs if r['detector_correct']) / len(xs):.4f}"
        def amb(xs):
            if not xs:
                return ""
            return f"{sum(1 for r in xs if r['ambiguous']) / len(xs):.4f}"
        summary_rows.append(
            {
                "class": klass,
                "pole": pole,
                "model": model,
                "strip_level": strip,
                "n": n,
                "raw_valid_n": raw_valid,
                "stripped_valid_n": strip_valid,
                "stripped_valid_rate": f"{strip_valid / n:.4f}" if n else "",
                "detector_accuracy_on_raw_valid": acc(det_on_raw_valid),
                "detector_accuracy_on_behavior_preserving": acc(det_on_pres),
                "ambiguous_rate_on_raw_valid": amb(det_on_raw_valid),
                "strip_induced_behavioral_failures": strip_fail_from_raw,
            }
        )

    # Robustness decision per class × strip
    rob_rows = []
    for klass in ["B", "C", "D", "E"]:
        for strip in STRIP_LEVELS:
            rs = [r for r in reoracle_rows if r["class"] == klass and r["strip_level"] == strip]
            n = len(rs)
            raw_v = [r for r in rs if r["raw_oracle_pass"] is True]
            preserved = [r for r in raw_v if r["stripped_oracle_pass"] is True]
            bp_rate = len(preserved) / len(raw_v) if raw_v else 0.0
            det_ok = sum(1 for r in preserved if r["detector_correct"])
            det_rate = det_ok / len(preserved) if preserved else 0.0
            if strip == "raw":
                status = "SUPPORTED"
                wording = "raw baseline: oracle and detector on unstripped artifacts"
            elif bp_rate >= 0.999 and det_rate >= 0.999:
                status = "SUPPORTED"
                wording = "behavior-preserving stability under this predefined source transformation"
            elif bp_rate >= 0.999 and det_rate >= 0.85:
                status = "PARTIALLY SUPPORTED"
                wording = "behavior preserved; detector stability incomplete under this transform"
            elif bp_rate < 0.999 and det_rate >= 0.85:
                status = "PARTIALLY SUPPORTED"
                wording = "detector labels often stable, but strip induced behavioral failures — not semantics-preserving"
            else:
                status = "NOT SUPPORTED"
                wording = "neither full behavior preservation nor conditional detector stability"
            # Original manuscript claimed stripping robustness broadly
            if strip == "format_normalized":
                if status == "SUPPORTED":
                    orig = "SUPPORTED"
                elif status == "PARTIALLY SUPPORTED":
                    orig = "PARTIALLY SUPPORTED"
                else:
                    orig = "NOT SUPPORTED"
            else:
                orig = status
            rob_rows.append(
                {
                    "class": klass,
                    "strip_level": strip,
                    "n": n,
                    "behavior_preserved_n": len(preserved),
                    "behavior_preserved_rate": f"{bp_rate:.4f}",
                    "detector_correct_n": det_ok,
                    "detector_correct_rate_conditional": f"{det_rate:.4f}",
                    "original_claim_status": orig,
                    "recommended_wording": wording,
                }
            )

    # Aggregate baseline metrics
    base_agg = []
    bg: dict[tuple, list] = defaultdict(list)
    for r in baseline_rows:
        # evaluate accuracy on raw-valid artifacts only for fairness with paper metrics
        if r["raw_oracle_pass"] is not True:
            continue
        bg[(r["baseline"], r["class"], r["model"], r["strip_level"])].append(r)
    for key, rs in sorted(bg.items()):
        bname, klass, model, strip = key
        n = len(rs)
        covered = [r for r in rs if not r["abstain"]]
        cov = len(covered) / n if n else 0
        acc = sum(1 for r in covered if r["correct"]) / len(covered) if covered else 0
        amb = sum(1 for r in rs if r["abstain"]) / n if n else 0
        base_agg.append(
            {
                "baseline": bname,
                "class": klass,
                "model": model,
                "strip_level": strip,
                "n": n,
                "coverage": f"{cov:.4f}",
                "accuracy": f"{acc:.4f}" if covered else "",
                "ambiguous_or_abstain_rate": f"{amb:.4f}",
                "information_used": rs[0]["information_used"],
                "rule_source": rs[0]["rule_source"],
                "outcome_tuned": False,
                "notes": "accuracy among non-abstain; n=raw-oracle-valid artifacts at strip level",
            }
        )

    # Write outputs
    write_csv(
        OUT / "strip_reoracle_results.csv",
        reoracle_rows,
        [
            "run_id",
            "class",
            "dimension",
            "model",
            "task_id",
            "pole",
            "rep",
            "strip_level",
            "raw_oracle_pass",
            "stripped_oracle_pass",
            "detector_label",
            "requested_pole",
            "detector_correct",
            "ambiguous",
            "execution_error",
            "notes",
        ],
    )
    write_csv(
        OUT / "strip_reoracle_summary.csv",
        summary_rows,
        [
            "class",
            "pole",
            "model",
            "strip_level",
            "n",
            "raw_valid_n",
            "stripped_valid_n",
            "stripped_valid_rate",
            "detector_accuracy_on_raw_valid",
            "detector_accuracy_on_behavior_preserving",
            "ambiguous_rate_on_raw_valid",
            "strip_induced_behavioral_failures",
        ],
    )
    write_csv(
        OUT / "robustness_reoracle_decision.csv",
        rob_rows,
        [
            "class",
            "strip_level",
            "n",
            "behavior_preserved_n",
            "behavior_preserved_rate",
            "detector_correct_n",
            "detector_correct_rate_conditional",
            "original_claim_status",
            "recommended_wording",
        ],
    )
    write_csv(
        OUT / "offline_baseline_results.csv",
        base_agg,
        [
            "baseline",
            "class",
            "model",
            "strip_level",
            "n",
            "coverage",
            "accuracy",
            "ambiguous_or_abstain_rate",
            "information_used",
            "rule_source",
            "outcome_tuned",
            "notes",
        ],
    )
    write_csv(
        OUT / "offline_baseline_per_artifact.csv",
        baseline_rows,
        list(baseline_rows[0].keys()) if baseline_rows else [],
    )

    elapsed = time.time() - t0
    prov = {
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(elapsed, 2),
        "git_commit": commit,
        "script": "scripts/phase2_offline_validation.py",
        "plan": "paper/audit/phase2_offline_analysis_plan.md",
        "n_reoracle_rows": len(reoracle_rows),
        "n_baseline_artifact_rows": len(baseline_rows),
        "model_executions": 0,
        "paid_api_calls": 0,
        "classes": list(RUNS.keys()),
        "strip_levels": STRIP_LEVELS,
        "output_dir": str(OUT),
    }
    (OUT / "provenance.json").write_text(json.dumps(prov, indent=2), encoding="utf-8")

    # Copy to paper audit
    PAPER_AUDIT.mkdir(parents=True, exist_ok=True)
    for name in [
        "strip_reoracle_results.csv",
        "strip_reoracle_summary.csv",
        "robustness_reoracle_decision.csv",
        "offline_baseline_results.csv",
    ]:
        src = OUT / name
        dst = PAPER_AUDIT / name
        dst.write_bytes(src.read_bytes())

    # Global strip-failure counts
    strip_induced = sum(
        1
        for r in reoracle_rows
        if r["raw_oracle_pass"] is True and r["stripped_oracle_pass"] is not True
    )
    print(json.dumps({"ok": True, "rows": len(reoracle_rows), "strip_induced_failures": strip_induced, **prov}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
