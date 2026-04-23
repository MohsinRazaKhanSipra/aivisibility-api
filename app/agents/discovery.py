from .base import BaseAgent


class QueryDiscoveryAgent(BaseAgent):

    def run(self, profile):
        system_prompt = """
You are an expert SEO strategist.

Generate 10-20 realistic, high-intent queries.

Return JSON:
{
  "queries": ["..."]
}
"""

        user_prompt = f"""
Business: {profile.name}
Industry: {profile.industry}
Competitors: {profile.competitors}
"""

        response = self.call_llm(system_prompt, user_prompt)
        print("\n🔥 RAW GEMINI RESPONSE:\n", response)
        parsed = self.safe_json_parse(response)

        return parsed.get("queries", []) if parsed else []