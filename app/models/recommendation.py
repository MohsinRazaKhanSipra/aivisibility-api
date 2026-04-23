import uuid
from datetime import datetime
from app.extensions import db


class ContentRecommendation(db.Model):
    __tablename__ = "content_recommendations"

    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    profile_uuid = db.Column(
        db.String(36), db.ForeignKey("business_profiles.uuid"), nullable=False
    )

    query_uuid = db.Column(
        db.String(36), db.ForeignKey("discovered_queries.uuid"), nullable=False
    )

    content_type = db.Column(db.String(50))
    title = db.Column(db.String(255))

    rationale = db.Column(db.Text)

    target_keywords = db.Column(db.JSON, default=list)

    priority = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)