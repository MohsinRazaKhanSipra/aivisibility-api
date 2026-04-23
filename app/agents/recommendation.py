from .base import BaseAgent


class ContentRecommendationAgent(BaseAgent):

    def run(self, queries):
        if not queries:
            return []

        system_prompt = """
You are a senior SEO content strategist.

Return JSON:
{
  "recommendations": [
    {
      "content_type": "",
      "title": "",
      "rationale": "",
      "target_keywords": [],
      "priority": "high|medium|low"
    }
  ]
}
"""

        user_prompt = f"Queries:\n{queries}"

        response = self.call_llm(system_prompt, user_prompt)
        parsed = self.safe_json_parse(response)

        return parsed.get("recommendations", []) if parsed else []