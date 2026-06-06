"""
Evaluator: measures coverage of generated GX rules against a data contract.

Ground truth  = (field, check_type) pairs derived from the contract.
CLI coverage  = expectations without check_id in meta.
LLM coverage  = expectations with check_id in meta.
"""

import json
import yaml

CANONICAL_TYPES = {"not_null", "unique", "domain", "range", "format", "freshness", "foreign_key"}

GX_TO_CHECK_TYPE = {
    "expect_column_values_to_not_be_null": "not_null",
    "expect_column_values_to_be_unique": "unique",
    "expect_column_values_to_be_between": "range",
    "expect_column_values_to_be_in_set": "domain",
    "expect_column_distinct_values_to_be_in_set": "domain",
    "expect_column_distinct_values_to_equal_set": "domain",
    "expect_column_values_to_match_regex": "format",
    "expect_column_values_to_match_strftime_format": "format",
    "expect_column_values_to_match_like_pattern": "format",
}

_TYPE_KEYWORDS = [
    (["null", "missing", "mandatory", "required"], "not_null"),
    (["unique", "dup"], "unique"),
    (["valid", "invalid", "allowed", "domain", "lookup", "member", "accept"], "domain"),
    (["format", "regex", "pattern"], "format"),
    (["fresh", "stale", "latency", "older than"], "freshness"),
    (["foreign", "reference", "referential", "integrity"], "foreign_key"),
    (["range", "min", "max", "less than", "greater than", "between", "percentile",
      "quantile", "later", "before", "after", "earlier", "exceed"], "range"),
]


def _infer_type(text: str) -> str:
    text = text.lower()
    for keywords, check_type in _TYPE_KEYWORDS:
        if any(k in text for k in keywords):
            return check_type
    return "custom"


def extract_expected(contract: dict) -> set[tuple[str, str]]:
    """Derive expected (field, check_type) pairs from a data contract."""
    checks: set[tuple[str, str]] = set()

    for _model, model_def in (contract.get("models") or {}).items():
        if not isinstance(model_def, dict):
            continue

        pk_fields = model_def.get("primaryKey") or []
        if isinstance(pk_fields, str):
            pk_fields = [pk_fields]

        for field, field_def in (model_def.get("fields") or {}).items():
            if not isinstance(field_def, dict):
                continue

            is_pk = field_def.get("primaryKey", False) or field in pk_fields
            if field_def.get("required") or is_pk:
                checks.add((field, "not_null"))
            if field_def.get("unique") or is_pk:
                checks.add((field, "unique"))
            if field_def.get("enum") is not None:
                checks.add((field, "domain"))
            if field_def.get("pattern") is not None:
                checks.add((field, "format"))
            if "minimum" in field_def or "maximum" in field_def:
                checks.add((field, "range"))

            for q in field_def.get("quality") or []:
                if not isinstance(q, dict):
                    continue
                metric = q.get("metric", "")
                qtype = q.get("type", "")
                if metric == "nullValues":
                    checks.add((field, "not_null"))
                elif metric == "invalidValues":
                    checks.add((field, "domain"))
                elif qtype in ("text", "sql", "custom"):
                    desc = q.get("description", "") + " " + q.get("query", "")
                    checks.add((field, _infer_type(desc)))

        for q in model_def.get("quality") or []:
            if not isinstance(q, dict):
                continue
            field = q.get("field", "")
            if not field:
                continue
            rule = q.get("rule", "")
            if rule == "unique":
                checks.add((field, "unique"))
            elif rule == "accepted_values":
                checks.add((field, "domain"))
            elif rule == "regex":
                checks.add((field, "format"))
            elif rule == "referential_integrity":
                checks.add((field, "foreign_key"))
            elif rule == "custom":
                desc = q.get("description", "") + " " + q.get("expression", "")
                checks.add((field, _infer_type(desc)))

    sla = contract.get("servicelevels") or contract.get("serviceLevel") or {}
    freshness = sla.get("freshness") or {}
    if isinstance(freshness, dict) and freshness:
        ts_field = freshness.get("timestampField", "")
        field = ts_field.split(".")[-1] if ts_field else "__freshness__"
        checks.add((field, "freshness"))

    return checks


def extract_cli(suite_path: str) -> set[tuple[str, str]]:
    """Return (field, check_type) pairs from CLI-generated expectations (no check_id)."""
    with open(suite_path) as f:
        suite = json.load(f)

    covered: set[tuple[str, str]] = set()
    for exp in suite.get("expectations", []):
        if exp.get("meta", {}).get("check_id"):
            continue
        check_type = GX_TO_CHECK_TYPE.get(exp.get("type", ""))
        if not check_type:
            continue
        column = exp.get("kwargs", {}).get("column")
        if column:
            covered.add((column, check_type))
    return covered


def _parse_check_id(check_id: str) -> tuple[str, str] | None:
    """Parse 'model:check_type:field' → (field, check_type), with fallbacks."""
    parts = check_id.split(":")
    if len(parts) < 2:
        return None
    if len(parts) >= 3:
        if parts[1] in CANONICAL_TYPES:
            return (parts[2], parts[1])
        if parts[2] in CANONICAL_TYPES:
            return (parts[1], parts[2])
        return (parts[2], _infer_type(parts[1]))
    return (parts[1], "unknown")


