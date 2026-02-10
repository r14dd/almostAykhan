from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health():
    """
    Input: ()
    Output: health endpoint response with a string
    """

    return {"sagligdi": True}

