from fastapi import APIRouter

from backer.log import get_stats


router = APIRouter()


@router.get("/stats")
def stats():
    return get_stats()

