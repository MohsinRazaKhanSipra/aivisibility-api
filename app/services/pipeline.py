from datetime import datetime
from app.extensions import db
from app.models.query import DiscoveredQuery
from app.models.recommendation import ContentRecommendation
from app.models.pipeline_run import PipelineRun

from app.agents.discovery import QueryDiscoveryAgent
from app.agents.scoring import VisibilityScoringAgent
from app.agents.recommendation import ContentRecommendationAgent




class PipelineService:

    def __init__(self):
        self.discovery_agent = QueryDiscoveryAgent()
        self.scoring_agent = VisibilityScoringAgent()
        self.recommendation_agent = ContentRecommendationAgent()

    def run(self, profile):

        run = PipelineRun(profile_uuid=profile.uuid)
        db.session.add(run)
        db.session.commit()

        try:
            # ---- Agent 1 ----
            queries = self.discovery_agent.run(profile)
            run.queries_discovered = len(queries)

            stored_queries = []

            # ---- Agent 2 ----
            for q in queries:
                try:
                    score_data = self.scoring_agent.run(q, profile.domain)
                    if not score_data:
                        continue

                    dq = DiscoveredQuery(
                        profile_uuid=profile.uuid,
                        run_uuid=run.uuid,
                        query_text=q,
                        **score_data
                    )

                    db.session.add(dq)
                    stored_queries.append(dq)

                except Exception:
                    continue

            run.queries_scored = len(stored_queries)

            db.session.commit()

            # ---- Agent 3 ----
            not_visible_queries = [
                q.query_text for q in stored_queries if not q.domain_visible
            ][:5]

            recommendations = self.recommendation_agent.run(not_visible_queries)

            stored_recs = []

            for rec, query in zip(recommendations, stored_queries):
                r = ContentRecommendation(
                    profile_uuid=profile.uuid,
                    query_uuid=query.uuid,
                    content_type=rec.get("content_type"),
                    title=rec.get("title"),
                    rationale=rec.get("rationale"),
                    target_keywords=rec.get("target_keywords", []),
                    priority=rec.get("priority")
                )
                db.session.add(r)
                stored_recs.append(r)

            run.status = "completed"
            run.completed_at = datetime.utcnow()

            db.session.commit()

            # Top queries
            top_queries = sorted(
                stored_queries,
                key=lambda x: x.opportunity_score,
                reverse=True
            )[:3]

            return {
                "run_uuid": run.uuid,
                "status": run.status,
                "queries_discovered": run.queries_discovered,
                "queries_scored": run.queries_scored,
                "top_queries": [
                    {
                        "query": q.query_text,
                        "score": q.opportunity_score
                    } for q in top_queries
                ],
                "recommendations": [
                    {
                        "title": r.title,
                        "priority": r.priority
                    } for r in stored_recs
                ]
            }

        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            db.session.commit()

            return {"status": "failed", "error": str(e)}