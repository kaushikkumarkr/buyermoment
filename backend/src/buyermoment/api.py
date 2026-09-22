from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .analyzer import discover_buyer_moments
from .demo import demo_businesses
from .experiments import export_experiment, generate_experiment
from .models import CommercialContext, Experiment
from .scoring import score

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
