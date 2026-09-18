import json
from pathlib import Path

from main import SessionLocal, Workflow


BASE_DIR = Path(__file__).resolve().parent.parent


def load_json(filename):
    path = BASE_DIR / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_records(data):
    # Direct list of records
    if isinstance(data, list):
        # n8n exported format:
        # [{"source": "...", "records": [...]}]
        if (
            len(data) > 0
            and isinstance(data[0], dict)
            and "records" in data[0]
        ):
            return data[0]["records"]

        # Normal list format:
        return data

    # Dictionary format:
    # {"records": [...]}
    if isinstance(data, dict):
        records = data.get("records", [])

        if isinstance(records, list):
            return records

    raise ValueError("Unsupported JSON format")

def record_exists(db, external_id, platform):
    return (
        db.query(Workflow)
        .filter(
            Workflow.external_id == external_id,
            Workflow.source_platform == platform
        )
        .first()
        is not None
    )


def import_youtube(db):
    data = load_json("youtube_data.json")
    records = extract_records(data)

    added = 0

    for record in records:

        external_id = str(
            record.get("video_id", "")
        )

        if not external_id:
            continue

        if record_exists(
            db,
            external_id,
            "youtube"
        ):
            continue

        workflow = Workflow(
            external_id=external_id,

            title=record.get("title"),

            description=record.get(
                "description"
            ),

            source_platform="youtube",

            source_url=record.get(
                "source_url"
            ),

            country=record.get(
                "country_segment",
                "unknown"
            ),

            views=int(
                record.get("views", 0)
            ),

            likes=int(
                record.get("likes", 0)
            ),

            comments=int(
                record.get("comments", 0)
            ),

            like_to_view_ratio=record.get(
                "like_to_view_ratio"
            ),

            comment_to_view_ratio=record.get(
                "comment_to_view_ratio"
            ),

            popularity_score=float(
                record.get(
                    "popularity_score",
                    0
                )
            ),

            collected_at=record.get(
                "collected_at"
            ),
        )

        db.add(workflow)
        added += 1

    return added


def import_forum(db):
    data = load_json("forum_data.json")
    records = extract_records(data)

    added = 0

    for record in records:

        external_id = str(
            record.get("forum_topic_id", "")
        )

        if not external_id:
            continue

        if record_exists(
            db,
            external_id,
            "n8n_forum"
        ):
            continue

        workflow = Workflow(
            external_id=external_id,

            title=record.get("title"),

            description=None,

            source_platform="n8n_forum",

            source_url=record.get("url"),

            country="unknown",

            views=int(
                record.get("views", 0)
            ),

            likes=int(
                record.get("likes", 0)
            ),

            replies=int(
                record.get("replies", 0)
            ),

            popularity_score=float(
                record.get(
                    "popularity_score",
                    0
                )
            ),

            collected_at=record.get(
                "collected_at"
            )
        )

        db.add(workflow)
        added += 1

    return added


def import_google_trends(db):
    data = load_json(
        "google_trends_data.json"
    )

    records = extract_records(data)

    added = 0

    for record in records:

        keyword = record.get(
            "keyword",
            ""
        )

        country = record.get(
            "country",
            "unknown"
        )

        if not keyword:
            continue

        external_id = (
            f"{keyword}_{country}"
        )

        if record_exists(
            db,
            external_id,
            "google_trends"
        ):
            continue

        workflow = Workflow(
            external_id=external_id,

            title=keyword,

            description=(
                f"Google Trends data for "
                f"{keyword} in {country}"
            ),

            source_platform="google_trends",

            source_url=(
                "https://trends.google.com/"
            ),

            country=country,

            views=0,
            likes=0,
            comments=0,
            replies=0,

            popularity_score=float(
                record.get(
                    "popularity_score",
                    0
                )
            ),

            collected_at=record.get(
                "collected_at"
            ),
            current_interest=float(record.get("current_interest", 0)),
            average_interest=float(record.get("average_interest", 0)),
            growth_percent=float(record.get("growth_percent", 0)),
            interest_score=float(record.get("interest_score", 0)),
            average_score=float(record.get("average_score", 0)),
            growth_score=float(record.get("growth_score", 0)),
        )

        db.add(workflow)
        added += 1

    return added


def main():

    db = SessionLocal()

    try:
        db.query(Workflow).delete()
        db.commit()

        youtube_added = import_youtube(db)

        forum_added = import_forum(db)

        google_added = import_google_trends(db)

        db.commit()

        total = (
            db.query(Workflow)
            .count()
        )

        print(
            f"YouTube added: {youtube_added}"
        )

        print(
            f"Forum added: {forum_added}"
        )

        print(
            f"Google Trends added: {google_added}"
        )

        print(
            f"Total records in database: {total}"
        )

    except Exception as error:

        db.rollback()

        print(
            f"Import failed: {error}"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()