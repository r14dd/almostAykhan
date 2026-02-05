# #####################

def split_into_chunks(
    _text: str,
    _max_chars: int = 500,
    _overlap: int = 100,
) -> list[str]:
    """
    Input: single text string, max num of chars per chunk, num of chars to overlap
    Output: list of text chunks which are strs, at most max chars long
    """

    chunks: list[str] = []
    start = 0
    text_len = len(_text)

    while start < text_len:
        end = start + _max_chars
        chunk = _text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - _overlap
        if start < 0:
            start = 0

    return chunks


def make_chunk_record(
    _content: str,
    _page: dict,
    _index: int,
) -> dict:
    """
    Input: a given chunk, original page dict, index of the chunk on the page
    Output: a dict containing: chunk text, source url, source page title, index of the chunk
    """

    return {
        "content": _content,
        "url": _page.get("url"),
        "title": _page.get("title"),
        "chunk_index": _index,
    }


def chunk_page(
    _page: dict,
    _max_chars: int = 500,
    _overlap: int = 100,
) -> list[dict]:
    """
    Convert a parsed page into chunk records.
    """
    text = _page.get("clean_text", "")
    chunks = split_into_chunks(text, _max_chars, _overlap)

    results: list[dict] = []

    for idx, chunk in enumerate(chunks):
        results.append(make_chunk_record(chunk, _page, idx))

    return results
