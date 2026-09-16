from pathlib import Path
import ast
import csv

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
DATA = ROOT / "data"

# Syntax validation without importing Streamlit.
ast.parse(APP.read_text(encoding="utf-8"), filename=str(APP))

required = {
    "countries.csv": {"Rank", "Tier", "Country", "Score /100", "Product Focus", "Country Positioning"},
    "products.csv": {"Product / Line", "Architecture", "Primary Buyer"},
    "risks.csv": {"ID", "Risk", "Severity", "Impact", "Mitigation"},
    "roadmap.csv": {"Phase", "Timing", "Workstream", "Actions", "Deliverable", "Success Metric"},
    "golden1000.csv": {"Segment", "Target Accounts", "Decision Makers", "Best Offer"},
    "trade.csv": {"Framework", "Markets", "Execution Rule"},
    "sources.csv": {"Source", "Use", "URL / File"},
}

for name, expected in required.items():
    path = DATA / name
    if not path.exists():
        raise SystemExit(f"Missing required file: {name}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = set(reader.fieldnames or [])
        missing = expected - headers
        if missing:
            raise SystemExit(f"{name}: missing columns {sorted(missing)}")
        rows = list(reader)
        if not rows:
            raise SystemExit(f"{name}: no data rows")
        print(f"OK {name}: {len(rows)} rows")

print("OK app.py syntax")
print("Cards Club smoke test passed")
