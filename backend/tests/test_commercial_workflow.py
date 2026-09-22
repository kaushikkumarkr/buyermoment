import csv
from pathlib import Path

import pytest

from buyermoment.commercial import BusinessEvidencePackage, CampaignOutcome, PilotRequest
from buyermoment.commercial_workflow import import_outcomes_csv, outcome_lineage
from buyermoment.dogfood import load_package
from buyermoment.ledger import ExperimentLedger


def test_dogfood_package_derives_candidates_with_provenance() -> None:
    package = load_package(Path("businesses/buyermoment/business_evidence.json"))
    assert isinstance(package, BusinessEvidencePackage)
    from buyermoment.commercial_workflow import build_opportunity_report, discover_package_moments

    moments = discover_package_moments(package)
    report = build_opportunity_report(package)
    assert len(moments) >= 20
    assert report.supported_candidate_count == len(moments)
    assert all(moment.supporting_evidence for moment in moments)
    assert all(any(item.kind == "observed" for item in moment.supporting_evidence) for moment in moments)


def test_outcome_lineage_is_immutable() -> None:
    package = load_package(Path("businesses/buyermoment/business_evidence.json"))
    from buyermoment.commercial_workflow import discover_package_moments, generate_ad_experiment

    moment = discover_package_moments(package)[0]
    experiment = generate_ad_experiment(moment, package.business.id)
    outcome = CampaignOutcome(experiment_id=experiment.experiment_id, buyer_moment_id=moment.id, platform="manual", date="2026-09-22", source="test", import_method="manual_entry")
    lineage = outcome_lineage(experiment, outcome)
    assert lineage.buyer_moment_id == moment.id
    with pytest.raises(ValueError):
        outcome_lineage(experiment, outcome.model_copy(update={"buyer_moment_id": "other"}))


def test_manual_csv_import_and_sqlite_ledger(tmp_path: Path) -> None:
    package = load_package(Path("businesses/buyermoment/business_evidence.json"))
    from buyermoment.commercial_workflow import discover_package_moments, generate_ad_experiment

    moment = discover_package_moments(package)[0]
    experiment = generate_ad_experiment(moment, package.business.id)
    ledger = ExperimentLedger(tmp_path / "ledger.sqlite3")
    ledger.save_experiment(experiment)
    csv_path = tmp_path / "outcomes.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["experiment_id", "buyer_moment_id", "platform", "date", "impressions", "clicks", "spend", "conversions", "qualified_conversions", "source"])
        writer.writeheader()
        writer.writerow({"experiment_id": experiment.experiment_id, "buyer_moment_id": moment.id, "platform": "manual", "date": "2026-09-22", "impressions": 10, "clicks": 2, "spend": 3.5, "conversions": 1, "qualified_conversions": 1, "source": "test"})
    outcome = import_outcomes_csv(csv_path)[0]
    lineage = ledger.save_outcome(outcome)
    assert lineage.experiment_id == experiment.experiment_id
    assert len(ledger.list_outcomes()) == 1


def test_pilot_request_is_validated_and_stored(tmp_path: Path) -> None:
    from buyermoment.ledger import ExperimentLedger

    ledger = ExperimentLedger(tmp_path / "ledger.sqlite3")
    request = PilotRequest(request_id="req-1", name="Test Owner", work_email="owner@example.com", company="Example SaaS", website="https://example.com", role="Founder")
    ledger.save_pilot_request(request)
