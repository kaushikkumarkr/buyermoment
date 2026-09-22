from __future__ import annotations

from pathlib import Path
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .analyzer import discover_buyer_moments
from .commercial import CampaignOutcome, DesignPartnerFeedback, PilotRequest
from .commercial_workflow import build_opportunity_report, generate_ad_experiment, import_outcomes_csv_text
from .demo import demo_businesses
from .dogfood import load_package
from .evidence import chunk_source, retrieve, source_from_text
from .ingestion import fetch_website, parse_file
from .experiments import export_experiment, generate_experiment
from .ledger import ExperimentLedger
from .models import BusinessProfile, CommercialContext, Experiment
from .planners import chatgpt_ads_plan, google_ai_max_plan
from .scoring import score
from .service import analyze_package, audit_measurement, build_client_report, next_best_experiment, package_from_sources
from .service_ledger import ServiceLedger
from .service_models import AnalysisRun, Client, DesignPartnerFeedbackV2, HumanApproval
from .spend_safety import spend_safety

app = FastAPI(title="BuyerMoment API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "buyermoment-api"}


@app.get("/api/demo")
def demo() -> dict:
    businesses = demo_businesses()
    return {"businesses": [business.model_dump(mode="json") for business in businesses], "moments": {business.id: [moment.model_dump(mode="json") for moment in discover_buyer_moments(business)] for business in businesses}}


@app.get("/api/businesses/{business_id}/buyer-moments")
def buyer_moments(business_id: str) -> list[dict]:
    business = next((item for item in demo_businesses() if item.id == business_id), None)
    if business is None:
        raise HTTPException(404, "Business not found")
    return [moment.model_dump(mode="json") for moment in discover_buyer_moments(business)]


@app.post("/api/score")
def score_context(payload: dict) -> dict:
    context = CommercialContext.model_validate(payload["context"])
    product = next((item for business in demo_businesses() for item in business.products if item.id == payload.get("product_id")), None)
    if product is None:
        raise HTTPException(404, "Product not found")
    return score(context, product).model_dump(mode="json")


@app.post("/api/spend-decision")
def spend_decision(payload: dict) -> dict:
    context = CommercialContext.model_validate(payload["context"])
    product = next((item for business in demo_businesses() for item in business.products if item.id == payload.get("product_id")), None)
    if product is None:
        raise HTTPException(404, "Product not found")
    contextfit = score(context, product)
    return {"contextfit": contextfit.model_dump(mode="json"), "spend_decision": spend_safety(context, product, contextfit).model_dump(mode="json")}


@app.post("/api/experiments", response_model=Experiment)
def experiment(payload: dict) -> Experiment:
    business = next((item for item in demo_businesses() if item.id == payload.get("business_id")), None)
    if business is None:
        raise HTTPException(404, "Business not found")
    moment = next((item for item in discover_buyer_moments(business) if item.id == payload.get("buyer_moment_id")), None)
    if moment is None:
        raise HTTPException(404, "Buyer Moment not found")
    return generate_experiment(moment, business.offers[0] if business.offers else None)


@app.post("/api/experiments/export")
def experiment_export(experiment: Experiment) -> Response:
    return Response(content=export_experiment(experiment), media_type="application/json", headers={"Content-Disposition": f'attachment; filename="{experiment.id}.json"'})


@app.post("/api/ad-experiments")
def ad_experiment(payload: dict) -> dict:
    business = next((item for item in demo_businesses() if item.id == payload.get("business_id")), None)
    if business is None:
        raise HTTPException(404, "Business not found")
    moment = next((item for item in discover_buyer_moments(business) if item.id == payload.get("buyer_moment_id")), None)
    if moment is None:
        raise HTTPException(404, "Buyer Moment not found")
    experiment = generate_ad_experiment(moment, business.id, platform=payload.get("platform", "chatgpt_ads"), budget=payload.get("budget"))
    ExperimentLedger().save_experiment(experiment)
    return experiment.model_dump(mode="json")


@app.post("/api/outcomes")
def campaign_outcome(outcome: CampaignOutcome) -> dict:
    lineage = ExperimentLedger().save_outcome(outcome)
    return lineage.model_dump(mode="json")


@app.post("/api/design-partner/feedback")
def design_partner_feedback(feedback: DesignPartnerFeedback) -> dict:
    return {"accepted": True, "feedback": feedback.model_dump(mode="json"), "formal_ml_ground_truth": False}


@app.post("/api/pilot-request")
def pilot_request(request: PilotRequest) -> dict:
    ExperimentLedger().save_pilot_request(request)
    return {"accepted": True, "request_id": request.request_id, "conversion_type": request.conversion_type, "private_storage": True}


@app.get("/api/phase7/dogfood")
def dogfood_report() -> dict:
    package = load_package(Path("businesses/buyermoment/business_evidence.json"))
    return build_opportunity_report(package).model_dump(mode="json")


@app.get("/api/clients")
def list_clients() -> list[dict]:
    return [client.model_dump(mode="json") for client in ServiceLedger().list_clients()]


@app.post("/api/clients")
def create_client(client: Client) -> dict:
    ledger = ServiceLedger()
    ledger.save_client(client)
    return client.model_dump(mode="json")


@app.post("/api/clients/{client_id}/evidence")
def ingest_client_evidence(client_id: str, payload: dict) -> dict:
    ledger = ServiceLedger()
    if ledger.get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    text = str(payload.get("text", "")).strip()
    if not text:
        raise HTTPException(422, "Evidence text is required")
    source = source_from_text(
        source_id=str(payload.get("source_id") or f"src-{uuid4().hex[:12]}"),
        client_id=client_id,
        source_type=str(payload.get("source_type", "provided")),
        title=str(payload.get("title", "Untitled evidence")),
        text=text,
        uri=payload.get("uri"),
        data_origin=str(payload.get("data_origin", "provided")),
        private=bool(payload.get("private", True)),
    )
    chunks = chunk_source(source)
    ledger.save_source(source, chunks)
    return {"source": source.model_dump(mode="json"), "chunks": [chunk.model_dump(mode="json") for chunk in chunks]}


@app.post("/api/clients/{client_id}/evidence/file")
def ingest_client_file(client_id: str, payload: dict) -> dict:
    if ServiceLedger().get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    try:
        filename, text = parse_file(str(payload.get("filename", "")), str(payload.get("content", "")).encode())
    except (ValueError, KeyError) as exc:
        raise HTTPException(422, str(exc)) from exc
    suffix = filename.rsplit(".", 1)[-1].lower()
    source_type = "html" if suffix == "htm" else suffix
    source = source_from_text(
        source_id=str(payload.get("source_id") or f"src-{uuid4().hex[:12]}"),
        client_id=client_id,
        source_type=source_type,
        title=filename,
        text=text,
        uri=payload.get("uri"),
        data_origin=str(payload.get("data_origin", "provided")),
        private=bool(payload.get("private", True)),
    )
    chunks = chunk_source(source)
    ServiceLedger().save_source(source, chunks)
    return {"source": source.model_dump(mode="json"), "chunks": len(chunks)}


@app.post("/api/clients/{client_id}/evidence/website")
def ingest_client_website(client_id: str, payload: dict) -> dict:
    if ServiceLedger().get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    url = str(payload.get("url", ""))
    try:
        content_type, text = fetch_website(url)
    except (ValueError, OSError) as exc:
        raise HTTPException(422, str(exc)) from exc
    source = source_from_text(
        source_id=str(payload.get("source_id") or f"src-{uuid4().hex[:12]}"),
        client_id=client_id,
        source_type="website",
        title=str(payload.get("title") or url),
        text=text,
        uri=url,
        data_origin="public",
        private=False,
    )
    source.provenance["content_type"] = content_type
    chunks = chunk_source(source)
    ServiceLedger().save_source(source, chunks)
    return {"source": source.model_dump(mode="json"), "chunks": len(chunks)}


@app.post("/api/clients/{client_id}/search")
def search_client_evidence(client_id: str, payload: dict) -> list[dict]:
    ledger = ServiceLedger()
    if ledger.get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    chunks = retrieve(ledger.list_chunks(client_id), client_id=client_id, query=str(payload.get("query", "")))
    return [chunk.model_dump(mode="json") for chunk in chunks]


@app.post("/api/clients/{client_id}/analyze")
def analyze_client(client_id: str, payload: dict) -> dict:
    started = perf_counter()
    ledger = ServiceLedger()
    client = ledger.get_client(client_id)
    if client is None:
        raise HTTPException(404, "Client not found")
    try:
        from .commercial import BusinessEvidencePackage

        package = BusinessEvidencePackage.model_validate(payload)
    except Exception as exc:
        raise HTTPException(422, f"Invalid business evidence package: {exc}") from exc
    analysis = analyze_package(client, package, ledger.list_sources(client_id))
    ledger.save_portfolio(analysis.portfolio)
    ledger.save_analysis_run(AnalysisRun(run_id=f"run-{uuid4().hex[:12]}", client_id=client_id, status="SUCCEEDED", duration_ms=int((perf_counter() - started) * 1000), retrieval_calls=0, llm_calls=0, metadata={"mode": "legacy_local"}))
    return analysis.model_dump(mode="json")


@app.post("/api/clients/{client_id}/analyze-from-evidence")
def analyze_client_from_evidence(client_id: str) -> dict:
    started = perf_counter()
    ledger = ServiceLedger()
    client = ledger.get_client(client_id)
    sources = ledger.list_sources(client_id)
    if client is None:
        raise HTTPException(404, "Client not found")
    if not sources:
        raise HTTPException(422, "At least one evidence source is required")
    analysis = analyze_package(client, package_from_sources(client, sources), sources)
    ledger.save_portfolio(analysis.portfolio)
    ledger.save_analysis_run(AnalysisRun(run_id=f"run-{uuid4().hex[:12]}", client_id=client_id, status="SUCCEEDED", duration_ms=int((perf_counter() - started) * 1000), retrieval_calls=len(sources), llm_calls=0, metadata={"mode": "legacy_local", "source_count": len(sources)}))
    return analysis.model_dump(mode="json")


@app.get("/api/clients/{client_id}/workspace")
def client_workspace(client_id: str) -> dict:
    ledger = ServiceLedger()
    client = ledger.get_client(client_id)
    if client is None:
        raise HTTPException(404, "Client not found")
    experiments = []
    for row in ledger.list_experiments():
        if row.get("client_id") == client_id:
            experiments.append(row)
    return {
        "client": client.model_dump(mode="json"),
        "evidence_sources": [source.model_dump(mode="json") for source in ledger.list_sources(client_id)],
        "portfolio": (ledger.get_portfolio(client_id).model_dump(mode="json") if ledger.get_portfolio(client_id) else None),
        "experiments": experiments,
        "analysis_runs": [run.model_dump(mode="json") for run in ledger.list_analysis_runs(client_id)],
        "measurement_audit": (ledger.get_measurement_audit(client_id).model_dump(mode="json") if ledger.get_measurement_audit(client_id) else None),
    }


@app.post("/api/clients/{client_id}/measurement-audit")
def client_measurement_audit(client_id: str, payload: dict) -> dict:
    ledger = ServiceLedger()
    if ledger.get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    audit = audit_measurement(client_id, payload)
    ledger.save_measurement_audit(audit)
    return audit.model_dump(mode="json")


@app.post("/api/clients/{client_id}/experiments")
def create_client_experiment(client_id: str, payload: dict) -> dict:
    ledger = ServiceLedger()
    client = ledger.get_client(client_id)
    portfolio = ledger.get_portfolio(client_id)
    if client is None or portfolio is None:
        raise HTTPException(404, "Client analysis not found")
    item = next((candidate for candidate in [*portfolio.test, *portfolio.watch, *portfolio.blocked_or_abstained] if candidate.buyer_moment.id == payload.get("buyer_moment_id")), None)
    if item is None:
        raise HTTPException(404, "Buyer Moment not found in portfolio")
    experiment = generate_ad_experiment(item.buyer_moment, client_id, platform=payload.get("platform", "chatgpt_ads"), budget=payload.get("budget"), client_id=client_id)
    ledger.save_experiment(experiment)
    return {"experiment": experiment.model_dump(mode="json"), "chatgpt_ads": chatgpt_ads_plan(experiment)}


@app.get("/api/clients/{client_id}/experiments/{experiment_id}/plans")
def client_experiment_plans(client_id: str, experiment_id: str) -> dict:
    row = next((item for item in ServiceLedger().list_experiments() if item.get("experiment_id") == experiment_id and item.get("client_id") == client_id), None)
    if row is None:
        raise HTTPException(404, "Experiment not found")
    from .commercial import AdExperiment

    experiment = AdExperiment.model_validate_json(row["payload_json"])
    portfolio = ServiceLedger().get_portfolio(client_id)
    item = next((candidate for candidate in [*(portfolio.test if portfolio else []), *(portfolio.watch if portfolio else [])] if candidate.buyer_moment.id == experiment.buyer_moment_id), None)
    if item is None:
        raise HTTPException(404, "Buyer Moment not found")
    business = item.buyer_moment.matching_products[0]
    return {"chatgpt_ads": chatgpt_ads_plan(experiment), "google_ai_max": google_ai_max_plan(item.buyer_moment, BusinessProfile(id=client_id, name=client_id, category=business.category, description="Service plan", products=[business]))}


@app.post("/api/clients/{client_id}/feedback")
def save_client_feedback(client_id: str, feedback: DesignPartnerFeedbackV2) -> dict:
    if feedback.client_id != client_id:
        raise HTTPException(400, "Client boundary mismatch")
    ledger = ServiceLedger()
    if ledger.get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    ledger.save_feedback(feedback)
    return {"accepted": True, "formal_ml_ground_truth": False, "feedback_id": feedback.id}


@app.post("/api/clients/{client_id}/approvals")
def save_client_approval(client_id: str, approval: HumanApproval) -> dict:
    if approval.client_id != client_id:
        raise HTTPException(400, "Client boundary mismatch")
    if approval.approved:
        raise HTTPException(403, "Live advertising approval must be recorded by an authorized human operator outside this API")
    ServiceLedger().save_approval(approval)
    return {"accepted": True, "human_approval_required": True}


@app.post("/api/clients/{client_id}/report")
def client_report(client_id: str, payload: dict | None = None) -> dict:
    ledger = ServiceLedger()
    client = ledger.get_client(client_id)
    portfolio = ledger.get_portfolio(client_id)
    if client is None or portfolio is None:
        raise HTTPException(404, "Client analysis not found")
    report = build_client_report(client, portfolio, [], (payload or {}).get("unknowns", []))
    ledger.save_report(report)
    return report.model_dump(mode="json")


@app.post("/api/clients/{client_id}/outcomes")
def client_outcome(client_id: str, outcome: CampaignOutcome) -> dict:
    ledger = ServiceLedger()
    if ledger.get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    if outcome.client_id not in {"default", client_id}:
        raise HTTPException(400, "Outcome crosses client boundary")
    outcome.client_id = client_id
    lineage = ledger.save_outcome(outcome)
    return lineage.model_dump(mode="json")


@app.post("/api/clients/{client_id}/outcomes/import")
def import_client_outcomes(client_id: str, payload: dict) -> dict:
    ledger = ServiceLedger()
    if ledger.get_client(client_id) is None:
        raise HTTPException(404, "Client not found")
    try:
        outcomes = import_outcomes_csv_text(str(payload.get("csv", "")), source_name=str(payload.get("source", "manual_csv")))
        lineages = []
        for outcome in outcomes:
            outcome.client_id = client_id
            lineages.append(ledger.save_outcome(outcome).model_dump(mode="json"))
    except (KeyError, ValueError) as exc:
        raise HTTPException(422, f"Invalid outcome CSV: {exc}") from exc
    return {"imported": len(lineages), "lineage": lineages, "human_approval_required": True}


@app.post("/api/clients/{client_id}/next-best-experiment/{buyer_moment_id}")
def client_next_best_experiment(client_id: str, buyer_moment_id: str) -> dict:
    ledger = ServiceLedger()
    portfolio = ledger.get_portfolio(client_id)
    if ledger.get_client(client_id) is None or portfolio is None:
        raise HTTPException(404, "Client analysis not found")
    item = next((candidate for candidate in [*portfolio.test, *portfolio.watch, *portfolio.blocked_or_abstained] if candidate.buyer_moment.id == buyer_moment_id), None)
    if item is None:
        raise HTTPException(404, "Buyer Moment not found")
    outcomes = []
    for row in ledger.list_outcomes():
        if row.get("payload_json"):
            outcome = CampaignOutcome.model_validate_json(row["payload_json"])
            if outcome.client_id in {"default", client_id}:
                outcomes.append(outcome)
    return next_best_experiment(client_id, item, outcomes).model_dump(mode="json")
