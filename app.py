from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Cards Club Export Growth Study", page_icon="🂡", layout="wide", initial_sidebar_state="expanded")
ROOT=Path(__file__).parent
DATA=ROOT/"data"/"Cards_Club_International_Export_Command_Center.xlsx"
LOGO=ROOT/"assets"/"cards-club-logo.png"
PROFILE=ROOT/"assets"/"CP-Cards-Club-14-07-2026.pdf"
LINKS=ROOT/"assets"/"Cards-Club-links.docx"

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"]{background:#fbfdfb}
[data-testid="stSidebar"]{border-right:1px solid #d9e4dc;background:#0b0e0c}
[data-testid="stSidebar"] *{color:#f6fff8}
.block-container{max-width:1600px;padding-top:1rem;padding-bottom:2rem}
.hero{background:linear-gradient(135deg,#080b09 0%,#111713 68%,#a6f3b5 180%);border:1px solid #27352b;border-radius:24px;padding:30px 32px;margin-bottom:18px;box-shadow:0 14px 40px rgba(0,0,0,.12)}
.hero h1{color:#fff;margin:6px 0 0;font-size:2.2rem}.hero p{color:#dce8df;line-height:1.9;margin:.7rem 0 0}.tag{display:inline-block;background:#c9ffd5;color:#07150b;border-radius:999px;padding:5px 11px;margin-right:6px;font-size:.76rem;font-weight:850}
.kpi{background:#fff;border:1px solid #dce7df;border-radius:16px;padding:16px 18px;min-height:128px;box-shadow:0 6px 18px rgba(10,30,18,.05)}
.kpi .label{font-size:.82rem;color:#58675e}.kpi .value{font-size:1.46rem;font-weight:850;color:#0c1710;margin:.3rem 0}.kpi .note{font-size:.78rem;color:#6b786f;line-height:1.55}
.panel{background:#fff;border:1px solid #dce7df;border-radius:16px;padding:18px 20px;margin:.55rem 0 1rem}.good{border-left:5px solid #61d881;background:#f3fff6}.warn{border-left:5px solid #e5b34f;background:#fffaf0}.risk{border-left:5px solid #db6a6a;background:#fff5f5}.small{font-size:.82rem;color:#657169}.titleline{font-weight:900;font-size:1.1rem;color:#0b1710;margin-bottom:.3rem}.cta{display:inline-block;background:#a6f3b5;color:#07150b;padding:9px 14px;border-radius:10px;font-weight:900}.pill{display:inline-block;border:1px solid #cfe5d4;border-radius:999px;padding:4px 9px;margin:2px;background:#f6fff8}.mono{direction:ltr;text-align:left;font-family:monospace;white-space:pre-wrap;background:#0c120e;color:#dfffea;border-radius:12px;padding:14px}
div[data-testid="stMetric"]{background:white;border:1px solid #dce7df;padding:12px;border-radius:14px}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data():
    if not DATA.exists(): return {}
    sheets=["Country Priority","Product Strategy","Risk Register","90 Day Roadmap","Golden 1000","Customs & Trade","Sources"]
    out={}
    for s in sheets:
        try: out[s]=pd.read_excel(DATA,sheet_name=s,header=3)
        except Exception: out[s]=pd.DataFrame()
    return out

D=load_data(); C=D.get("Country Priority",pd.DataFrame()); P=D.get("Product Strategy",pd.DataFrame()); R=D.get("Risk Register",pd.DataFrame()); M=D.get("90 Day Roadmap",pd.DataFrame()); G=D.get("Golden 1000",pd.DataFrame()); T=D.get("Customs & Trade",pd.DataFrame()); S=D.get("Sources",pd.DataFrame())
if not C.empty:
    C=C[pd.to_numeric(C.get("Rank"),errors="coerce").notna()].copy(); C["Rank"]=pd.to_numeric(C["Rank"]).astype(int); C["Score /100"]=pd.to_numeric(C["Score /100"],errors="coerce"); C["HS950440 Import USD"]=pd.to_numeric(C["HS950440 Import USD"],errors="coerce")
if not R.empty: R=R[R.get("ID").astype(str).str.match(r"R\d+",na=False)].copy()
if not M.empty: M=M[pd.to_numeric(M.get("Phase"),errors="coerce").notna()].copy()
if not G.empty: G=G[pd.to_numeric(G.get("Target Accounts"),errors="coerce").notna()].copy(); G["Target Accounts"]=pd.to_numeric(G["Target Accounts"])
if not T.empty: T=T[T.get("Framework").notna() & ~T.get("Framework").astype(str).isin(["Step","Mandatory pre-shipment gate"])].copy()
if not S.empty: S=S[S.get("Source").notna()].copy()

SWOT={
"Strengths":["Made-in-Egypt manufacturing base close to GCC and Africa","Standard + heritage + tourism + seasonal + custom portfolio","Customization reduces commodity-only price pressure","Egyptian cultural storytelling creates differentiated creative value","Potential preferential regional trade routes subject to origin rules"],
"Weaknesses":["Limited international export proof versus established suppliers","Master-data inconsistencies require cleanup before buyer use","Full EXW/FOB/CIF pricing governance still needs validation","B2B case studies and distributor references are limited","Some operational claims require verification"],
"Opportunities":["Cards Club BrandLab for corporate/private-label business","Hotels, resorts, museums, duty-free and tourism souvenir decks","UAE as GCC hub and South Africa as Southern Africa hub","Localized Ramadan, wildlife and destination editions","Importers, gifting agencies, hospitality and direct strategic brands"],
"Threats":["China and scale suppliers dominate pure price competition","Compliance/origin errors can stop shipments or remove tariff benefits","FX, freight and payment risk can erase margin","Weak exclusivity contracts can lock a market","IP, cultural sensitivity and gambling perception create friction"]}

EMAILS={
"Distributor Acquisition":("Playing cards for {{Country}}","Standard, cultural and private-label decks manufactured in Egypt.","Hi {{FirstName}},\n\nCards Club manufactures premium playing cards in Egypt for retail, distribution and private-label programs. We offer standard Bridge decks, cultural collections and fully customized editions.\n\nWe're opening selected distribution partnerships in {{Country}}, and {{Company}} looks relevant.\n\nWould it be useful if I sent our distributor range, MOQ and export pricing?\n\nBest,\nCards Club Export Team"),
"Regional Supplier Alternative":("A closer deck supplier","Regional production instead of another long Asian supply chain.","Hi {{FirstName}},\n\nIf your playing-card range currently comes from Asia or Europe, Cards Club offers a manufacturing alternative from Egypt. We produce standard and custom decks with flexible branding, packaging and regional export support.\n\nIf you share the product you currently buy, I can prepare a like-for-like commercial comparison.\n\nBest,\nCards Club Export Team"),
"Corporate BrandLab":("52 branded touchpoints","Not another promotional giveaway.","Hi {{FirstName}},\n\nA custom playing-card deck puts {{Company}} across 52 usable, collectible brand touchpoints — from the cards to the packaging. Cards Club handles concept, design and manufacturing in Egypt.\n\nWould you like us to create one sample concept for {{Company}}?\n\nBest,\nCards Club BrandLab"),
"Hotels & Resorts":("Your hotel as a collectible deck","Guest entertainment, souvenir and branded gift in one product.","Hi {{FirstName}},\n\nWe manufacture custom playing-card decks for hospitality and tourism brands. A {{Hotel}} edition can feature the property, destination and local landmarks for guest rooms, VIP gifts and retail.\n\nWould you like to see three creative directions?\n\nBest,\nCards Club Export Team"),
"Tourism / Souvenir":("Put {{City}} in their pocket","A souvenir travelers can actually use.","Hi {{FirstName}},\n\nCards Club creates destination decks inspired by local culture, landmarks and stories. We'd like to explore a {{Destination}} edition with {{Company}}.\n\nShould I send a sample concept?\n\nBest,\nCards Club Export Team"),
"Seasonal / Ramadan":("52 moments for Ramadan","A limited branded edition built for gifting.","Hi {{FirstName}},\n\nCards Club creates premium seasonal decks for corporate gifting and brand campaigns. We can build a Ramadan edition around {{Company}} — artwork, packaging and production.\n\nWould you like a visual direction?\n\nBest,\nCards Club BrandLab"),
"Breakup / Re-engagement":("Close {{Country}}?","Last note from me.","Hi {{FirstName}},\n\nI haven't heard back, so I'll close the conversation. We're selecting distribution and custom-deck partners in {{Country}}, and {{Company}} was still on our shortlist.\n\nIf relevant, reply CATALOG and I'll send everything over.\n\nBest,\nCards Club Export Team")}

def kpi(label,value,note): st.markdown(f'<div class="kpi"><div class="label">{label}</div><div class="value">{value}</div><div class="note">{note}</div></div>',unsafe_allow_html=True)
def money(x): return "Not verified" if pd.isna(x) else f"${x:,.0f}"
def download(label,path,mime):
    if path.exists():
        with open(path,"rb") as f: st.download_button(label,f.read(),file_name=path.name,mime=mime,use_container_width=True)

if LOGO.exists():
    c1,c2=st.columns([1,6]); c1.image(str(LOGO),use_container_width=True)
    with c2: st.markdown('<div class="hero"><span class="tag">GCC + AFRICA</span><span class="tag">HS 950440</span><h1>Cards Club Export Growth Study</h1><p><b>From Concept to Deck.</b><br>Market intelligence, export readiness, customs control, Golden 1000 account strategy and 90-day execution roadmap.</p></div>',unsafe_allow_html=True)
else:
    st.markdown('<div class="hero"><span class="tag">GCC + AFRICA</span><span class="tag">HS 950440</span><h1>Cards Club Export Growth Study</h1><p><b>From Concept to Deck.</b><br>Market intelligence, export readiness, customs control, Golden 1000 account strategy and 90-day execution roadmap.</p></div>',unsafe_allow_html=True)

page=st.sidebar.radio("Navigate",["Executive Dashboard","Market Intelligence","SWOT & Positioning","Products & Offers","Golden 1000","90-Day Roadmap","Risk Register","Customs & Trade","Email Campaigns","Sales Scenarios","Files & Sources"])
st.sidebar.caption("Research snapshot: Sep 2026. Re-validate tariffs, conformity and buyer data before live shipment.")

if page=="Executive Dashboard":
    cs=st.columns(5)
    vals=[("Priority Markets","50","GCC + Africa universe"),("Wave 1","6","UAE, Saudi, South Africa, Kuwait, Morocco, Qatar"),("Golden Accounts","1,000","Segmented target-company model"),("Pilot POs","2–6","90-day scenario, not guarantee"),("Core HS","950440","Playing cards")]
    for c,v in zip(cs,vals):
        with c:kpi(*v)
    st.markdown('<div class="panel good"><div class="titleline">Execution principle</div>50 markets are the intelligence universe, not a simultaneous rollout. Build export proof in six markets, then scale by reply quality, RFQ, sample conversion, margin and reorder economics.</div>',unsafe_allow_html=True)
    if not C.empty:
        a,b=st.columns([1.45,1])
        with a:
            top=C.sort_values("Score /100",ascending=False).head(12)
            fig=px.bar(top.sort_values("Score /100"),x="Score /100",y="Country",orientation="h",text="Score /100",title="Top market-attractiveness scores"); fig.update_traces(marker_color="#61d881"); fig.update_layout(height=470,plot_bgcolor="white",paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
        with b:
            tc=C["Tier"].value_counts().reindex(["A","B","C","D"]).fillna(0); fig=go.Figure(go.Pie(labels=tc.index,values=tc.values,hole=.58,marker=dict(colors=["#61d881","#a6f3b5","#90a697","#d7dfd9"]))); fig.update_layout(title="50-market portfolio by tier",height=470,paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
    x,y,z=st.columns(3); x.markdown('<div class="panel"><div class="titleline">Avoid the commodity trap</div>Core opens doors; BrandLab, destination and heritage lines build margin.</div>',unsafe_allow_html=True); y.markdown('<div class="panel"><div class="titleline">Build regional hubs</div>UAE for GCC and South Africa for Southern Africa where partner economics support it.</div>',unsafe_allow_html=True); z.markdown('<div class="panel"><div class="titleline">Export proof before scale</div>Qualified buyer → RFQ → sample → pilot PO → reorder → case study.</div>',unsafe_allow_html=True)

elif page=="Market Intelligence":
    st.subheader("50-country market intelligence")
    if C.empty: st.warning("Country dataset unavailable.")
    else:
        a,b,c=st.columns(3); tiers=a.multiselect("Tier",["A","B","C","D"],default=["A","B","C","D"]); regions=b.multiselect("Region",sorted(C["Region"].dropna().unique()),default=sorted(C["Region"].dropna().unique())); q=c.text_input("Search")
        V=C[C["Tier"].isin(tiers)&C["Region"].isin(regions)].copy()
        if q: V=V[V.astype(str).apply(lambda r:r.str.lower().str.contains(q.lower()).any(),axis=1)]
        cols=["Rank","Tier","Country","Region","HS950440 Import USD","Data Year","Score /100","Product Focus","Country Positioning","3-Day Reply Potential"]
        st.dataframe(V[cols],use_container_width=True,hide_index=True,column_config={"HS950440 Import USD":st.column_config.NumberColumn(format="$%d"),"Score /100":st.column_config.ProgressColumn(min_value=0,max_value=100)})
        country=st.selectbox("Country drill-down",V["Country"].tolist() if not V.empty else C["Country"].tolist()); r=C[C["Country"]==country].iloc[0]
        d1,d2,d3,d4=st.columns(4); d1.metric("Rank",int(r["Rank"])); d2.metric("Tier",r["Tier"]); d3.metric("Import signal",money(r["HS950440 Import USD"])); d4.metric("Score",f'{int(r["Score /100"])} / 100')
        st.markdown(f'<div class="panel"><b>Positioning:</b> {r["Country Positioning"]}<br><b>Product focus:</b> {r["Product Focus"]}<br><b>Trade route:</b> {r["Potential Trade Route"]}</div>',unsafe_allow_html=True)
        rc=["Demand /30","Trade /20","Fit /20","Logistics /15","Risk /15"]; caps=[30,20,20,15,15]; rv=[float(r[k])/m*100 for k,m in zip(rc,caps)]; labs=["Demand","Trade","Fit","Logistics","Risk quality"]
        fig=go.Figure(go.Scatterpolar(r=rv+[rv[0]],theta=labs+[labs[0]],fill="toself",line_color="#61d881")); fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])),showlegend=False,height=430,paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True); st.caption("Scores are decision-support heuristics, not guaranteed outcomes or sovereign-risk ratings.")

elif page=="SWOT & Positioning":
    st.markdown('<div class="panel good"><div class="titleline">Master positioning</div>Cards Club — a regional design-to-deck manufacturing partner for brands, distributors, retailers, hotels and destinations across the Middle East and Africa.</div>',unsafe_allow_html=True)
    st.write("**Architecture:** Core · Heritage · Destinations · Seasons · BrandLab · Collector")
    a,b=st.columns(2)
    for i,k in enumerate(["Strengths","Weaknesses","Opportunities","Threats"]):
        with [a,b][i%2]: st.markdown(f"### {k}"); [st.write("• "+x) for x in SWOT[k]]
    st.markdown('<div class="panel"><div class="titleline">Competitive frame</div>Do not compete as the cheapest deck. Position Cards Club between anonymous commodity suppliers and expensive imported premium brands: closer, flexible, customizable, culturally relevant and export-oriented.</div>',unsafe_allow_html=True)

elif page=="Products & Offers":
    st.subheader("Product & offer architecture")
    if not P.empty: st.dataframe(P,use_container_width=True,hide_index=True)
    st.markdown('<div class="panel"><b>Commercial ladder:</b> Trial MOQ → Standard MOQ → Strategic Distributor MOQ.<br><b>Pricing:</b> EXW → FOB → CIF with quote validity and freight separated.<br><b>Margin priority:</b> BrandLab → Destination → Heritage → Core.<br><b>Volume priority:</b> Core → Private Label → Tourism/Destination → Heritage.</div>',unsafe_allow_html=True)

elif page=="Golden 1000":
    st.subheader("Golden 1000 account model")
    if not G.empty:
        st.dataframe(G,use_container_width=True,hide_index=True); fig=px.pie(G,values="Target Accounts",names="Segment",hole=.5,title="Account allocation by segment",color_discrete_sequence=["#61d881","#a6f3b5","#7d9b84","#cfe5d4","#35543e","#9fb6a5","#dce7df"]); st.plotly_chart(fig,use_container_width=True)
    wave=pd.DataFrame({"Market":["UAE","Saudi Arabia","South Africa","Kuwait","Morocco","Qatar"],"Accounts":[100,100,70,50,50,40],"Angle":["Distributor + BrandLab + Hospitality","Distributor + BrandLab + Ramadan","Distributor + Retail + Private Label","Premium retail + gifting","Tourism + distributor","Hospitality + corporate"]}); st.markdown("### Wave 1"); st.dataframe(wave,hide_index=True,use_container_width=True)
    st.markdown('<div class="panel warn"><div class="titleline">Outbound rule</div>No 1,000-contact blast. Split by country × segment × offer. Start with 1–2 decision makers per company and optimize positive reply, RFQ and sample rates.</div>',unsafe_allow_html=True)

elif page=="90-Day Roadmap":
    st.subheader("90-day execution roadmap")
    if not M.empty:
        st.dataframe(M,use_container_width=True,hide_index=True); fig=px.bar(M,x="Phase",y="Workstream",orientation="h",text="Timing",title="Execution sequence"); fig.update_traces(marker_color="#61d881"); fig.update_layout(height=620,yaxis=dict(autorange="reversed"),plot_bgcolor="white",paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="panel risk"><div class="titleline">Hard gates</div>1) No mass outbound before data/compliance cleanup. 2) No final price promise before origin, freight and customs validation. 3) No shipment before payment security, conformity and QC approval.</div>',unsafe_allow_html=True)

elif page=="Risk Register":
    st.subheader("Export risk register")
    if not R.empty:
        order=["Critical","High","Medium","Low"]; sel=st.multiselect("Severity",order,default=order); V=R[R["Severity"].isin(sel)]; st.dataframe(V,use_container_width=True,hide_index=True)
        counts=V["Severity"].value_counts().reindex(order).fillna(0); fig=px.bar(x=counts.index,y=counts.values,labels={"x":"Severity","y":"Risks"}); fig.update_traces(marker_color="#61d881"); fig.update_layout(plot_bgcolor="white",paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
        for _,r in R[R["Severity"].isin(["Critical","High"])].head(12).iterrows():
            with st.expander(f"{r['ID']} · {r['Risk']} — {r['Severity']}"): st.write(f"**Impact:** {r['Impact']}"); st.write(f"**Mitigation:** {r['Mitigation']}"); st.write(f"**Owner:** {r['Owner']} · **Gate:** {r['Deadline / Gate']}")

elif page=="Customs & Trade":
    st.markdown('<div class="panel warn"><div class="titleline">Non-negotiable</div>Never market “zero customs guaranteed.” Preferential treatment depends on HS classification, current agreement implementation, Rules of Origin, origin evidence and destination-customs acceptance.</div>',unsafe_allow_html=True)
    if not T.empty: st.dataframe(T,use_container_width=True,hide_index=True)
    st.markdown("### Pre-shipment gate")
    for i,x in enumerate(["Confirm destination HS classification","Confirm agreement + Rules of Origin","Confirm marking/conformity route","Approve invoice + packing list + COO route","Confirm payment security + Incoterm","Approve Golden Sample / batch QC","Validate freight, insurance, transit time and quote validity"],1): st.checkbox(f"{i}. {x}",key=f"gate{i}")

elif page=="Email Campaigns":
    st.subheader("7 outbound campaign angles"); n=st.selectbox("Campaign",list(EMAILS)); subject,preview,body=EMAILS[n]
    a,b=st.columns(2); a.markdown(f'<div class="panel"><div class="small">SUBJECT</div><div class="titleline">{subject}</div></div>',unsafe_allow_html=True); b.markdown(f'<div class="panel"><div class="small">PREVIEW</div><div class="titleline">{preview}</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="mono">{body}</div>',unsafe_allow_html=True); st.caption("Use as a segment-specific starting point; personalize account context and keep the first CTA low-friction.")

elif page=="Sales Scenarios":
    st.subheader("90-day sales scenarios"); st.caption("Operating scenarios, not guaranteed forecasts.")
    st.dataframe(pd.DataFrame([["Conservative",1000,"15–25","2–5","0–1"],["Base",1000,"30–50","6–15","2–4"],["Strong",1000,"50–80+","12–25","5–8"]],columns=["Scenario","Target companies","Replies","Qualified buyers","Pilot POs"]),hide_index=True,use_container_width=True)
    st.markdown('<div class="panel good"><b>KPI tree:</b> Deliverability → Reply → Positive reply → Qualified buyer → RFQ → Sample → PO → Gross margin → Reorder.<br><b>72-hour goal:</b> buyer interest, catalog/RFQ/sample intent — not assuming closed orders from cold email.</div>',unsafe_allow_html=True)

elif page=="Files & Sources":
    st.subheader("Project files & sources"); a,b,c=st.columns(3)
    with a: download("Download Export Command Center",DATA,"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with b: download("Download Company Profile",PROFILE,"application/pdf")
    with c: download("Download Links Document",LINKS,"application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.markdown('<div class="panel risk"><div class="titleline">Security</div>The original Local & global data workbook is intentionally not published because it contains sensitive credentials/banking-related information. The app uses the sanitized export command-center dataset.</div>',unsafe_allow_html=True)
    if not S.empty: st.dataframe(S,use_container_width=True,hide_index=True)
