import json
import logging
import google.generativeai as genai
import os


class BaseAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

    def call_llm(self, system_prompt: str, user_prompt: str):
        try:
            full_prompt = f"""
{system_prompt}

USER INPUT:
{user_prompt}

IMPORTANT:
Return ONLY valid JSON. No explanation.
"""

            response = self.model.generate_content(full_prompt)

            return response.text

        except Exception as e:
            logging.error(f"Gemini call failed: {e}")
            return None

    def safe_json_parse(self, text: str):
        if not text:
            return None

        try:
            return json.loads(text)
        except:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                return json.loads(text[start:end])
            except:
                return None