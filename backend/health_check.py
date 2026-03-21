def check_repo_health(repo):
    score = 0

    if repo.get("stars", 0) > 10:
        score += 1

    if repo.get("recent_commit", False):
        score += 1

    if repo.get("has_license", False):
        score += 1

    return score