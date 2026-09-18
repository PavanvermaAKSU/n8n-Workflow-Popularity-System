from main import SessionLocal, Workflow


db = SessionLocal()

platforms = [
    "youtube",
    "n8n_forum",
    "google_trends"
]

for platform in platforms:
    records = (
        db.query(Workflow)
        .filter(Workflow.source_platform == platform)
        .all()
    )

    if not records:
        continue

    scores = [
        float(record.popularity_score or 0)
        for record in records
    ]

    minimum = min(scores)
    maximum = max(scores)

    for record in records:
        score = float(record.popularity_score or 0)

        if maximum > minimum:
            overall = (
                (score - minimum)
                / (maximum - minimum)
            ) * 100
        else:
            overall = 0

        record.overall_score = round(overall, 2)

db.commit()
db.close()

print("Overall scores calculated successfully.")