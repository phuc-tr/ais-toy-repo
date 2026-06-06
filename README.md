# Agentic Data Quality Pipeline — Report

## Overview

This pipeline automatically generates and executes data quality checks from data contracts, combining deterministic CLI tooling with LLM-driven reasoning to achieve broad coverage across structurally simple and semantically complex rules alike.

---

## Pipeline Architecture

```
Data Contract (YAML)
        │
        ▼
┌──────────────────┐
│  Stage 0         │  Sampler: query DB → Parquet + profile JSON
│  Sampling        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Stage 1         │  datacontract CLI → GX suite JSON
│  CLI Export      │  (structural checks only)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Stage 2         │  Gap classifier: find rules the CLI missed
│  Gap Analysis    │
└────────┬─────────┘
         │  (if gaps exist)
         ▼
┌──────────────────┐
│  Stage 3         │  LLM coder → append expectations to suite
│  LLM Generation  │  (with self-healing retry loop)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Stage 4         │  GX validation on sample → report + GitHub PR
│  Validate & PR   │
└──────────────────┘
```

**Stage 0 — Sampling** connects to the MySQL database declared in the contract's `servers` block and queries up to 100 rows per table. Results are written as Parquet files under `artifacts/samples/`. A column-level profile (null rate, distinct ratio, numeric percentiles) is saved to `artifacts/profiles/` and fed to the LLM as context.

**Stage 1 — CLI Export** invokes the `datacontract` CLI against the contract YAML to generate a GX suite JSON. The CLI handles only rules structurally encoded in field properties (`required`, `unique`, `minimum`/`maximum`, `enum`, `pattern`). It cannot express `text`, `sql`, or `custom` quality blocks, freshness SLAs, or referential integrity rules.

**Stage 2 — Gap Analysis** parses the generated suite to determine which `(field, check_type)` pairs are already covered, then emits an `unresolved` list for everything the CLI missed. Each unresolved item is serialised as a YAML fragment that becomes the LLM prompt input.

**Stage 3 — LLM Generation** receives the unresolved rules and schema metadata. It appends expectations to the existing suite and tags each one with `meta={"check_id": "<model>:<check_type>:<field>"}` — the tag the evaluator uses to distinguish LLM-generated from CLI-generated checks. A self-healing retry loop (up to 5 attempts) feeds Python tracebacks back to the LLM to fix execution errors.

**Stage 4 — Validation & PR** validates all table samples against the GX suite, writes the full report to `artifacts/sandbox/{dataset}.{run_id}.report.json`, commits the results to a `bot/{run_id}` branch, and opens a draft GitHub PR.

---

## Worked Example (raddb)

### Stage 1 — What the CLI can generate

Given this contract snippet:

```yaml
models:
  radacct:
    fields:
      radacctid:
        type: integer
        required: true
        unique: true          # ← CLI picks this up

      nasporttype:
        type: string
        quality:
          - type: library
            metric: invalidValues
            arguments:
              validValues: [Virtual, ISDN]   # ← CLI picks this up

      nasportid:
        type: string
        quality:
          - type: text
            description: Must follow format "Uniq-Sess-ID<id>" where <id> are numerics.
            # ← CLI cannot express free-text rules — skipped

      acctsessiontime:
        type: integer
        quality:
          - type: sql
            description: 95% of acctsessiontime should be less than 30000 seconds.
            query: SELECT quantile(acctsessiontime, 0.95) FROM radacct
            # ← CLI cannot express SQL rules — skipped

servicelevels:
  freshness:
    description: Data should be no older than 25 hours.
    timestampField: radacct.acctstarttime
    # ← CLI cannot express freshness SLAs — skipped
```

The CLI produces only the checks it can express structurally:

```json
{ "type": "expect_column_values_to_be_of_type",  "kwargs": { "column": "radacctid", "type_": "int32" }, "meta": {} }
{ "type": "expect_column_values_to_be_unique",    "kwargs": { "column": "radacctid" },                  "meta": {} }
{ "type": "expect_column_values_to_be_of_type",  "kwargs": { "column": "nasporttype", "type_": "str" }, "meta": {} }
```

`nasporttype`'s domain check, `nasportid`'s format rule, `acctsessiontime`'s percentile rule, and the freshness SLA produce no expectations — they become gaps.

Note: the CLI translates `required: true` into a type check, not a null check. `not_null` for required fields is therefore always a gap passed to the LLM.

---

### Stage 2 — Gaps passed to the LLM

The gap classifier compares the contract rules against what the CLI covered and emits the unresolved items as a YAML fragment:

```yaml
radacct.radacctid:
  not_null: "radacctid is required (primaryKey)"

radacct.nasportid:
  format: 'Must follow format "Uniq-Sess-ID<id>" where <id> are numerics.'

radacct.nasporttype:
  domain: "Ensure nasporttype uses valid port types: [Virtual, ISDN]"

radacct.acctsessiontime:
  range: "95% of acctsessiontime should be less than 30000 seconds."

radacct.acctstarttime:
  freshness: "Data should be no older than 25 hours."
```

