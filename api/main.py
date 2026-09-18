from typing import Optional
from fastapi import FastAPI, HTTPException
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text
)
from sqlalchemy.orm import declarative_base, sessionmaker

# Database

DATABASE_URL = "sqlite:///./workflows.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}

)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit = False,
    autoflush=False
)

Base = declarative_base()

#Workflow Model 

class Workflow(Base):
    __tablename__ = "Workflows"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)

    source_platform = Column(String, index=True)
    source_url = Column(String, index=True)
    country = Column(String, nullable=True, index=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer,  default=0)
    replies = Column(Integer,  default=0)

    like_to_view_ratio = Column(Float, nullable=True)
    comment_to_view_ratio = Column(Float,nullable=True)
    popularity_score = Column(
        Float,
        default=0
    )

    current_interest = Column(Float, nullable= True)
    average_interest = Column(Float, nullable=True)
    growth_percent = Column(Float, nullable=True)

    interest_score = Column(Float, nullable=True)
    average_score = Column(Float, nullable=True)
    growth_score = Column(Float, nullable=True)

    overall_score = Column(Float, nullable=True)
    collected_at = Column(
        String,
        nullable=True
    )


Base.metadata.create_all(bind=engine)

#  FastAPI 

app = FastAPI(
    title="n8n Workflow Popularity API",
    description= (
        "API for discovering and ranking "
        "Popular n8n workflow using "
        "Youtube, n8n forum and google trends evidence"
    ),
    version="1.0.0"

)

# Helper

def workflow_to_dict(workflow):
    return{
        "id": workflow.id,
        "external_id": workflow.external_id,
        "title": workflow.title,
        "description": workflow.description,
        "source_platform": workflow.source_platform,
        "source_url": workflow.source_url,
        "country": workflow.country,
        "views": workflow.views,
        "likes": workflow.likes,
        "comments": workflow.comments,
        "replies": workflow.replies,
        "like_to_view_ratio":
            workflow.like_to_view_ratio,
        "comment_to_view_ratio":
            workflow.comment_to_view_ratio,
        "popularity_score":
            workflow.popularity_score,
        "overall_score":workflow.overall_score,
        "collected_at":
            workflow.collected_at
    }        


# Endpoints

@app.get("/")
def root():
    return{
        "message":"n8n Workflow Popularity API",
        "status":"running"
    }


@app.get("/workflows")
def get_workflows(
    platform:Optional[str] = None,
    country: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    db = SessionLocal()
    query = db.query(Workflow)
    if platform:
        query = query.filter(Workflow.source_platform == platform)

    if country:
        query = query.filter(Workflow.country == country)

    if keyword:
        query = query.filter(
            Workflow.title.ilike(f"%{keyword}%")
        )

    total = query.count()

    workflows = (
        query
        .order_by(Workflow.popularity_score.desc()
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    db.close()

    return{
        "total": total,
        "limit": limit,
        "offset":offset,
        "data":[workflow_to_dict(Workflow)
                for Workflow in workflows]
    }

@app.get("/workflows/top")
def get_top_workflows(
    limit: int= 10
):
    db = SessionLocal()

    workflows = (
        db.query(Workflow)
        .order_by(Workflow.popularity_score.desc())
        .limit(limit).all()
    )

    db.close()

    return[
        workflow_to_dict(workflow)
        for workflow in workflows
    ]

@app.get("/workflows/youtube")
def get_youtube_workflows(
    limit: int = 50
):
    db = SessionLocal()

    workflows = (
        db.query(Workflow)
        .filter(
            Workflow.source_platform == "youtube"
        )
        .order_by(
            Workflow.popularity_score.desc()
        )
        .limit(limit)
        .all()
    )

    db.close()

    return [
        workflow_to_dict(workflow)
        for workflow in workflows
    ]


@app.get("/workflows/forum")
def get_forum_workflows(
    limit: int = 50
):
    db = SessionLocal()

    workflows = (
        db.query(Workflow)
        .filter(
            Workflow.source_platform ==
            "n8n_forum"
        )
        .order_by(
            Workflow.popularity_score.desc()
        )
        .limit(limit)
        .all()
    )

    db.close()

    return [
        workflow_to_dict(workflow)
        for workflow in workflows
    ]


@app.get("/workflows/google")
def get_google_trends(
    limit: int = 50
):
    db = SessionLocal()

    workflows = (
        db.query(Workflow)
        .filter(
            Workflow.source_platform ==
            "google_trends"
        )
        .order_by(
            Workflow.popularity_score.desc()
        )
        .limit(limit)
        .all()
    )

    db.close()

    return [
        workflow_to_dict(workflow)
        for workflow in workflows
    ]

@app.post("/workflows/bulk")
def bulk_create_workflows(records: list[dict]):
    db = SessionLocal()
    added = 0
    skipped = 0

    try:
        for record in records:
            external_id = str(
                record.get("video_id")
                or record.get("forum_topic_id")
                or ""
            )

            platform = record.get("source_platform")

            if not external_id or not platform:
                skipped += 1
                continue

            exists = (
                db.query(Workflow)
                .filter(
                    Workflow.external_id == external_id,
                    Workflow.source_platform == platform
                )
                .first()
            )

            if exists:
                skipped += 1
                continue

            workflow = Workflow(
                external_id=external_id,
                title=record.get("title"),
                description=record.get("description"),
                source_platform=platform,
                source_url=record.get("source_url") or record.get("url"),
                
                country=(
                  record.get("country_segment")
                  or record.get("country")
                  or "unknown",
                ),
                views=int(record.get("views", 0)),
                likes=int(record.get("likes", 0)),
                comments=int(record.get("comments", 0)),
                replies=int(record.get("replies", 0)),
                like_to_view_ratio=record.get("like_to_view_ratio"),
                comment_to_view_ratio=record.get("comment_to_view_ratio"),
                popularity_score=float(
                    record.get("popularity_score", 0)
                ),
                overall_score=float(
                    record.get("overall_score", 0)
                ),
                collected_at=record.get("collected_at")
            )

            db.add(workflow)
            added += 1

        db.commit()

        return {
            "message": "Bulk import completed",
            "added": added,
            "skipped": skipped
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

@app.get("/workflows/{workflow_id}")
def get_workflow(
    workflow_id: int
):
    db = SessionLocal()

    workflow = (
        db.query(Workflow)
        .filter(
            Workflow.id == workflow_id
        )
        .first()
    )

    db.close()

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return workflow_to_dict(workflow)
    