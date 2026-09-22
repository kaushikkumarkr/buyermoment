from buyermoment.models import CommercialContextRecord, Evidence, LocationContext


def test_canonical_record_preserves_provenance_and_nullable_fields():
    record = CommercialContextRecord(
        record_id="test:1",
        source_dataset="wayfair_wands",
        source_record_id="42",
        source_license="MIT",
        context_text="salon chair",
        original_query="salon chair",
        product_id="p1",
        product_title="Salon chair",
        relevance="exact",
        product_fit=1.0,
        location=LocationContext(country="US"),
        evidence=[Evidence(id="q", kind="observed", text="salon chair", source="test", source_record_id="42")],
        provenance=["source query/product join"],
        metadata={"original_label": "Exact"},
    )
    assert record.metadata["original_label"] == "Exact"
    assert record.constraints.budget_max is None
    assert record.evidence[0].kind == "observed"
