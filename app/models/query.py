import uuid
from datetime import datetime
from app.extensions import db


class DiscoveredQuery(db.Model):
    __tablename__ = "discovered_queries"

    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    profile_uuid = db.Column(
        db.String(36), db.ForeignKey("business_profiles.uuid"), nullable=False
    )

    run_uuid = db.Column(
        db.String(36), db.ForeignKey("pipeline_runs.uuid"), nullable=True
    )

    query_text = db.Column(db.Text, nullable=False)

    estimated_search_volume = db.Column(db.Integer)
    competitive_difficulty = db.Column(db.Integer)

    opportunity_score = db.Column(db.Float)

    domain_visible = db.Column(db.Boolean, default=False)
    visibility_position = db.Column(db.Integer, nullable=True)

    status = db.Column(db.String(50), default="unknown")

    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)