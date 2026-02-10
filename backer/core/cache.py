CACHE = {}
CACHE_ORDER = []
CACHE_MAX = 200


def cache_key(_question: str) -> str:
    """
    Input: question string
    Output: normalized cache key string
    """

    return _question.strip().lower()


def cache_get(_question: str):
    """
    Input: question string
    Output: cached payload dict or None
    """

    key = cache_key(_question)
    if key in CACHE:
        return CACHE[key]
    return None


def cache_set(_question: str, _payload: dict) -> None:
    """
    Input: question string, payload dict
    Output: ()
    """

    key = cache_key(_question)

    if key in CACHE:
        CACHE[key] = _payload
        return

    CACHE[key] = _payload
    CACHE_ORDER.append(key)

    if len(CACHE_ORDER) > CACHE_MAX:
        old_key = CACHE_ORDER.pop(0)
        if old_key in CACHE:
            del CACHE[old_key]


def clear_cache() -> None:
    """
    Input: ()
    Output: ()
    """

    CACHE.clear()
    CACHE_ORDER.clear()

