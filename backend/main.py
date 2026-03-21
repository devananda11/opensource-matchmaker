from fastapi import FastAPI
from backend.matcher import run_matching_pipeline
from backend.health_check import check_repo_health

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FirstIssue API is running"}


@app.get("/recommend/{username}")
def recommend(username: str):

    try:
        matches = run_matching_pipeline(username)

        print("MATCHES:", matches)

        # Apply health check
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