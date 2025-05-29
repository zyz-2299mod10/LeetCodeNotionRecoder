import requests
from urllib.parse import urlparse

def extract_slug(url):
    path = urlparse(url).path
    parts = path.strip("/").split("/")

    return parts[-1] if parts[-1] != "description" else parts[-2] 

def get_leetcode_info_via_api(slug):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{slug}/",
        "User-Agent": "Mozilla/5.0",
    }

    query = {
        "query": """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionFrontendId
                title
                difficulty
                topicTags {
                    name
                }
            }
        }
        """,
        "variables": {
            "titleSlug": slug
        }
    }

    res = requests.post(url, json=query, headers=headers)
    if res.status_code != 200:
        print("API Error:", res.text)
        return None
    
    q = res.json()["data"]["question"]
    return {
        "id": q["questionFrontendId"],
        "title": q["title"],
        "difficulty": q["difficulty"],
        "topics": [t["name"] for t in q["topicTags"]],
    }

if __name__ == "__main__":
    leetcode_url = "https://leetcode.com/problems/minimum-path-sum/"
    slug = extract_slug(leetcode_url)
    info = get_leetcode_info_via_api(slug)

    print("Problem ID: ", info["id"])
    print("Title:", info["title"])
    print("Difficulty:", info["difficulty"])
    print("Topic:", ", ".join(info["topics"]))
