from backer.config import RETRIEVAL_MAX_DISTANCE


INJECTION_PHRASES = [
    # Azerbaijani
    "konteksti ignore et",
    "konteksti nəzərə alma",
    "təlimatları ignore et",
    "təlimatları nəzərə alma",
    "qaydaları ignore et",
    "sistem mesajını ignore et",
    # English
    "ignore context",
    "ignore instructions",
    "ignore previous instructions",
    "ignore the rules",
    "system prompt",
    "developer message",
    "act as",
    "jailbreak",
    "bypass",
    # Russian
    "игнорируй контекст",
    "игнорируй инструкции",
    "игнорируй предыдущие инструкции",
    "игнорируй правила",
    "системный промпт",
    "сообщение разработчика",
    "обойди ограничения",
]


def retrieval_is_confident(_chunks: list) -> bool:
    """
    Input: retrieved chunk list
    Output: True if best retrieval distance is good enough, else False
    """

    if not _chunks:
        return False

    first = _chunks[0]
    best_distance = first.get("distance")
    if best_distance is None:
        return False

    return float(best_distance) <= RETRIEVAL_MAX_DISTANCE


def is_injection_attempt(_question: str) -> bool:
    """
    Input: question string
    Output: True if question contains prompt-injection phrases, else False
    """

    q = _question.strip().lower()
    i = 0
    while i < len(INJECTION_PHRASES):
        if INJECTION_PHRASES[i] in q:
            return True
        i += 1
    return False

