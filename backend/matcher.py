from backend.github_api import get_user_repos, search_good_first_issues


def run_matching_pipeline(username):

    # Fetch user repos
    repos = get_user_repos(username)
    print("REPOS:", repos[:3])

    if not repos:
        print("No repos found for user.")
        return []

    # Extract top languages
    languages = [repo['language'] for repo in repos if repo.get('language')]
    top_languages = list(set(languages))

    # Fallback if empty
    if not top_languages:
        top_languages = ["Python"]

    print("LANGUAGES:", top_languages)

    profile = {'top_languages': top_languages}

    # Search issues
    all_issues = []
    for lang in top_languages:
        issues = search_good_first_issues(lang)

        for issue in issues:
            repo = next((r for r in repos if r['name'] == issue.get('repo_name')), None)

            issue['repo_stars'] = repo['stars'] if repo else 0
            issue['labels'] = ['good first issue']

            # 🔥 IMPORTANT: add repo object for health check
            issue['repo'] = {
                "name": issue.get("repo_name"),
                "stars": issue.get("repo_stars", 0),
                "recent_commit": True,   # temporary assumption
                "has_license": True      # temporary assumption
            }

        all_issues.extend(issues)

    print("ISSUES FOUND:", len(all_issues))

    # Match issues
    matches = match_issues(profile, all_issues)
    return matches


def match_issues(profile, issues):

    scored_issues = []

    for issue in issues:
        score = score_issue(issue, profile)

        issue_copy = issue.copy()
        issue_copy['score'] = score

        scored_issues.append(issue_copy)

    scored_issues.sort(key=lambda x: x['score'], reverse=True)

    return scored_issues[:10]


def score_issue(issue, profile):

    score = 0

    if issue.get('language') in profile.get('top_languages', []):
        score += 3

    if 'good first issue' in issue.get('labels', []):
        score += 2

    stars = issue.get('repo_stars', 0)

    if stars >= 100:
        score += 2
    elif stars >= 50:
        score += 1

    return score