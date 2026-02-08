from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

from backer.config import *
from backer.rag import retrieve
from backer.db import initialize
from backer.log import log_qa, get_stats
from backer.ingest import ingest_chunks

from contextlib import asynccontextmanager


# https://github.com/fastapi/fastapi/discussions/13484#discussioncomment-12480851
# on a short notice here, declaring actions on startup is now deprecated?...

# @app.on_event("startup")
# def startup():
#     initialize()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize()
    yield

# From FastAPI docs: A lifespan context function, which can be used to perform startup and shutdown tasks.
# This is a newer style that replaces the on_startup and on_shutdown handlers. Use one or the other, not both.

app = FastAPI(lifespan=lifespan)
client = OpenAI()

# Serve frontend files at /ui
app.mount("/ui", StaticFiles(directory="fronter", html=True), name="ui")

CACHE = {}
CACHE_ORDER = []
CACHE_MAX = 200


class AskRequest(BaseModel):
    question: str


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


@app.get("/health")
def health():
    """
    Input: ()
    Output: health endpoint response with a string
    """

    return {"sagligdi": True}


@app.post("/ask")
def ask(_req: AskRequest):

    question = _req.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Sual tələb olunur.")

    cached = cache_get(question)
    if cached:
        log_qa(question, cached.get("answer", ""), cached.get("sources", []))
        return cached

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

    log_qa(question, answer, sources)

    payload = {
        "answer": answer,
        "sources": sources,
    }
    cache_set(question, payload)
    return payload

@app.get("/stats")
def stats():
    return get_stats()

@app.post("/ingest")
def ingest(_payload: dict):
    """
    Input: JSON body
    Output: ingestion summary dict or error 400
    """
    chunks = _payload.get("chunks")
    if not chunks or not isinstance(chunks, list):
        raise HTTPException(status_code=400, detail="chunks list required")

    result = ingest_chunks(chunks)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail="No text to ingest")

    CACHE.clear()
    CACHE_ORDER.clear()

    return result


