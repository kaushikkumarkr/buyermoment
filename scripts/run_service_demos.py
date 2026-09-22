from __future__ import annotations

import json
from pathlib import Path

from buyermoment.service import analyze_package, audit_measurement, build_client_report
from buyermoment.service_demos import service_demo_packages
from buyermoment.service_models import Client


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    results = []
    for package in service_demo_packages():
        client = Client(id=f"{package.business.id}-client", name=package.business.name, vertical="B2B SaaS")
        analysis = analyze_package(client, package, [])
        measurement = audit_measurement(client.id, {"primary_conversion": "demo_request", "utm_parameters": True, "deduplication": True, "crm_linkage": True, "offline_conversion_path": True, "revenue_or_pipeline_fields": True, "conversion_lag": "90d"})
        report = build_client_report(client, analysis.portfolio, [], package.unknowns)
        results.append({"client": client.model_dump(mode="json"), "analysis": analysis.model_dump(mode="json"), "measurement": measurement.model_dump(mode="json"), "report": report.model_dump(mode="json"), "data_origin": "DEMO_SYNTHETIC"})
    output = ROOT / "artifacts" / "service_demo_validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"businesses": len(results), "output": str(output), "data_origin": "DEMO_SYNTHETIC"}, indent=2))


if __name__ == "__main__":
    main()
