from __future__ import annotations

import json
from pathlib import Path

from buyermoment.evidence_grounding import assess_claim
from buyermoment.models import Evidence


CASES = [
    ("ContextFit records budget and product fit.", ["ContextFit records budget and product fit."], "SUPPORTED"),
    ("The product has a verified $99 price and SOC 2 support.", ["The product has a verified $99 price."], "PARTIAL"),
    ("BuyerMoment has proven ROI.", ["The repository has no campaign outcomes or ROI claims."], "UNSUPPORTED"),
    ("The experiment requires human approval.", ["Human approval remains mandatory for generated experiments."], "SUPPORTED"),
    ("The service ships to Canada tomorrow.", ["The service has a US landing page."], "UNSUPPORTED"),
    ("The business has public pricing and Slack integration.", ["The product documents Slack integration."], "PARTIAL"),
]


def main() -> None:
    rows = []
    for index, (claim, texts, expected) in enumerate(CASES, start=1):
        evidence = [Evidence(id=f"grounding:{index}:{i}", kind="observed", text=text, source="phase8_control") for i, text in enumerate(texts)]
        result = assess_claim(claim, evidence)
        rows.append({"id": index, "claim": claim, "expected": expected, "assessment": result.model_dump(mode="json")})
    summary = {"cases": len(rows), "accuracy": sum(row["expected"] == row["assessment"]["label"] for row in rows) / len(rows), "status": "authored deterministic controls; not external evidence-grounding performance"}
    payload = {"summary": summary, "rows": rows}
    Path("artifacts/evidence_grounding_benchmark.json").write_text(json.dumps(payload, indent=2) + "\n")
    Path("reports/evidence_grounding.md").write_text("# Evidence grounding benchmark\n\n" + json.dumps(summary, indent=2) + "\n\nThese six controls test only the conservative deterministic token-support gate. Amazon Contextual Product QA is registered as evaluation-only pending rights review and has not been downloaded. This is not a production accuracy claim.\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
