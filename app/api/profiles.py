from flask import Blueprint, request, jsonify
from datetime import datetime
from uuid import uuid4

from app.extensions import db
from app.models.profile import BusinessProfile
from app.services.pipeline import PipelineService

profiles_bp = Blueprint("profiles", __name__)
pipeline_service = PipelineService()


@profiles_bp.route("", methods=["POST"])
def create_profile():
    data = request.get_json()

    profile = BusinessProfile(
        uuid=str(uuid4()),
        name=data["name"],
        domain=data["domain"],
        industry=data.get("industry"),
        description=data.get("description"),
        competitors=data.get("competitors", []),
        created_at=datetime.utcnow()
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "profile_uuid": profile.uuid,
        "status": "created"
    }), 201


@profiles_bp.route("/<uuid>", methods=["GET"])
def get_profile(uuid):
    profile = BusinessProfile.query.get_or_404(uuid)

    queries = profile.queries
    avg_score = (
        sum(q.opportunity_score for q in queries if q.opportunity_score) / len(queries)
        if queries else 0
    )

    return jsonify({
        "uuid": profile.uuid,
        "name": profile.name,
        "total_queries": len(queries),
        "avg_opportunity_score": round(avg_score, 3)
    })


@profiles_bp.route("/<uuid>/run", methods=["POST"])
def run_pipeline(uuid):
    profile = BusinessProfile.query.get_or_404(uuid)

    result = pipeline_service.run(profile)

    return jsonify(result)