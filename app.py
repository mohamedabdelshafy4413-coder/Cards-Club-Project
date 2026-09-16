from pathlib import Path
import csv
import html
import streamlit as st

st.set_page_config(
    page_title="Cards Club Export Command Center",
    page_icon="🂡",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
DATA = ROOT / "data"
LOGO = ROOT / "assets" / "cards-club-logo.svg"

st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"]{background:#fbfdfb;color:#101410}
[data-testid="stSidebar"]{border-right:1px solid #d9e4dc;background:#0b0e0c}
[data-testid="stSidebar"] *{color:#f6fff8}
.block-container{max-width:1600px;padding-top:1rem;padding-bottom:2rem}
.hero{background:linear-gradient(135deg,#080b09 0%,#111713 68%,#a6f3b5 180%);border:1px solid #27352b;border-radius:24px;padding:30px 32px;margin-bottom:18px;box-shadow:0 14px 40px rgba(0,0,0,.12)}
.hero h1{color:#fff;margin:6px 0 0;font-size:2.25rem}.hero p{color:#dce8df;line-height:1.8;margin:.7rem 0 0}.tag{display:inline-block;background:#c9ffd5;color:#07150b;border-radius:999px;padding:5px 11px;margin-right:6px;font-size:.76rem;font-weight:850}
.kpi{background:#fff;border:1px solid #dce7df;border-radius:16px;padding:16px 18px;min-height:128px;box-shadow:0 6px 18px rgba(10,30,18,.05)}
.kpi .label{font-size:.82rem;color:#58675e}.kpi .value{font-size:1.46rem;font-weight:850;color:#0c1710;margin:.3rem 0}.kpi .note{font-size:.78rem;color:#6b786f;line-height:1.55}
.panel{background:#fff;border:1px solid #dce7df;border-radius:16px;padding:18px 20px;margin:.55rem 0 1rem}.good{border-left:5px solid #61d881;background:#f3fff6}.warn{border-left:5px solid #e5b34f;background:#fffaf0}.risk{border-left:5px solid #db6a6a;background:#fff5f5}.titleline{font-weight:900;font-size:1.1rem;color:#0b1710;margin-bottom:.3rem}
.mono{direction:ltr;text-align:left;font-family:monospace;white-space:pre-wrap;background:#0c120e;color:#dfffea;border-radius:12px;padding:14px}
.marketrow{background:#fff;border:1px solid #e2ebe4;border-radius:12px;padding:10px 12px;margin:6px 0}.marketname{font-weight:800}.score{float:right;background:#c9ffd5;color:#07150b;padding:2px 8px;border-radius:999px;font-weight:800}
</style>
""",
    unsafe_allow_html=True,
)


def esc(x):
    return html.escape(str(x))


@st.cache_data(show_spinner=False, ttl=3600)
def load_csv(name):
    path = DATA / name
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def to_float(v, default=0.0):
    try:
        if v in (None, "", "nan", "None"):
            return default
        return float(v)
    except Exception:
        return default


def to_int(v, default=0):
    try:
        return int(float(v))
    except Exception:
        return default


def money(v):
    try:
        if v in (None, "", "nan", "None"):
            return "Not verified"
        return f"${float(v):,.0f}"
    except Exception:
        return "Not verified"


def panel(title, body, kind="good"):
    st.markdown(
        f'<div class="panel {kind}"><div class="titleline">{esc(title)}</div>{body}</div>',
        unsafe_allow_html=True,
    )


def kpi(label, value, note):
    st.markdown(
        f'<div class="kpi"><div class="label">{esc(label)}</div><div class="value">{esc(value)}</div><div class="note">{esc(note)}</div></div>',
        unsafe_allow_html=True,
    )


def top_market_rows(rows, n=12):
    rows = sorted(rows, key=lambda r: to_float(r.get("Score /100")), reverse=True)[:n]
    for r in rows:
        score = to_int(r.get("Score /100"))
        st.markdown(
            f'<div class="marketrow"><span class="marketname">#{esc(r.get("Rank"))} · {esc(r.get("Country"))}</span><span class="score">{score}/100</span><br><small>{esc(r.get("Country Positioning"))}</small></div>',
            unsafe_allow_html=True,
        )


SWOT = {
    "Strengths": [
        "Made-in-Egypt manufacturing base close to GCC and Africa.",
        "Standard + heritage + tourism + seasonal + custom portfolio.",
        "Customization moves the sale away from commodity-only pricing.",
        "Egyptian cultural storytelling creates differentiated creative IP.",
        "Potential regional trade preferences, subject to Rules of Origin.",
    ],
    "Weaknesses": [
        "Limited international export proof versus established suppliers.",
        "Master-data inconsistencies must be fixed before buyer-facing use.",
        "Pricing still needs full EXW / FOB / CIF governance.",
        "B2B case studies and distributor references are limited.",
        "Some capacity/specification claims need verification.",
    ],
    "Opportunities": [
        "Cards Club BrandLab for corporate/private-label business.",
        "Hotels, resorts, museums, duty-free and tourism souvenir decks.",
        "UAE as GCC hub and South Africa as Southern Africa hub.",
        "Localized Ramadan, wildlife, national-occasion and destination decks.",
        "Importers, gifting agencies, hospitality and direct strategic brands.",
    ],
    "Threats": [
        "China and other scale suppliers dominate pure price competition.",
        "Origin/compliance errors can block shipments or remove tariff benefits.",
        "FX, freight and payment risk can erase margin.",
        "Weak exclusivity contracts can lock a market behind a weak distributor.",
        "IP, cultural sensitivity and gambling perception can create friction.",
    ],
}

EMAILS = {
    "Distributor Acquisition": (
        "Playing cards for {{Country}}",
        "Standard, cultural and private-label decks manufactured in Egypt.",
        "Hi {{FirstName}},\n\nCards Club manufactures premium playing cards in Egypt for retail, distribution and private-label programs.\n\nWe offer standard Bridge decks, cultural collections and fully customized editions. We're opening selected distribution partnerships in {{Country}}, and {{Company}} looks relevant.\n\nWould it be useful if I sent our distributor range, MOQ and export pricing?\n\nBest,\nCards Club Export Team",
    ),
    "Regional Supplier Alternative": (
        "A closer deck supplier",
        "Regional production instead of another long Asian supply chain.",
        "Hi {{FirstName}},\n\nIf your playing-card range currently comes from Asia or Europe, Cards Club offers a manufacturing alternative from Egypt. We produce standard and custom decks with flexible branding, packaging and regional export support.\n\nIf you share the product you currently buy, I can prepare a like-for-like commercial comparison.\n\nBest,\nCards Club Export Team",
    ),
    "Corporate BrandLab": (
        "52 branded touchpoints",
        "Not another promotional giveaway.",
        "Hi {{FirstName}},\n\nA custom playing-card deck puts {{Company}} across 52 usable, collectible brand touchpoints — from the cards to the packaging. Cards Club handles concept, design and manufacturing in Egypt.\n\nWould you like us to create one sample concept for {{Company}}?\n\nBest,\nCards Club BrandLab",
    ),
    "Hotels & Resorts": (
        "Your hotel as a collectible deck",
        "Guest entertainment, souvenir and branded gift in one product.",
        "Hi {{FirstName}},\n\nWe manufacture custom playing-card decks for hospitality and tourism brands. A {{Hotel}} edition can feature the property, destination and local landmarks for guest rooms, VIP gifts and retail.\n\nWould you like to see three creative directions?\n\nBest,\nCards Club Export Team",
    ),
    "Tourism / Souvenir": (
        "Put {{City}} in their pocket",
        "A souvenir travelers can actually use.",
        "Hi {{FirstName}},\n\nCards Club creates destination decks inspired by local culture, landmarks and stories. We'd like to explore a {{Destination}} edition with {{Company}}.\n\nShould I send a sample concept?\n\nBest,\nCards Club Export Team",
    ),
    "Seasonal / Ramadan": (
        "52 moments for Ramadan",
        "A limited branded edition built for gifting.",
        "Hi {{FirstName}},\n\nCards Club creates premium seasonal decks for corporate gifting and brand campaigns. We can build a Ramadan edition around {{Company}} — artwork, packaging and production.\n\nWould you like a visual direction?\n\nBest,\nCards Club BrandLab",
    ),
    "Breakup / Re-engagement": (
        "Close {{Country}}?",
        "Last note from me.",
        "Hi {{FirstName}},\n\nI haven't heard back, so I'll close the conversation. We're selecting distribution and custom-deck partners in {{Country}}, and {{Company}} was still on our shortlist.\n\nIf relevant, reply CATALOG and I'll send everything over.\n\nBest,\nCards Club Export Team",
    ),
}

left, right = st.columns([1, 5])
with left:
    if LOGO.exists():
        st.image(str(LOGO))
with right:
    st.markdown(
        '<div class="hero"><span class="tag">GCC + AFRICA</span><span class="tag">HS 950440</span><span class="tag">90-DAY GTM</span><h1>Cards Club Export Command Center</h1><p><b>From Concept to Deck.</b> Market intelligence, positioning, export risk control, buyer targeting and commercial execution.</p></div>',
        unsafe_allow_html=True,
    )

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Dashboard",
        "Market Intelligence",
        "SWOT & Positioning",
        "Products & Offers",
        "Golden 1000",
        "90-Day Roadmap",
        "Risk Register",
        "Customs & Trade",
        "Email Campaigns",
        "Sales Scenarios",
        "Files & Sources",
    ],
)
st.sidebar.success("Runtime: lightweight CSV mode")
st.sidebar.caption("Research snapshot: Sep 2026. Re-validate tariffs, conformity and buyer data before live shipment.")

if page == "Executive Dashboard":
    cols = st.columns(5)
    items = [
        ("Priority markets", "50", "GCC + Africa intelligence universe"),
        ("Wave 1", "6", "UAE, Saudi, South Africa, Kuwait, Morocco, Qatar"),
        ("Golden accounts", "1,000", "Segmented target-company model"),
        ("Pilot POs", "2–6", "90-day operating scenario"),
        ("Core HS", "950440", "Playing cards"),
    ]
    for col, item in zip(cols, items):
        with col:
            kpi(*item)

    panel(
        "Execution rule",
        "50 markets are the intelligence universe, not a simultaneous rollout. First build export proof in Wave 1, then scale using reply, RFQ, sample, margin and reorder economics.",
        "warn",
    )
    countries = load_csv("countries.csv")
    st.markdown("### Top market-attractiveness scores")
    if countries:
        top_market_rows(countries, 12)
    else:
        st.error("countries.csv is missing or empty.")

    a, b, c = st.columns(3)
    with a:
        panel("Avoid the commodity trap", "Core products open doors; BrandLab, destination and heritage lines are the margin engine.")
    with b:
        panel("Build regional hubs", "Use UAE for GCC and South Africa for Southern Africa when partner economics and compliance support the route.")
    with c:
        panel("Build export proof", "Qualified buyer → RFQ → sample → pilot PO → reorder → case study.")

elif page == "Market Intelligence":
    countries = load_csv("countries.csv")
    st.subheader("50-country market intelligence")
    if not countries:
        st.error("Country dataset is missing.")
    else:
        c1, c2, c3 = st.columns(3)
        tiers = c1.multiselect("Tier", ["A", "B", "C", "D"], default=["A", "B", "C", "D"])
        all_regions = sorted({r.get("Region", "") for r in countries if r.get("Region")})
        regions = c2.multiselect("Region", all_regions, default=all_regions)
        query = c3.text_input("Search market / positioning").strip().lower()

        view = []
        for r in countries:
            if r.get("Tier") not in tiers or r.get("Region") not in regions:
                continue
            if query and query not in " ".join(str(v) for v in r.values()).lower():
                continue
            view.append(r)

        display_cols = ["Rank", "Tier", "Country", "Region", "HS950440 Import USD", "Data Year", "Score /100", "Product Focus", "Country Positioning", "3-Day Reply Potential"]
        st.dataframe([{k: r.get(k, "") for k in display_cols} for r in view], use_container_width=True, hide_index=True)

        options = [r.get("Country") for r in view] or [r.get("Country") for r in countries]
        market = st.selectbox("Country drill-down", options)
        r = next(x for x in countries if x.get("Country") == market)
        a, b, c, d = st.columns(4)
        a.metric("Rank", to_int(r.get("Rank")))
        b.metric("Tier", r.get("Tier", ""))
        c.metric("Import signal", money(r.get("HS950440 Import USD")))
        d.metric("Attractiveness", f"{to_int(r.get('Score /100'))}/100")
        panel("Country positioning", esc(r.get("Country Positioning", "")))
        x, y = st.columns(2)
        with x:
            st.write("**Product focus:**", r.get("Product Focus", ""))
            st.write("**Trade route:**", r.get("Potential Trade Route", ""))
            st.write("**Data status:**", r.get("Data Status", ""))
        with y:
            checks = [("Demand", "Demand /30", 30), ("Trade access", "Trade /20", 20), ("Product fit", "Fit /20", 20), ("Logistics", "Logistics /15", 15), ("Risk quality", "Risk /15", 15)]
            for label, field, maxv in checks:
                val = to_float(r.get(field))
                st.caption(f"{label}: {val:.0f}/{maxv}")
                st.progress(max(0.0, min(val / maxv, 1.0)))
        st.caption("Scores are internal decision-support heuristics, not guaranteed sales outcomes or sovereign-risk ratings.")

elif page == "SWOT & Positioning":
    panel("Master positioning", "<b>Cards Club — a regional design-to-deck manufacturing partner for brands, distributors, retailers, hotels and destinations across the Middle East and Africa.</b>")
    st.write("**Architecture:** Core · Heritage · Destinations · Seasons · BrandLab · Collector")
    a, b = st.columns(2)
    for idx, key in enumerate(["Strengths", "Weaknesses", "Opportunities", "Threats"]):
        target = a if idx % 2 == 0 else b
        kind = "good" if key in ("Strengths", "Opportunities") else "risk"
        with target:
            body = "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in SWOT[key]) + "</ul>"
            panel(key, body, kind)
    panel("Competitive frame", "Do not compete as the cheapest deck. Position Cards Club between anonymous commodity suppliers and high-price imported premium brands: closer, flexible, customizable, culturally relevant and export-oriented.", "warn")

elif page == "Products & Offers":
    products = load_csv("products.csv")
    st.subheader("Product & offer architecture")
    if products:
        st.dataframe(products, use_container_width=True, hide_index=True)
    a, b = st.columns(2)
    with a:
        panel("Margin priority", "BrandLab → Destination → Heritage → Core")
    with b:
        panel("Volume priority", "Core → Private Label → Tourism/Destination → Heritage")
    panel("Commercial ladder", "Trial MOQ → Standard MOQ → Strategic Distributor MOQ. Quote EXW → FOB → CIF with freight separated and short quote-validity windows.", "warn")

elif page == "Golden 1000":
    golden = load_csv("golden1000.csv")
    st.subheader("Golden 1000 account model")
    if golden:
        st.dataframe(golden, use_container_width=True, hide_index=True)
        st.markdown("### Segment allocation")
        for r in golden:
            val = to_int(r.get("Target Accounts"))
            st.write(f"**{r.get('Segment','')} — {val} accounts**")
            st.progress(min(val / 300.0, 1.0))
    st.markdown("### Wave 1 account allocation")
    wave = [
        {"Market": "UAE", "Accounts": 100, "Primary angle": "Distributor + BrandLab + Hospitality"},
        {"Market": "Saudi Arabia", "Accounts": 100, "Primary angle": "Distributor + BrandLab + Ramadan"},
        {"Market": "South Africa", "Accounts": 70, "Primary angle": "Distributor + Retail + Private Label"},
        {"Market": "Kuwait", "Accounts": 50, "Primary angle": "Premium retail + corporate gifting"},
        {"Market": "Morocco", "Accounts": 50, "Primary angle": "Tourism + distributor"},
        {"Market": "Qatar", "Accounts": 40, "Primary angle": "Hospitality + corporate"},
    ]
    st.dataframe(wave, hide_index=True, use_container_width=True)
    panel("Outbound operating rule", "No 1,000-contact blast. Split by country × segment × offer. Start with 1–2 decision makers per company and optimize positive reply, RFQ and sample rates.", "warn")

elif page == "90-Day Roadmap":
    roadmap = load_csv("roadmap.csv")
    st.subheader("90-day export execution")
    if roadmap:
        st.dataframe(roadmap, use_container_width=True, hide_index=True)
        for r in roadmap:
            with st.expander(f"Phase {r.get('Phase','')} · {r.get('Timing','')} · {r.get('Workstream','')}"):
                st.write("**Actions:**", r.get("Actions", ""))
                st.write("**Deliverable:**", r.get("Deliverable", ""))
                st.write("**Success metric:**", r.get("Success Metric", ""))
    panel("Gate 1", "No mass outbound before data, security and compliance cleanup.", "risk")
    panel("Gate 2", "No final landed-price promise before origin, freight and destination-customs validation.", "warn")
    panel("Gate 3", "No shipment before payment security, conformity and QC approval.", "risk")

elif page == "Risk Register":
    risks = load_csv("risks.csv")
    st.subheader("Export risk register")
    if not risks:
        st.error("Risk dataset is missing.")
    else:
        order = ["Critical", "High", "Medium", "Low"]
        selected = st.multiselect("Severity", order, default=order)
        view = [r for r in risks if r.get("Severity") in selected]
        st.dataframe(view, use_container_width=True, hide_index=True)
        counts = {s: sum(1 for r in view if r.get("Severity") == s) for s in order}
        st.markdown("### Risk mix")
        for s in order:
            st.write(f"**{s}: {counts[s]}**")
            st.progress(min(counts[s] / max(len(view), 1), 1.0))
        st.markdown("### Critical + high-risk controls")
        for r in risks:
            if r.get("Severity") not in ("Critical", "High"):
                continue
            with st.expander(f"{r.get('ID','')} · {r.get('Risk','')} — {r.get('Severity','')}"):
                st.write("**Impact:**", r.get("Impact", ""))
                st.write("**Mitigation:**", r.get("Mitigation", ""))
                st.write(f"**Owner:** {r.get('Owner','')} · **Gate:** {r.get('Deadline / Gate','')}")

elif page == "Customs & Trade":
    trade = load_csv("trade.csv")
    panel("Non-negotiable", "Never market ‘zero customs guaranteed’. Preferential treatment depends on HS classification, current agreement implementation, Rules of Origin, documentary evidence and destination-customs acceptance.", "risk")
    if trade:
        st.dataframe(trade, use_container_width=True, hide_index=True)
    st.markdown("### Pre-shipment gate")
    checks = [
        "Confirm destination HS classification",
        "Confirm applicable agreement + Rules of Origin",
        "Confirm label / marking / conformity route",
        "Approve commercial invoice + packing list + COO route",
        "Confirm payment security + Incoterm",
        "Approve Golden Sample / batch QC",
        "Validate freight, insurance, transit time and quote validity",
    ]
    for i, text in enumerate(checks, 1):
        st.checkbox(f"{i}. {text}", key=f"gate-{i}")

elif page == "Email Campaigns":
    st.subheader("7 outbound campaign angles")
    name = st.selectbox("Campaign", list(EMAILS))
    subject, preview, body = EMAILS[name]
    a, b = st.columns(2)
    with a:
        panel("Subject", esc(subject))
    with b:
        panel("Preview", esc(preview))
    st.markdown(f'<div class="mono">{esc(body)}</div>', unsafe_allow_html=True)
    st.caption("Use as a segment-specific starting point; personalize account context and keep the first CTA low-friction.")

elif page == "Sales Scenarios":
    st.subheader("90-day sales scenarios")
    st.caption("Operating scenarios, not guaranteed forecasts.")
    scenarios = [
        {"Scenario": "Conservative", "Target companies": 1000, "Replies": "15–25", "Qualified buyers": "2–5", "Pilot POs": "0–1"},
        {"Scenario": "Base", "Target companies": 1000, "Replies": "30–50", "Qualified buyers": "6–15", "Pilot POs": "2–4"},
        {"Scenario": "Strong", "Target companies": 1000, "Replies": "50–80+", "Qualified buyers": "12–25", "Pilot POs": "5–8"},
    ]
    st.dataframe(scenarios, hide_index=True, use_container_width=True)
    panel("KPI tree", "Deliverability → Reply → Positive reply → Qualified buyer → RFQ → Sample → PO → Gross margin → Reorder.")
    panel("72-hour goal", "Buyer interest, catalog/RFQ/sample intent — not assuming closed orders from cold email.", "warn")

elif page == "Files & Sources":
    sources = load_csv("sources.csv")
    st.subheader("Runtime files & source index")
    panel("Deployment architecture", "The dashboard uses small sanitized CSV files for fast startup. The original raw workbook is intentionally not published because it contains sensitive credentials / banking-related information. Heavy source documents are also kept out of the runtime bundle to reduce cold-start and repository weight.", "warn")
    st.markdown("### Download sanitized runtime data")
    files = ["countries.csv", "products.csv", "risks.csv", "roadmap.csv", "golden1000.csv", "trade.csv", "sources.csv"]
    cols = st.columns(3)
    for i, name in enumerate(files):
        path = DATA / name
        if path.exists():
            with cols[i % 3]:
                st.download_button(f"Download {name}", path.read_bytes(), file_name=name, mime="text/csv", key=f"download-{name}")
    if sources:
        st.markdown("### Research & source register")
        st.dataframe(sources, use_container_width=True, hide_index=True)
