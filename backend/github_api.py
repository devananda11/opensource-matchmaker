import requests

BASE_URL = "https://api.github.com"


def get_user_repos(username):
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

    return repos

def search_good_first_issues(language):
    url = f"https://api.github.com/search/issues?q=label:\"good first issue\"+language:{language}+state:open+archived:false"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "FirstIssue-App"
    }

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

    return issues
