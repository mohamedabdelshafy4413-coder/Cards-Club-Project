# Runtime data

The Streamlit dashboard uses small sanitized CSV files for faster cold starts and page navigation:

- `countries.csv` — 50-country market prioritization and scoring
- `products.csv` — product / offer architecture
- `risks.csv` — export risk register and mitigations
- `roadmap.csv` — 90-day execution roadmap
- `golden1000.csv` — account-segment allocation
- `trade.csv` — customs / trade frameworks and controls
- `sources.csv` — research source register

## Security
The original uploaded `Local & global data .xlsx` is intentionally **not published** because it contains sensitive credentials / banking-related information and inconsistent raw operational fields. The app only uses sanitized commercial data.

## Data governance
Import values are historical HS 950440 trade signals and should be refreshed before live commercial decisions. Tariff advantages are conditional on product classification, Rules of Origin, documentation and destination-customs acceptance.
