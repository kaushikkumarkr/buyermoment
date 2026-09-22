from buyermoment.service import analyze_package, audit_measurement, build_client_report
from buyermoment.service_demos import service_demo_packages
from buyermoment.service_models import Client


def test_three_service_demo_full_flow():
    for package in service_demo_packages():
        client = Client(id=f"{package.business.id}-client", name=package.business.name, vertical="B2B SaaS")
        analysis = analyze_package(client, package, [])
        assert analysis.portfolio.human_approval_required
        assert analysis.buyer_moments
        assert all(item.buyer_moment.business_id == package.business.id for item in analysis.portfolio.test + analysis.portfolio.watch + analysis.portfolio.blocked_or_abstained)
        audit = audit_measurement(client.id, {"primary_conversion": "demo_request", "utm_parameters": True, "deduplication": True, "crm_linkage": True, "offline_conversion_path": True, "revenue_or_pipeline_fields": True, "conversion_lag": "90d"})
        assert audit.status == "TRACKING_READY"
        report = build_client_report(client, analysis.portfolio, [], package.unknowns)
        assert report.client_id == client.id