The LLM receives this fragment along with the data profile and generates GX expectations for each item, tagging every one with a `check_id` so the evaluator can attribute it:

```json
{ "type": "expect_column_values_to_not_be_null",       "kwargs": { "column": "radacctid" },                                  "meta": { "check_id": "radacct:not_null:radacctid" } }
{ "type": "expect_column_values_to_match_regex",        "kwargs": { "column": "nasportid", "regex": "^Uniq-Sess-ID\\d+$" },  "meta": { "check_id": "radacct:format:nasportid" } }
{ "type": "expect_column_values_to_be_in_set",          "kwargs": { "column": "nasporttype", "value_set": ["Virtual","ISDN"] }, "meta": { "check_id": "radacct:domain:nasporttype" } }
{ "type": "expect_column_quantile_values_to_be_between","kwargs": { "column": "acctsessiontime", ... },                       "meta": { "check_id": "radacct:range:acctsessiontime" } }
{ "type": "expect_column_values_to_be_between",         "kwargs": { "column": "acctstarttime", ... },                         "meta": { "check_id": "radacct:freshness:acctstarttime" } }
```

---

## Evaluation Methodology

Evaluation compares **expected checks** (derived from the data contract) against **generated checks** (parsed from the committed suite JSON).

| Source | How checks are identified |
|---|---|
| Contract (expected) | Field properties: `required`→`not_null`, `unique`→`unique`, `min/max`→`range`, `enum`→`domain`, `pattern`→`format`; field-level quality blocks (type inferred from description); model-level quality rules; freshness SLAs |
| CLI suite | Expectation type + `column` kwarg; expectations with a `check_id` in meta are skipped |
| LLM suite | `meta.check_id` tag in the format `<model>:<check_type>:<field>` |

For `text`/`sql`/`custom` quality blocks, the canonical check type is inferred from the rule description using keyword matching (e.g. "must not be null" → `not_null`, "must be a valid value from" → `domain`, "must be on or after" → `range`).

```
precision  = TP / (TP + FP)
recall     = TP / (TP + FN)
F1         = 2 × precision × recall / (precision + recall)

TP = expected ∩ generated
FP = generated − expected   (hallucinations)
FN = expected − generated   (missed rules)
```

---

## Datasets

| Dataset | Domain | Tables | Expected checks |
|---|---|---|---|
| `raddb` | RADIUS Accounting | 1 | 13 |
| `billing` | ISP Billing Platform | 12 | 56 |
| `bsadb` | Support Ticketing | 8 | 23 |

---

## Results

### Coverage (precision / recall / F1)

| Dataset | Mode | Precision | Recall | F1 | TP | FP | FN |
|---|---|---|---|---|---|---|---|
| raddb | CLI | 1.000 | 0.154 | 0.267 | 2 | 0 | 11 |
| raddb | CLI + LLM | 1.000 | 0.769 | 0.870 | 10 | 0 | 3 |
| billing | CLI | 1.000 | 0.268 | 0.423 | 15 | 0 | 41 |
| billing | CLI + LLM | 0.964 | 0.482 | 0.643 | 27 | 1 | 29 |
| bsadb | CLI | 1.000 | 0.261 | 0.414 | 6 | 0 | 17 |
| bsadb | CLI + LLM | 0.929 | 0.565 | 0.703 | 13 | 1 | 10 |

### LLM contribution

| Dataset | LLM TP added | LLM FP (hallucinations) | F1 lift |
|---|---|---|---|
| raddb | +8 | 0 | +0.603 |
| billing | +12 | 1 | +0.220 |
| bsadb | +7 | 1 | +0.289 |

### Execution (exception-free rate, latest run)

| Dataset | CLI expectations | CLI exec% | LLM expectations | LLM exec% |
|---|---|---|---|---|
| raddb | 28 | 100.0% | 8 | 100.0% |
| billing | 231 | 100.0% | 15 | 100.0% |
| bsadb | 66 | 100.0% | 8 | 100.0% |

All generated expectations ran without exceptions across every dataset.

---

## Analysis

**CLI always achieves perfect precision (1.000)** — because it generates directly from contract field properties, it never produces checks that contradict the contract. However, recall is consistently low (0.154–0.268). The CLI only covers structural field attributes; it cannot express quality rules described in free text, SQL, or custom expressions, nor freshness SLAs.

**LLM augmentation improves F1 substantially across all datasets** — +0.603 on raddb, +0.220 on billing, +0.289 on bsadb — recovering the semantic rules the CLI cannot generate. Precision stays near-perfect (0.929–1.000) with at most 1 hallucination per dataset.

**Remaining FN across all datasets** are primarily: `required` fields that the CLI maps to type checks instead of null checks (a CLI limitation), referential integrity rules that have no native GX expectation type, and the billing freshness SLA which has no `timestampField` in the contract.
