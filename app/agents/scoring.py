import random
from app.utils.scoring import calculate_opportunity


class VisibilityScoringAgent:

    def run(self, query_text: str, domain: str):
        try:
            volume = random.randint(100, 5000)
            difficulty = random.randint(10, 90)

            visible = random.choice([True, False])
            position = random.randint(1, 10) if visible else None

            score = calculate_opportunity(
                volume=volume,
                difficulty=difficulty,
                visible=visible
            )

            return {
                "estimated_search_volume": volume,
                "competitive_difficulty": difficulty,
                "domain_visible": visible,
                "visibility_position": position,
                "opportunity_score": score,
                "status": "visible" if visible else "not_visible"
            }

        except Exception:
            return None