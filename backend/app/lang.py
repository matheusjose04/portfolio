def resolve_lang(accept_language: str | None, lang_query: str | None) -> str:
    if lang_query in ("pt", "en"):
        return lang_query
    if accept_language and accept_language.lower().startswith("en"):
        return "en"
    return "pt"
