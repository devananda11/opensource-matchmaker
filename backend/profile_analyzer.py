def count_languages(repos):
    language_count = {}

    for repo in repos:
        lang = repo.get("language")
        if lang:
            language_count[lang] = language_count.get(lang, 0) + 1

    return language_count


def detect_top_languages(language_count, top_n=2):
    sorted_langs = sorted(language_count.items(), key=lambda x: x[1], reverse=True)
    return [lang[0] for lang in sorted_langs[:top_n]]


def analyze_profile(repos):
    language_count = count_languages(repos)
    top_languages = detect_top_languages(language_count)
    return {
        "top_languages": top_languages,
        "language_count": language_count
    }