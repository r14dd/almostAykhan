from fastapi import FastAPI, HTTPException

from backer.config import TOP_K
from backer.core.guards import is_injection_attempt, retrieval_is_confident
from backer.core.llm import answer_question
from backer.rag import retrieve
from backer.schemas import AskRequest


app = FastAPI()


@app.get("/health")
def health():
    """
    Input: ()
    Output: health response dict
    """

    return {"sagligdi": True}


@app.post("/answer")
def answer(_req: AskRequest):
    """
    Input: AskRequest
    Output: dict with answer and sources
    """

    question = _req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Sual tələb olunur.")

    if is_injection_attempt(question):
        return {
            "answer": "Bunu bilmirəm.",
            "sources": [],
        }

    chunks = retrieve(question, TOP_K)
    confident = retrieval_is_confident(chunks)

    if not confident:
        return {
            "answer": "Bunu bilmirəm.",
            "sources": [],
        }

    answer_text = answer_question(question, chunks)

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
        "answer": answer_text,
        "sources": sources,
    }

