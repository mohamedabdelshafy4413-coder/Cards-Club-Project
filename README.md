# Cards Club International Export Command Center

Streamlit decision-support application for Cards Club expansion across GCC and Africa.

## Positioning
**Cards Club — From Concept to Deck.**

Regional design-to-deck manufacturing partner for brands, distributors, retailers, hotels and destinations.

## What is inside
- 50-country market-priority model for HS 950440
- Product / offer architecture: Core, Heritage, Destinations, Seasons and BrandLab
- SWOT and positioning system
- Golden 1000 target-account model
- 90-day export GTM roadmap
- 25-risk export register with mitigations
- Customs / Rules-of-Origin control layer
- 7 outbound email campaign angles
- Sales scenarios and KPI logic

## Performance architecture
The app loads small CSV datasets lazily with Streamlit caching. Heavy XLSX parsing, `openpyxl`, and Plotly were removed from the runtime to reduce cold-start time and rerun cost.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud
Use:
- Repository: `mohamedabdelshafy4413-coder/Cards-Club-Project`
- Branch: `main`
- Main file: `app.py`

## Security
Raw working spreadsheets containing credentials or banking-related data are intentionally excluded from this public repository. Only sanitized commercial datasets are published.
