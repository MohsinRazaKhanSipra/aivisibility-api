import uuid
from datetime import datetime
from app.extensions import db


class BusinessProfile(db.Model):
    __tablename__ = "business_profiles"

    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), nullable=False, index=True)
    industry = db.Column(db.String(255))
    description = db.Column(db.Text)
    competitors = db.Column(db.JSON, default=list)

    status = db.Column(db.String(50), default="created")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    queries = db.relationship("DiscoveredQuery", backref="profile", lazy=True)
    recommendations = db.relationship("ContentRecommendation", backref="profile", lazy=True)
    pipeline_runs = db.relationship("PipelineRun", backref="profile", lazy=True)