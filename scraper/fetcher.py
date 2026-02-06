import httpx

from .config import *
from typing import Optional

async def fetch(_url: str) -> Optional[str]:
    """
    Input: URL
    Output: HTML str or None
    """
    tries = 0

    while tries < MAX_RETRIES:
        try:
            async with httpx.AsyncClient(
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
                follow_redirects=True,
            ) as client:
                res = await client.get(_url)

            # Failure:
            if res.status_code != 200:
                return None
            
            c_type = res.headers.get("content-type", "").lower()
            if ALLOWED_CONTENT_TYPES in c_type:
                return res.text

            return None
        
        except Exception:
            tries = tries + 1


    return None
