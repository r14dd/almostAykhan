import httpx
from fastapi import APIRouter, HTTPException

from backer.config import QA_SERVICE_URL
from backer.core.cache import cache_get, cache_set
from backer.log import log_qa
from backer.schemas import AskRequest


router = APIRouter()


@router.post("/ask")
def ask(_req: AskRequest):
    question = _req.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Sual tələb olunur.")

    cached = cache_get(question)
    if cached:
        log_qa(question, cached.get("answer", ""), cached.get("sources", []))
        return cached

    try:
        with httpx.Client(timeout=45.0) as client:
            res = client.post(
                QA_SERVICE_URL,
                json={"question": question},
            )
        res.raise_for_status()
        payload = res.json()
    except Exception:
        raise HTTPException(status_code=502, detail="QA service unavailable")

    answer = payload.get("answer", "Bunu bilmirəm.")
    sources = payload.get("sources", [])

    log_qa(question, answer, sources)

    payload = {"answer": answer, "sources": sources}
    cache_set(question, payload)
    return payload
