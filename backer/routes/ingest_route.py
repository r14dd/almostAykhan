from fastapi import APIRouter, HTTPException

from backer.core.cache import clear_cache
from backer.ingest import ingest_chunks


router = APIRouter()


@router.post("/ingest")
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

    clear_cache()
    return result

