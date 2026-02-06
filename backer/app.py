from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

from backer.config import *
from backer.rag import retrieve


app = FastAPI()
client = OpenAI()


class AskRequest(BaseModel):
    question: str


def build_context(chunks: list, max_chars_per_chunk: int = 800) -> str:
    """
    Input: list of retrieved chunk dicts, hardcoded number of max chars in a single given chunk
    Output: combined context string
    """

    parts = []
    i = 0
    while i < len(chunks):
        item = chunks[i]

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


def extract_text(response) -> str:
    """
    Input: OpenAI response object
    Output: model output text
    """

    if response is None:
        return ""
    try:
        return response.output[0].content[0].text
    except Exception:
        return ""


def answer_question(question: str, chunks: list) -> str:
    """
    Input: question, dictionary chunks
    Output: llm answer
    """

    context = build_context(chunks)

    prompt = (
        "Yalnız kontekstdən istifadə et.\n"
        "Sual ingiliscədirsə cavabı yalnız ingiliscə, rusdursa yalnız rusca yaz.\n"
        "Əgər sual növlər/kateqoriyalar haqqındadırsa, kontekstdə olan maddələri siyahıla.\n"
        "Əgər cavab kontekstdə yoxdursa, sual verilən dildə “Bunu bilmirəm.” de.\n"
        "Cavab qısa və dəqiq olsun.\n\n"
        "Context:\n"
        + context
        + "\n\nQuestion:\n"
        + question
    )

    resp = client.responses.create(
        model=CHAT_MODEL,
        input=prompt,
        temperature=0,
    )

    return extract_text(resp).strip()


@app.get("/health")
def health():
    """
    Input: ()
    Output: health endpoint response with a string
    """

    return {"sagligdi": True}


@app.post("/ask")
def ask(req: AskRequest):

    question = req.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Sual tələb olunur.")

    chunks = retrieve(question, TOP_K)
    answer = answer_question(question, chunks)

    sources = []
    for item in chunks:
        source = {
            "url": item.get("url"),
            "title": item.get("title"),
            "content": item.get("content"),
            "distance": item.get("distance"),
        }

        sources.append(source)

    return {
        "answer": answer,
        "sources": sources,
    }