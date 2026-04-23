import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/v1"


def create_profile():
    url = f"{BASE_URL}/profiles"

    payload = {
        "name": "Surfer SEO",
        "domain": "surferseo.com",
        "industry": "SEO Software",
        "description": "AI-powered SEO optimization tool",
        "competitors": ["clearscope.io", "frase.io"]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 201:
        print("❌ Failed to create profile:", response.text)
        return None

    data = response.json()
    print("✅ Profile created:", data)

    return data["profile_uuid"]


def run_pipeline(profile_uuid):
    url = f"{BASE_URL}/profiles/{profile_uuid}/run"

    print("⏳ Running pipeline...")
    response = requests.post(url)

    if response.status_code != 200:
        print("❌ Pipeline failed:", response.text)
        return None

    data = response.json()
    print("✅ Pipeline result:\n", data)

    return data


def get_queries(profile_uuid):
    url = f"{BASE_URL}/profiles/{profile_uuid}/queries?min_score=0.3"

    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Failed to fetch queries:", response.text)
        return

    data = response.json()

    print("\n📊 Queries:")
    for q in data:
        print(f"- {q['query_text']} | Score: {q['score']} | Status: {q['status']}")


def main():
    profile_uuid = create_profile()
    if not profile_uuid:
        return

    time.sleep(1)

    run_pipeline(profile_uuid)

    time.sleep(1)

    get_queries(profile_uuid)


if __name__ == "__main__":
    main()