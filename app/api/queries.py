from flask import Blueprint, request, jsonify
from app.models.query import DiscoveredQuery
from app.extensions import db
from app.agents.scoring import VisibilityScoringAgent

queries_bp = Blueprint("queries", __name__)


@queries_bp.route("/profiles/<profile_uuid>/queries", methods=["GET"])
def get_queries(profile_uuid):

    min_score = float(request.args.get("min_score", 0))
    status = request.args.get("status")

    query = DiscoveredQuery.query.filter_by(profile_uuid=profile_uuid)

    if status:
        query = query.filter_by(status=status)

    query = query.filter(DiscoveredQuery.opportunity_score >= min_score)

    results = query.order_by(DiscoveredQuery.opportunity_score.desc()).all()

    return jsonify([
        {
            "query_text": q.query_text,
            "score": q.opportunity_score,
            "status": q.status
        } for q in results
    ])


@queries_bp.route("/queries/<query_uuid>/recheck", methods=["POST"])
def recheck(query_uuid):

    q = DiscoveredQuery.query.get_or_404(query_uuid)

    agent = VisibilityScoringAgent()
    data = agent.run(q.query_text, q.profile.domain)

    q.estimated_search_volume = data["estimated_search_volume"]
    q.competitive_difficulty = data["competitive_difficulty"]
    q.opportunity_score = data["opportunity_score"]
    q.domain_visible = data["domain_visible"]
    q.visibility_position = data["visibility_position"]
    q.status = data["status"]

    db.session.commit()

    return jsonify({"updated": True})