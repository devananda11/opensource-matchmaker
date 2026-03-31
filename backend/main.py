from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Query
from matcher import run_matching_pipeline
from health_check import check_repo_health
from ai_description import explain_issue
from github_api import search_good_first_issues

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (perfect for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FirstIssue API is running"}


@app.get("/recommend/{username}")
def recommend(username: str, language: str = Query(None), bypass_health: bool = Query(False)):

    try:
        language = language.strip() if isinstance(language, str) else language
        if language == "":
            language = None
        
        matches = run_matching_pipeline(username, language)

        print("MATCHES:", matches)

        if bypass_health:
            filtered_matches = matches
        else:
            filtered_matches = []
            for match in matches:
                repo = match.get("repo", {})

                if check_repo_health(repo) >= 2:
                    filtered_matches.append(match)

        return {
            "username": username,
            "count": len(filtered_matches),
            "recommendations": filtered_matches
        }

    except Exception as e:
        return {
            "username": username,
            "error": str(e),
            "recommendations": []
        }

@app.get("/health-test")
def test_health():

    repo = {
        "name": "test-repo",
        "stars": 50,
        "recent_commit": True,
        "has_license": True
    }

    score = check_repo_health(repo)

    return {
        "repo": repo["name"],
        "health_score": score
    }
@app.get("/rate-limit")
def rate_limit():
    import requests

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "FirstIssue-App"
    }

    response = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=10)
    return response.json()


@app.post("/explain")
def explain(data: dict):
    title = data.get("title")
    body = data.get("body", "")

    if not title:
        return {"error": "Missing title"}

    explanation = explain_issue(title, body)

    return {"explanation": explanation}


