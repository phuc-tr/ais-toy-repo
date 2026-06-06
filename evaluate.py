"""
Run coverage evaluation for all (or selected) datasets.

Usage:
    python evaluate.py                  # all three datasets
    python evaluate.py raddb            # single dataset
    python evaluate.py raddb billing    # subset
"""
import sys
from pathlib import Path

from evaluator import coverage_report, print_report

DATASETS = ["raddb", "billing", "bsadb"]
CONTRACT_PATH = "contracts/contract.{dataset}.yaml"
SUITE_PATH    = "expectations/{dataset}_suite.json"
REPORT_GLOB   = "artifacts/sandbox/{dataset}.*.report.json"


def _latest_report(dataset: str) -> str | None:
    import glob
    files = sorted(glob.glob(REPORT_GLOB.format(dataset=dataset)))
    return files[-1] if files else None


def main():
    datasets = sys.argv[1:] if sys.argv[1:] else DATASETS

    for dataset in datasets:
        contract    = CONTRACT_PATH.format(dataset=dataset)
        suite       = SUITE_PATH.format(dataset=dataset)
        report_path = _latest_report(dataset)

        if not Path(contract).exists():
            print(f"\n[skip] contract not found: {contract}")
            continue
        if not Path(suite).exists():
            print(f"\n[skip] suite not found: {suite}")
            continue

        result = coverage_report(contract, suite, report_path)
        print_report(dataset, result)


if __name__ == "__main__":
    main()
