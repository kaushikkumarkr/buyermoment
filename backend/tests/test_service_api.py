import asyncio

import httpx

from buyermoment.api import app


def test_service_api_flow_is_client_scoped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    async def run_flow():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as client:
            response = await client.post("/api/clients", json={"id": "client-api", "name": "API SaaS", "vertical": "B2B SaaS"})
            assert response.status_code == 200
            response = await client.post("/api/clients/client-api/evidence", json={"source_type": "provided", "title": "Product evidence", "text": "DEMO_SYNTHETIC: secure analytics for support teams."})
            assert response.status_code == 200
            package = {
        "business": {
            "id": "business-api", "name": "API SaaS", "category": "B2B SaaS", "description": "Analytics", "products": [{"id": "product-api", "name": "Analytics", "category": "B2B SaaS", "description": "Secure analytics for support teams.", "url": "https://demo.invalid/product"}], "offers": [{"id": "offer-api", "name": "Book a demo", "description": "Talk to an analytics specialist."}]
        },
        "target_customer_hypotheses": [{"id": "hyp-api", "label": "Support leaders", "situation": "A support team is evaluating analytics this quarter.", "problem": "Reporting is fragmented.", "desired_outcome": "Shortlist a secure analytics tool.", "evidence_ids": [], "origin": "inference"}],
        "unknowns": ["No real outcomes"]
            }
            response = await client.post("/api/clients/client-api/analyze", json=package)
            assert response.status_code == 200, response.text
            portfolio = response.json()["portfolio"]
            candidate = (portfolio["test"] or portfolio["watch"] or portfolio["blocked_or_abstained"])[0]["buyer_moment"]["id"]
            response = await client.post("/api/clients/client-api/experiments", json={"buyer_moment_id": candidate, "platform": "chatgpt_ads"})
            assert response.status_code == 200, response.text
            assert response.json()["experiment"]["approval"]["required"] is True
            experiment_id = response.json()["experiment"]["experiment_id"]
            outcome_csv = "experiment_id,client_id,buyer_moment_id,platform,date,impressions,clicks,spend,conversions,qualified_conversions,source\n" + f"{experiment_id},client-api,{candidate},manual,2026-09-22,10,1,2,0,0,fixture\n"
            response = await client.post("/api/clients/client-api/outcomes/import", json={"csv": outcome_csv, "source": "fixture"})
            assert response.status_code == 200, response.text
            response = await client.post(f"/api/clients/client-api/next-best-experiment/{candidate}")
            assert response.status_code == 200
            response = await client.post("/api/clients/client-api/measurement-audit", json={"primary_conversion": "demo_request", "utm_parameters": True, "deduplication": True})
            assert response.status_code == 200
            response = await client.post("/api/clients/client-api/report", json={"unknowns": ["No live campaign data"]})
            assert response.status_code == 200

    asyncio.run(run_flow())
