from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.commercial_workflow import import_outcomes_csv
from buyermoment.ledger import ExperimentLedger


def main() -> None:
    parser = argparse.ArgumentParser(description="Import manually exported campaign outcomes into the portable Phase 7 ledger.")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--ledger", type=Path, default=Path("data/phase7/experiment_ledger.sqlite3"))
    args = parser.parse_args()
    ledger = ExperimentLedger(args.ledger)
    imported = []
    for outcome in import_outcomes_csv(args.csv):
        imported.append(ledger.save_outcome(outcome).model_dump(mode="json"))
    print(json.dumps({"imported": len(imported), "lineage": imported}, indent=2))


if __name__ == "__main__":
    main()
