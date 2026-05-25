"""
Evaluate precision/recall/F1 for each dataset by comparing
expected checks (derived from the data contract) against
generated checks (parsed from the committed GX suite JSON).

Usage:
    python evaluate.py                  # all three datasets
    python evaluate.py raddb            # single dataset
    python evaluate.py raddb billing    # subset
"""
import sys
import os
from pathlib import Path

from qa_agent.langgraph_src.evaluator import evaluate_run

DATASETS = ["raddb", "billing", "bsadb"]

CONTRACT_PATH = "contracts/contract.{dataset}.yaml"
SUITE_PATH = "expectations/{dataset}_suite.json"
SANDBOX_GLOB = "artifacts/sandbox/{dataset}.*.report.json"


def _execution_passed(dataset: str) -> bool:
    """True if at least one sandbox report exists for this dataset."""
    import glob
    return bool(glob.glob(SANDBOX_GLOB.format(dataset=dataset)))


def evaluate_dataset(dataset: str) -> dict | None:
    contract_path = CONTRACT_PATH.format(dataset=dataset)
    suite_path = SUITE_PATH.format(dataset=dataset)

    if not Path(contract_path).exists():
        print(f"  [skip] contract not found: {contract_path}")
        return None
    if not Path(suite_path).exists():
        print(f"  [skip] suite JSON not found: {suite_path}  (run qa_agent first)")
        return None

    passed = _execution_passed(dataset)
    return evaluate_run(contract_path, suite_path, execution_passed=passed)


def print_table(results: dict[str, dict]):
    cols = ["dataset", "precision", "recall", "f1", "expected", "generated", "tp", "fp", "fn", "exec"]
    widths = [10, 10, 8, 8, 9, 10, 5, 5, 5, 6]
    header = "  ".join(c.ljust(w) for c, w in zip(cols, widths))
    sep = "  ".join("-" * w for w in widths)

    print("\n" + header)
    print(sep)
    for dataset, m in results.items():
        row = [
            dataset,
            f"{m['precision']:.3f}",
            f"{m['recall']:.3f}",
            f"{m['f1']:.3f}",
            str(m["expected_count"]),
            str(m["generated_count"]),
            str(len(m["tp"])),
            str(len(m["fp"])),
            str(len(m["fn"])),
            "yes" if m["execution_passed"] else "no",
        ]
        print("  ".join(v.ljust(w) for v, w in zip(row, widths)))

    print()

    for dataset, m in results.items():
        if m["fn"]:
            print(f"{dataset} missing checks (FN):")
            for field, check_type in sorted(m["fn"]):
                print(f"  - {field}: {check_type}")
        if m["fp"]:
            print(f"{dataset} extra checks (FP):")
            for field, check_type in sorted(m["fp"]):
                print(f"  + {field}: {check_type}")
        if m["fn"] or m["fp"]:
            print()


def main():
    datasets = sys.argv[1:] if sys.argv[1:] else DATASETS
    results = {}

    for dataset in datasets:
        print(f"Evaluating {dataset}...")
        m = evaluate_dataset(dataset)
        if m is not None:
            results[dataset] = m

    if results:
        print_table(results)
    else:
        print("No results — run qa_agent for at least one dataset first.")


if __name__ == "__main__":
    main()
