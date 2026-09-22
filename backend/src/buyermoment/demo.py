from .models import BusinessProfile, Evidence, Offer, Product


def _evidence(prefix: str, text: str, source: str = "demo_catalog") -> Evidence:
    return Evidence(id=prefix, kind="observed", text=text, source=source, source_record_id=prefix, confidence=0.98)


def demo_businesses() -> list[BusinessProfile]:
    return [
        BusinessProfile(
            id="northline-footwear", name="Northline Footwear", category="footwear", website="https://demo.northline.example", description="Technical trail footwear for day hikes and wet-weather travel.",
            products=[Product(id="northline-peakshield", name="PeakShield GTX", category="hiking boots", description="Waterproof hiking boots with slip-resistant outsole and cushioned ankle support for wet trails.", price=139, features=["waterproof", "slip-resistant", "cushioned support"], service_regions=["US", "Canada"], evidence=[_evidence("nf-p1", "Product catalog lists waterproof construction, slip-resistant outsole, and $139 price.")]), Product(id="northline-ridgeline", name="Ridgeline Hiker", category="hiking boots", description="Lightweight day-hike boot with durable traction for maintained trails.", price=119, features=["slip-resistant", "lightweight"], service_regions=["US"], evidence=[_evidence("nf-p2", "Product catalog lists lightweight build, traction, and $119 price.")])],
            offers=[Offer(id="nf-free-ship", name="Free US shipping", description="Free standard shipping on US orders.", evidence=[_evidence("nf-o1", "Offer sheet lists free standard shipping on US orders.", "offer_sheet")])],
            evidence=[_evidence("nf-b1", "Catalog positions Northline around wet-weather trail footwear.", "brand_brief")],
        ),
        BusinessProfile(
            id="kindred-skin", name="Kindred Skin", category="skincare", website="https://demo.kindred.example", description="Fragrance-free skincare designed for sensitive routines.",
            products=[Product(id="kindred-calm-set", name="Calm Start Set", category="skincare", description="A fragrance-free cleanser, barrier serum, and moisturizer for sensitive skin.", price=72, features=["fragrance-free", "sensitive skin", "barrier support"], service_regions=["US", "Canada"], evidence=[_evidence("ks-p1", "Product catalog lists fragrance-free formulas and a $72 set price.")]), Product(id="kindred-barrier-cream", name="Barrier Cloud Cream", category="moisturizer", description="Fragrance-free daily moisturizer for dry and reactive skin.", price=34, features=["fragrance-free", "sensitive skin"], service_regions=["US"], evidence=[_evidence("ks-p2", "Product catalog lists fragrance-free ingredients and a $34 price.")])],
            offers=[Offer(id="ks-bundle", name="Routine bundle", description="Save 10% when cleanser, serum, and moisturizer are purchased together.", discount_percent=10, evidence=[_evidence("ks-o1", "Offer sheet lists 10% routine bundle savings.", "offer_sheet")])],
            evidence=[_evidence("ks-b1", "Brand brief emphasizes fragrance-free routines for sensitive skin.", "brand_brief")],
        ),
        BusinessProfile(
            id="signaldesk", name="SignalDesk", category="b2b-saas", website="https://demo.signaldesk.example", description="Support intelligence for teams that want customer evidence in the operating rhythm.",
            products=[Product(id="signaldesk-core", name="SignalDesk Core", category="support analytics", description="Customer support analytics with conversation tagging, trend alerts, and SOC 2 controls.", price=599, currency="USD", features=["SOC 2", "conversation tagging", "trend alerts"], service_regions=["US", "Canada", "UK"], evidence=[_evidence("sd-p1", "Product brief lists SOC 2 controls, conversation tagging, and $599 monthly plan.")]), Product(id="signaldesk-team", name="SignalDesk Team", category="support analytics", description="A smaller support analytics workspace for growing teams with secure shared views.", price=299, currency="USD", features=["SOC 2", "shared views"], service_regions=["US", "Canada"], evidence=[_evidence("sd-p2", "Product brief lists SOC 2 controls and shared views on the $299 plan.")])],
            offers=[Offer(id="sd-pilot", name="30-day pilot", description="A time-boxed pilot with implementation guidance.", eligibility="Teams evaluating support analytics this quarter.", evidence=[_evidence("sd-o1", "Sales enablement sheet lists 30-day pilot and implementation guidance.", "sales_enablement")])],
            evidence=[_evidence("sd-b1", "Product brief positions SignalDesk around customer support intelligence.", "brand_brief")],
        ),
    ]