def extract_llm(suite_path: str) -> set[tuple[str, str]]:
    """Return (field, check_type) pairs from LLM-generated expectations (have check_id)."""
    with open(suite_path) as f:
        suite = json.load(f)

    covered: set[tuple[str, str]] = set()
    for exp in suite.get("expectations", []):
        check_id = exp.get("meta", {}).get("check_id", "")
        if not check_id:
            continue
        result = _parse_check_id(check_id)
        if result:
            covered.add(result)
    return covered


def extract_execution(report_path: str) -> dict:
    """
    Parse a sandbox report JSON and return executed/error counts split by CLI vs LLM.
    An expectation is "executed" when it ran without raising an exception,
    regardless of whether the data passed or failed the rule.
    """
    with open(report_path) as f:
        report = json.load(f)

    counts = {"cli": {"executed": 0, "error": 0}, "llm": {"executed": 0, "error": 0}}
    for res in report.get("results", []):
        has_check_id = bool(res.get("expectation_config", {}).get("meta", {}).get("check_id"))
        key = "llm" if has_check_id else "cli"
        raised = res.get("exception_info", {}).get("raised_exception", False)
        if raised:
            counts[key]["error"] += 1
        else:
            counts[key]["executed"] += 1
    return counts


def _metrics(tp: set, fp: set, fn: set) -> dict:
    precision = len(tp) / (len(tp) + len(fp)) if (tp or fp) else 0.0
    recall    = len(tp) / (len(tp) + len(fn)) if (tp or fn) else 0.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "tp": sorted(tp), "fp": sorted(fp), "fn": sorted(fn),
        "precision": round(precision, 3),
        "recall":    round(recall, 3),
        "f1":        round(f1, 3),
    }


def coverage_report(contract_path: str, suite_path: str, report_path: str | None = None) -> dict:
    with open(contract_path) as f:
        contract = yaml.safe_load(f)

    expected = extract_expected(contract)
    cli      = extract_cli(suite_path)
    llm      = extract_llm(suite_path)
    combined = cli | llm

    cli_tp = cli & expected
    cli_fp = cli - expected
    cli_fn = expected - cli

    comb_tp = combined & expected
    comb_fp = combined - expected
    comb_fn = expected - combined

    return {
        "total_expected": len(expected),
        "cli":      _metrics(cli_tp, cli_fp, cli_fn),
        "combined": _metrics(comb_tp, comb_fp, comb_fn),
        "llm_delta": {
            "tp_added": sorted(comb_tp - cli_tp),
            "fp":       sorted(llm - expected),
        },
        "execution": extract_execution(report_path) if report_path else None,
    }


def print_report(dataset: str, r: dict) -> None:
    W = 60
    print(f"\n{'=' * W}")
    print(f"  {dataset}   (expected checks: {r['total_expected']})")
    print(f"{'=' * W}")

    # Summary table
    hdr = f"  {'':<12}  {'Precision':>10}  {'Recall':>8}  {'F1':>8}  {'TP':>4}  {'FP':>4}  {'FN':>4}"
    print(hdr)
    print(f"  {'-'*12}  {'-'*10}  {'-'*8}  {'-'*8}  {'-'*4}  {'-'*4}  {'-'*4}")
    for label, key in [("CLI", "cli"), ("CLI + LLM", "combined")]:
        m = r[key]
        print(f"  {label:<12}  {m['precision']:>10.3f}  {m['recall']:>8.3f}  {m['f1']:>8.3f}"
              f"  {len(m['tp']):>4}  {len(m['fp']):>4}  {len(m['fn']):>4}")

    d = r["llm_delta"]
    print(f"\n  LLM contribution : +{len(d['tp_added'])} TP,  {len(d['fp'])} FP (hallucinations)")

    if r["execution"]:
        e = r["execution"]
        rows = [
            ("CLI",      e["cli"]),
            ("LLM",      e["llm"]),
            ("Combined", {"executed": e["cli"]["executed"] + e["llm"]["executed"],
                          "error":    e["cli"]["error"]    + e["llm"]["error"]}),
        ]
        print(f"\n  Execution results (exception-free):")
        print(f"  {'':<12}  {'Total':>8}  {'Executed':>10}  {'Errors':>8}  {'Exec%':>7}")
        print(f"  {'-'*12}  {'-'*8}  {'-'*10}  {'-'*8}  {'-'*7}")
        for label, c in rows:
            total = c["executed"] + c["error"]
            pct   = c["executed"] / total * 100 if total else 0.0
            print(f"  {label:<12}  {total:>8}  {c['executed']:>10}  {c['error']:>8}  {pct:>6.1f}%")

    if r["cli"]["tp"]:
        print("\n  CLI TP:")
        for field, ctype in r["cli"]["tp"]:
            print(f"    ✓  {field:30s}  {ctype}")

    if d["tp_added"]:
        print("\n  LLM TP (added on top of CLI):")
        for field, ctype in d["tp_added"]:
            print(f"    +  {field:30s}  {ctype}")

    if d["fp"]:
        print("\n  FP — hallucinations (not in contract):")
        for field, ctype in d["fp"]:
            print(f"    ~  {field:30s}  {ctype}")

    if r["combined"]["fn"]:
        print("\n  FN — missed by both CLI and LLM:")
        for field, ctype in r["combined"]["fn"]:
            print(f"    ✗  {field:30s}  {ctype}")
