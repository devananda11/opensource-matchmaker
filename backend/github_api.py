import requests
from datetime import datetime, timedelta

BASE_URL = "https://api.github.com"

# Simple in-memory per-process cache
_REPO_CACHE = {}
_ISSUE_CACHE = {}

CACHE_TTL = timedelta(minutes=3)


def _cache_get(cache, key):
    entry = cache.get(key)
    if not entry:
        return None
    value, expires_at = entry
    if datetime.utcnow() >= expires_at:
        cache.pop(key, None)
        return None
    return value


def _cache_set(cache, key, value):
    cache[key] = (value, datetime.utcnow() + CACHE_TTL)


def get_user_repos(username):
    cached = _cache_get(_REPO_CACHE, username)
    if cached is not None:
        return cached

    url = f"{BASE_URL}/users/{username}/repos"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "FirstIssue-App"
    }

    response = requests.get(url, headers=headers, timeout=10)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text[:200])

    if response.status_code != 200:
        print("Error fetching repos")
        return []

    data = response.json()

    repos = []

    for repo in data[:10]: # gives 10
        repo_info = {
            "name": repo["name"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "repo_url": repo["html_url"]
        }

        repos.append(repo_info)

    _cache_set(_REPO_CACHE, username, repos)
    return repos

def search_good_first_issues(language):
    url = f"https://api.github.com/search/issues?q=label:\"good first issue\"+language:{language}+state:open+archived:false"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "FirstIssue-App"
    }

    cache_key = language.lower().strip()
    cached = _cache_get(_ISSUE_CACHE, cache_key)
    if cached is not None:
        return cached

    response = requests.get(url, headers=headers, timeout=10)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text[:200])

    if response.status_code != 200:
        return []

    data = response.json()

    issues = []

    for issue in data["items"]:  
        issue_info = {
            "repo_name": issue["repository_url"].split("/")[-1],
            "repo_url": issue["repository_url"],  
            "issue_title": issue["title"],
            "issue_body": issue.get("body", ""),
            "issue_url": issue["html_url"],
            "language": language,
            "assignees": issue.get("assignees", []),
            "comments": issue.get("comments", 0),
            "updated_at": issue.get("updated_at", None),
            "created_at": issue.get("created_at", None),
            "labels": [label["name"] for label in issue.get("labels", [])],
            "is_locked": issue.get("locked", False),
            "state": issue.get("state", "open"),
        }

        issues.append(issue_info)

    _cache_set(_ISSUE_CACHE, cache_key, issues)

    return issues
