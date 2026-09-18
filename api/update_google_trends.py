import json

from main import SessionLocal, Workflow


with open("../google_trends_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

db = SessionLocal()

updated = 0

for record in data:
    keyword = record.get("keyword")
    country = record.get("country")

    external_id = f"{keyword}_{country}"

    workflow = (
        db.query(Workflow)
        .filter(
            Workflow.external_id == external_id,
            Workflow.source_platform == "google_trends"
        )
        .first()
    )

    if not workflow:
        continue

    workflow.current_interest = record.get("current_interest", 0)
    workflow.average_interest = record.get("average_interest", 0)
    workflow.growth_percent = record.get("growth_percent", 0)

    workflow.interest_score = record.get("interest_score", 0)
    workflow.average_score = record.get("average_score", 0)
    workflow.growth_score = record.get("growth_score", 0)

    updated += 1

db.commit()
db.close()

print(f"Google Trends records updated: {updated}")