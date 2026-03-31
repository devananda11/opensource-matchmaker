from .github_api import get_user_repos, search_good_first_issues
from .profile_analyzer import analyze_profile

def run_matching_pipeline(username,language=None):

    # Fetch user repos
    repos = get_user_repos(username)
    print("REPOS:", repos[:3])

    if not repos:
        print("No repos found for user.")
        return []

    # Extract top languages
    profile = analyze_profile(repos)
    top_languages = profile.get('top_languages', ["Python"])


    # Search issues
    all_issues = []
    # Check if root README and CONTRIBUTING guide exist (for now, just check workspace root)
    import os
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    root_readme = os.path.exists(os.path.join(root_dir, 'README.md'))
    root_guide = (
        os.path.exists(os.path.join(root_dir, 'CONTRIBUTING.md')) or
        os.path.exists(os.path.join(root_dir, 'CONTRIBUTING.rst')) or
        os.path.exists(os.path.join(root_dir, 'CONTRIBUTING.txt'))
    )

    if language:
        top_languages = [language]

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
                "has_license": True,     # temporary assumption
                "has_readme": root_readme,  # crude check for now
                "has_guide": root_guide   # crude check for now
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

    # Language match
    language = issue.get('language') or ''
    if language in (profile.get('top_languages') or []):
        score += 3

    # Good first issue label
    labels = issue.get('labels') or []
    if 'good first issue' in labels:
        score += 2

    # Popularity (stars)
    stars = issue.get('repo_stars')
    if stars is None:
        stars = 0
    if stars >= 100:
        score += 2
    elif stars >= 50:
        score += 1

    # Issue description quality (length)
    desc = issue.get('issue_body')
    if desc is None:
        desc = ''
    if len(desc) > 300:
        score += 2
    elif len(desc) > 100:
        score += 1

    # Issue has code snippet in description
    if '```' in desc:
        score += 1

    # Recent activity (updated_at)
    from datetime import datetime, timedelta
    updated_at = issue.get('updated_at')
    if updated_at:
        try:
            updated = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ')
            if updated > datetime.utcnow() - timedelta(days=14):
                score += 2
            elif updated > datetime.utcnow() - timedelta(days=60):
                score += 1
        except Exception:
            pass

    # Comments
    comments = issue.get('comments')
    if comments is None:
        comments = 0
    if comments == 0:
        score += 1
    elif 1 <= comments <= 3:
        score += 2
    elif 4 <= comments <= 10:
        score += 1

    # Unassigned issues preferred
    assignees = issue.get('assignees')
    if assignees is None:
        assignees = []
    if not assignees:
        score += 2
    else:
        score -= 1

    # Helpful labels
    helpful_labels = {'help wanted', 'documentation', 'beginner friendly'}
    if any(label in helpful_labels for label in labels):
        score += 1

    # Repository health (has license, recent commit, has README/contributing guide)
    repo = issue.get('repo')
    if repo is None:
        repo = {}
    if repo.get('has_license'):
        score += 1
    if repo.get('recent_commit'):
        score += 1

    # Score for README presence
    if repo.get('has_readme'):
        score += 1

    # Score for contributing guide presence
    if repo.get('has_guide'):
        score += 1

    return score