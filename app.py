from pathlib import Path
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Cards Club Export Command Center", page_icon="🂡", layout="wide")
ROOT = Path(__file__).parent
DATA = ROOT / "data" / "Cards_Club_International_Export_Command_Center.xlsx"
LOGO = ROOT / "assets" / "cards-club-logo.png"
PROFILE = ROOT / "assets" / "CP-Cards-Club-14-07-2026.pdf"
LINKS = ROOT / "assets" / "Cards-Club-links.docx"

st.markdown("""
<style>
:root{--red:#E31B23;--black:#171315;--gold:#B68A3A;--light:#F7F3F4}
.stApp{background:#fbfafb}.block-container{padding-top:1.1rem}
.hero{background:linear-gradient(120deg,#171315,#2c2326 65%,#61191d);padding:24px 28px;border-radius:20px;color:white;margin-bottom:18px}
.hero h1{color:white;margin:0}.hero p{color:#f3e8ea;margin:.4rem 0 0}.kicker{color:#ff6b72;font-weight:800;font-size:.75rem;letter-spacing:.08em}
.card{background:white;border:1px solid #eadfe2;border-radius:16px;padding:16px;min-height:112px;box-shadow:0 8px 22px rgba(25,15,18,.05)}
.card .l{color:#7f6f74;font-size:.78rem;text-transform:uppercase}.card .v{font-size:1.65rem;font-weight:850;color:#171315;margin-top:.35rem}.card .s{font-size:.78rem;color:#8c7f83}
.note{border-left:4px solid #E31B23;padding:12px 16px;background:#fff2f3;border-radius:8px;margin:10px 0 18px}
.good{border-left:4px solid #1E8E5A;padding:12px 16px;background:#effaf4;border-radius:8px;margin:10px 0 18px}
[data-testid="stSidebar"]{background:#171315}[data-testid="stSidebar"] *{color:#f8f4f5}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load():
    if not DATA.exists(): return {}
    names=["Country Priority","Product Strategy","Risk Register","90 Day Roadmap","Golden 1000","Customs & Trade","Sources"]
    out={}
    for n in names:
        try: out[n]=pd.read_excel(DATA,sheet_name=n,header=3)
        except Exception: out[n]=pd.DataFrame()
    return out
D=load(); C=D.get("Country Priority",pd.DataFrame()); P=D.get("Product Strategy",pd.DataFrame()); R=D.get("Risk Register",pd.DataFrame()); M=D.get("90 Day Roadmap",pd.DataFrame()); G=D.get("Golden 1000",pd.DataFrame()); T=D.get("Customs & Trade",pd.DataFrame()); S=D.get("Sources",pd.DataFrame())
if not C.empty:
    C=C[pd.to_numeric(C.get("Rank"),errors="coerce").notna()].copy(); C["Rank"]=pd.to_numeric(C["Rank"]).astype(int); C["Score /100"]=pd.to_numeric(C["Score /100"],errors="coerce"); C["HS950440 Import USD"]=pd.to_numeric(C["HS950440 Import USD"],errors="coerce")
if not R.empty: R=R[R.get("ID").astype(str).str.match(r"R\d+",na=False)].copy()
if not M.empty: M=M[pd.to_numeric(M.get("Phase"),errors="coerce").notna()].copy()
if not G.empty: G=G[pd.to_numeric(G.get("Target Accounts"),errors="coerce").notna()].copy(); G["Target Accounts"]=pd.to_numeric(G["Target Accounts"])
if not T.empty: T=T[T.get("Framework").notna() & ~T.get("Framework").astype(str).isin(["Step","Mandatory pre-shipment gate"])].copy()
if not S.empty: S=S[S.get("Source").notna()].copy()

SWOT={
"Strengths":["Made-in-Egypt manufacturing base close to GCC and Africa.","Standard + heritage + tourism + seasonal + custom portfolio.","Customization moves the sale away from commodity-only pricing.","Egyptian cultural storytelling creates differentiated creative IP.","Potential preferential regional trade routes, subject to Rules of Origin."],
"Weaknesses":["Limited international export proof versus established suppliers.","Master-data inconsistencies must be fixed before buyer-facing use.","Pricing needs full EXW/FOB/CIF and buyer-tier governance.","B2B case studies and distributor references are still limited.","Some capacity/specification claims need verification."],
"Opportunities":["Cards Club BrandLab for corporate/private-label business.","Hotels, resorts, museums, duty-free and tourism souvenir decks.","UAE as GCC hub and South Africa as Southern Africa hub.","Localized Ramadan, wildlife, national occasion and destination decks.","Importers, gifting agencies, hospitality and direct strategic brands."],
"Threats":["China and other scale suppliers dominate pure price competition.","Origin/compliance errors can block shipments or remove tariff benefits.","FX, freight and payment risk can erase margin.","Weak exclusivity contracts can lock a market behind a weak distributor.","IP, cultural sensitivity and gambling perception create friction."]}
EMAILS={
"Distributor Acquisition":("Playing cards for {{Country}}","Standard, cultural and private-label decks manufactured in Egypt.","Hi {{FirstName}},\n\nCards Club manufactures premium playing cards in Egypt for retail, distribution and private-label programs.\n\nWe offer standard Bridge decks, cultural collections and fully customized editions. We're opening selected distribution partnerships in {{Country}}, and {{Company}} looks relevant.\n\nWould it be useful if I sent our distributor range, MOQ and export pricing?\n\nBest,\nCards Club Export Team"),
"Regional Supplier Alternative":("A closer deck supplier","Regional production instead of another long Asian supply chain.","Hi {{FirstName}},\n\nIf your playing-card range currently comes from Asia or Europe, Cards Club offers a manufacturing alternative from Egypt. We produce standard and custom decks with flexible branding, packaging and regional export support.\n\nIf you share the product you currently buy, I can prepare a like-for-like commercial comparison.\n\nBest,\nCards Club Export Team"),
"Corporate BrandLab":("52 branded touchpoints","Not another promotional giveaway.","Hi {{FirstName}},\n\nA custom playing-card deck puts {{Company}} across 52 usable, collectible brand touchpoints — from the cards to the packaging. Cards Club handles concept, design and manufacturing in Egypt.\n\nWould you like us to create one sample concept for {{Company}}?\n\nBest,\nCards Club BrandLab"),
"Hotels & Resorts":("Your hotel as a collectible deck","Guest entertainment, souvenir and branded gift in one product.","Hi {{FirstName}},\n\nWe manufacture custom playing-card decks for hospitality and tourism brands. A {{Hotel}} edition can feature the property, destination and local landmarks for guest rooms, VIP gifts and retail.\n\nWould you like to see three creative directions?\n\nBest,\nCards Club Export Team"),
"Tourism / Souvenir":("Put {{City}} in their pocket","A souvenir travelers can actually use.","Hi {{FirstName}},\n\nCards Club creates destination decks inspired by local culture, landmarks and stories. We'd like to explore a {{Destination}} edition with {{Company}}.\n\nShould I send a sample concept?\n\nBest,\nCards Club Export Team"),
"Seasonal / Ramadan":("52 moments for Ramadan","A limited branded edition built for gifting.","Hi {{FirstName}},\n\nCards Club creates premium seasonal decks for corporate gifting and brand campaigns. We can build a Ramadan edition around {{Company}} — artwork, packaging and production.\n\nWould you like a visual direction?\n\nBest,\nCards Club BrandLab"),
"Breakup / Re-engagement":("Close {{Country}}?","Last note from me.","Hi {{FirstName}},\n\nI haven't heard back, so I'll close the conversation. We're selecting distribution and custom-deck partners in {{Country}}, and {{Company}} was still on our shortlist.\n\nIf relevant, reply CATALOG and I'll send everything over.\n\nBest,\nCards Club Export Team")}

a,b=st.columns([1,5])
with a:
    if LOGO.exists(): st.image(str(LOGO),use_container_width=True)
with b: st.markdown('<div class="hero"><div class="kicker">INTERNATIONAL EXPORT COMMAND CENTER</div><h1>Cards Club</h1><p><b>From Concept to Deck.</b> GCC + Africa market intelligence, risk control and 90-day execution.</p></div>',unsafe_allow_html=True)

page=st.sidebar.radio("Navigate",["Executive Dashboard","Market Intelligence","SWOT & Positioning","Products & Offers","Golden 1000","90-Day Roadmap","Risk Register","Customs & Trade","Email Campaigns","Sales Scenarios","Files & Sources"])
st.sidebar.caption("Research snapshot: Sep 2026. Re-validate tariffs, conformity and buyer data before live shipment.")

def card(label,value,sub): st.markdown(f'<div class="card"><div class="l">{label}</div><div class="v">{value}</div><div class="s">{sub}</div></div>',unsafe_allow_html=True)
def money(x): return "Not verified" if pd.isna(x) else f"${x:,.0f}"
def download(label,path,mime):
    if path.exists():
        with open(path,"rb") as f: st.download_button(label,f.read(),file_name=path.name,mime=mime,use_container_width=True)

if page=="Executive Dashboard":
    cols=st.columns(5)
    vals=[("Priority markets","50","GCC + Africa universe"),("Wave 1","6","UAE, Saudi, South Africa, Kuwait, Morocco, Qatar"),("Golden accounts","1,000","Segmented target-company model"),("Pilot POs","2–6","90-day scenario target"),("Core HS","950440","Playing cards")]
    for c,v in zip(cols,vals):
        with c: card(*v)
    st.markdown('<div class="note"><b>Execution principle:</b> 50 markets are the intelligence universe, not a simultaneous rollout. First build export proof in six markets, then scale by response, RFQ, sample and reorder economics.</div>',unsafe_allow_html=True)
    if not C.empty:
        x,y=st.columns([1.4,1])
        with x:
            top=C.sort_values("Score /100",ascending=False).head(12)
            fig=px.bar(top.sort_values("Score /100"),x="Score /100",y="Country",orientation="h",text="Score /100",title="Top market-attractiveness scores"); fig.update_traces(marker_color="#E31B23"); fig.update_layout(height=470,plot_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
        with y:
            tc=C["Tier"].value_counts().reindex(["A","B","C","D"]).fillna(0); fig=go.Figure(go.Pie(labels=tc.index,values=tc.values,hole=.58,marker=dict(colors=["#E31B23","#B68A3A","#75666B","#D7D1D3"]))); fig.update_layout(title="50-market portfolio by tier",height=470); st.plotly_chart(fig,use_container_width=True)
    st.markdown("### Strategic thesis")
    c1,c2,c3=st.columns(3); c1.write("**Avoid the commodity trap.** Core opens doors; BrandLab, destination and heritage lines build margin."); c2.write("**Build two regional hubs.** UAE for GCC and South Africa for Southern Africa where partner economics support it."); c3.write("**Export proof before broad scale.** Qualified buyer → RFQ → sample → pilot PO → reorder/case study.")

elif page=="Market Intelligence":
    st.subheader("50-country market intelligence")
    if C.empty: st.warning("Country dataset unavailable.")
    else:
        a,b,c=st.columns(3); tiers=a.multiselect("Tier",["A","B","C","D"],default=["A","B","C","D"]); regions=b.multiselect("Region",sorted(C["Region"].dropna().unique()),default=sorted(C["Region"].dropna().unique())); q=c.text_input("Search")
        V=C[C["Tier"].isin(tiers)&C["Region"].isin(regions)].copy()
        if q: V=V[V.astype(str).apply(lambda r:r.str.lower().str.contains(q.lower()).any(),axis=1)]
        cols=["Rank","Tier","Country","Region","HS950440 Import USD","Data Year","Score /100","Product Focus","Country Positioning","3-Day Reply Potential"]; st.dataframe(V[cols],use_container_width=True,hide_index=True,column_config={"HS950440 Import USD":st.column_config.NumberColumn(format="$%d"),"Score /100":st.column_config.ProgressColumn(min_value=0,max_value=100)})
        country=st.selectbox("Country drill-down",V["Country"].tolist() if not V.empty else C["Country"].tolist()); r=C[C["Country"]==country].iloc[0]; d1,d2,d3,d4=st.columns(4); d1.metric("Rank",int(r["Rank"])); d2.metric("Tier",r["Tier"]); d3.metric("Import signal",money(r["HS950440 Import USD"])); d4.metric("Score",f'{int(r["Score /100"])} / 100'); st.write(f"**Positioning:** {r['Country Positioning']}"); st.write(f"**Product focus:** {r['Product Focus']}"); st.write(f"**Trade route:** {r['Potential Trade Route']}")
        rc=["Demand /30","Trade /20","Fit /20","Logistics /15","Risk /15"]; caps=[30,20,20,15,15]; rv=[float(r[k])/m*100 for k,m in zip(rc,caps)]; labs=["Demand","Trade","Fit","Logistics","Risk quality"]; fig=go.Figure(go.Scatterpolar(r=rv+[rv[0]],theta=labs+[labs[0]],fill="toself",line_color="#E31B23")); fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])),showlegend=False,height=420); st.plotly_chart(fig,use_container_width=True); st.caption("Scores are decision-support heuristics, not guaranteed outcomes or sovereign-risk ratings.")

elif page=="SWOT & Positioning":
    st.markdown('<div class="good"><b>Master positioning:</b> Cards Club — a regional design-to-deck manufacturing partner for brands, distributors, retailers, hotels and destinations across the Middle East and Africa.</div>',unsafe_allow_html=True)
    st.write("**Architecture:** Core · Heritage · Destinations · Seasons · BrandLab · Collector")
    a,b=st.columns(2)
    for i,k in enumerate(["Strengths","Weaknesses","Opportunities","Threats"]):
        with [a,b][i%2]:
            st.markdown(f"### {k}"); [st.write("• "+x) for x in SWOT[k]]
    st.markdown("### Competitive frame"); st.write("Do not compete as the cheapest deck. Position Cards Club between anonymous commodity suppliers and high-price imported premium brands: closer, flexible, customizable, culturally relevant and export-oriented.")

elif page=="Products & Offers":
    st.subheader("Product & offer architecture")
    if not P.empty: st.dataframe(P,use_container_width=True,hide_index=True)
    st.write("**Commercial ladder:** Trial MOQ → Standard MOQ → Strategic Distributor MOQ. Price as EXW → FOB → CIF with quote validity and freight separated.")
    st.write("**Margin priority:** BrandLab → Destination → Heritage → Core. **Volume priority:** Core → Private Label → Tourism/Destination → Heritage.")

elif page=="Golden 1000":
    st.subheader("Golden 1000 account model")
    if not G.empty:
        st.dataframe(G,use_container_width=True,hide_index=True); fig=px.pie(G,values="Target Accounts",names="Segment",hole=.5,title="Account allocation by segment"); st.plotly_chart(fig,use_container_width=True)
    wave=pd.DataFrame({"Market":["UAE","Saudi Arabia","South Africa","Kuwait","Morocco","Qatar"],"Accounts":[100,100,70,50,50,40],"Angle":["Distributor + BrandLab + Hospitality","Distributor + BrandLab + Ramadan","Distributor + Retail + Private Label","Premium retail + gifting","Tourism + distributor","Hospitality + corporate"]}); st.markdown("### Wave 1"); st.dataframe(wave,hide_index=True,use_container_width=True); st.markdown('<div class="note"><b>Outbound rule:</b> no 1,000-contact blast. Split by country × segment × offer; use 1–2 decision makers/account; optimize positive reply, RFQ and sample rates.</div>',unsafe_allow_html=True)

elif page=="90-Day Roadmap":
    st.subheader("90-day execution")
    if not M.empty: st.dataframe(M,use_container_width=True,hide_index=True); fig=px.bar(M,x="Phase",y="Workstream",orientation="h",text="Timing",title="Execution sequence"); fig.update_traces(marker_color="#E31B23"); fig.update_layout(height=620,yaxis=dict(autorange="reversed")); st.plotly_chart(fig,use_container_width=True)
    st.write("**Gate 1:** no mass outbound before data/compliance cleanup. **Gate 2:** no final price promise before origin, freight and customs validation. **Gate 3:** no shipment before payment security, conformity and QC approval.")

elif page=="Risk Register":
    st.subheader("Export risk register")
    if not R.empty:
        order=["Critical","High","Medium","Low"]; sel=st.multiselect("Severity",order,default=order); V=R[R["Severity"].isin(sel)]; st.dataframe(V,use_container_width=True,hide_index=True); counts=V["Severity"].value_counts().reindex(order).fillna(0); fig=px.bar(x=counts.index,y=counts.values,labels={"x":"Severity","y":"Risks"}); fig.update_traces(marker_color="#E31B23"); st.plotly_chart(fig,use_container_width=True)
        for _,r in R[R["Severity"].isin(["Critical","High"])].head(12).iterrows():
            with st.expander(f"{r['ID']} · {r['Risk']} — {r['Severity']}"): st.write(f"**Impact:** {r['Impact']}"); st.write(f"**Mitigation:** {r['Mitigation']}"); st.write(f"**Owner:** {r['Owner']} · **Gate:** {r['Deadline / Gate']}")

elif page=="Customs & Trade":
    st.markdown('<div class="note"><b>Non-negotiable:</b> never market “zero customs guaranteed.” Preferential treatment depends on HS classification, current agreement implementation, Rules of Origin, origin evidence and destination-customs acceptance.</div>',unsafe_allow_html=True)
    if not T.empty: st.dataframe(T,use_container_width=True,hide_index=True)
    st.markdown("### Pre-shipment gate")
    for i,x in enumerate(["Confirm destination HS classification","Confirm agreement + Rules of Origin","Confirm marking/conformity route","Approve invoice + packing list + COO route","Confirm payment security + Incoterm","Approve Golden Sample / batch QC","Validate freight, insurance, transit time and quote validity"],1): st.checkbox(f"{i}. {x}",key=f"gate{i}")

elif page=="Email Campaigns":
    st.subheader("7 outbound campaign angles"); n=st.selectbox("Campaign",list(EMAILS)); subject,preview,body=EMAILS[n]; a,b=st.columns(2); a.code(subject,language=None); b.code(preview,language=None); st.text_area("Template",body,height=290); st.caption("Use as a segment-specific starting point; personalize account context and keep the first CTA low-friction.")

elif page=="Sales Scenarios":
    st.subheader("90-day sales scenarios"); st.caption("Operating scenarios, not guaranteed forecasts."); st.dataframe(pd.DataFrame([["Conservative",1000,"15–25","2–5","0–1"],["Base",1000,"30–50","6–15","2–4"],["Strong",1000,"50–80+","12–25","5–8"]],columns=["Scenario","Target companies","Replies","Qualified buyers","Pilot POs"]),hide_index=True,use_container_width=True); st.write("**KPI tree:** Deliverability → Reply → Positive reply → Qualified buyer → RFQ → Sample → PO → Gross margin → Reorder."); st.write("**72-hour goal:** buyer interest, catalog/RFQ/sample intent — not assuming closed orders from cold email.")

elif page=="Files & Sources":
    st.subheader("Project files & sources"); a,b,c=st.columns(3)
    with a: download("Download Export Command Center",DATA,"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with b: download("Download Company Profile",PROFILE,"application/pdf")
    with c: download("Download Links Document",LINKS,"application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.markdown('<div class="note"><b>Security:</b> the original Local & global data workbook is intentionally not published because it contains sensitive credentials/banking-related information. The app uses the sanitized export command-center dataset.</div>',unsafe_allow_html=True)
    if not S.empty: st.dataframe(S,use_container_width=True,hide_index=True)
