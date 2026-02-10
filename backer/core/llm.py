from openai import OpenAI

from backer.config import CHAT_MODEL


client = OpenAI()


def build_context(_chunks: list, max_chars_per_chunk: int = 800) -> str:
    """
    Input: list of retrieved chunk dicts, hardcoded number of max chars in a single given chunk
    Output: combined context string
    """

    parts = []
    i = 0
    while i < len(_chunks):
        item = _chunks[i]

        title = item.get("title", "")
        url = item.get("url", "")
        content = item.get("content", "")

        if len(content) > max_chars_per_chunk:
            content = content[:max_chars_per_chunk].rstrip()

        header = "Source " + str(i + 1) + ":\n" + "Title: " + title + "\n" + "URL: " + url

        block = header + "\n" + content

        parts.append(block)

        i += 1

    return "\n\n".join(parts)


def extract_text(_response) -> str:
    """
    Input: OpenAI response object
    Output: model output text
    """

    if _response is None:
        return ""
    try:
        return _response.output[0].content[0].text
    except Exception:
        return ""


def answer_question(_question: str, _chunks: list) -> str:
    """
    Input: question, dictionary chunks
    Output: llm answer
    """

    context = build_context(_chunks)

    prompt = (
        "Yalnız kontekstdən istifadə et.\n"
        "Kontekst başqa dildədirsə, sualın dilinə tərcümə edib cavab ver.\n"
        "Əgər cavab kontekstdə yoxdursa, sual verilən dildə “Bunu bilmirəm.” de.\n"
        "Sual bir neçə hissədən ibarətdirsə, bildiyin hissələri cavabla; bilmədiyin hissə üçün ayrıca “Bunu bilmirəm” yaz.\n"
        "Cavab qısa və dəqiq olsun.\n\n"
        "Context:\n"
        + context
        + "\n\nQuestion:\n"
        + _question
    )

    resp = client.responses.create(
        model=CHAT_MODEL,
        input=prompt,
        temperature=0,
    )

    return extract_text(resp).strip()

