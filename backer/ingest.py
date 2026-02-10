import json
from pathlib import Path
import faiss
import numpy as np
from openai import OpenAI

from backer.config import *



def load_chunks(_path: str) -> list:
    """
    Input: path to JSON
    Output: list of chunk dicts
    """

    raw_text = Path(_path).read_text(encoding="utf-8")
    data = json.loads(raw_text)
    return data


def apply_limit(_data: list, _limit: int) -> list:
    """
    Input: list of chunk dicts, max number of items to keep
    Output: possibly truncated list of chunks
    """

    if _limit <= 0:
        return _data
    return _data[:_limit] 

def validate_chunks(_data: list) -> tuple:
    """
    Input: list
    Output: boolean and validated data or a string error
    """
    if not isinstance(_data, list):
        return False, "chunks must be a list"

    cleaned = []
    i = 0
    while i < len(_data):
        item = _data[i]
        if isinstance(item, dict):
            content = item.get("content")
            if isinstance(content, str) and content.strip():
                cleaned.append(item)
        i += 1

    if len(cleaned) == 0:
        return False, "no valid chunks with non-empty content"

    return True, cleaned


def build_texts_and_meta(_data: list) -> tuple:
    """
    Input: list of chunk dicts
    Output: list of non  empty chunk text strings, list of chunk dicts matching texts
    """

    texts = []
    meta = []

    for item in _data:
        content = item.get("content", "").strip()
        if not content:
            continue
        title = item.get("title", "").strip()
        url = item.get("url", "").strip()

        parts = []
        if title:
            parts.append("Title: " + title)
        if url:
            parts.append("URL: " + url)
        parts.append(content)

        full_text = "\n".join(parts)
        texts.append(full_text)
        meta.append(item)

    return texts, meta


def embed_texts(_texts: list) -> list:
    """
    Input: list of chunk text to embed
    Output: vector-list of embedding vectors
    """

    client = OpenAI()
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=_texts,
    )

    vectors = []
    for item in resp.data:
        vectors.append(item.embedding)

    return vectors


def build_faiss_index(_vectors: list):
    """
    Input: list of embedding vectors
    Output: faiss index with vectors added, dimension of each vector
    """

    dim = len(_vectors[0])
    index = faiss.IndexFlatL2(dim)

    matrix = np.array(_vectors, dtype="float32")
    index.add(matrix)

    return index, dim


def save_index(_index: str, _path: str) -> None:
    """
    Input: faiss index to save, output path for the index file
    Output: ()
    """

    Path(_path).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(_index, _path)


def save_metadata(_meta: list, _path: str) -> None:
    """
    Input: list of chunk dicts, output path for metadata JSON file
    Output: ()
    """

    Path(_path).parent.mkdir(parents=True, exist_ok=True)
    Path(_path).write_text(
        json.dumps(_meta, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def ingest_chunks(_data: list) -> dict:
    """
    Input: list of chunk dicts
    Output: dict with ingestion summary
    """

    ok, cleaned = validate_chunks(_data)
    
    if not ok:
        return {"ok": False, "error": cleaned}
    
    _data = cleaned

    _data = apply_limit(_data, EMBED_LIMIT)

    texts, meta = build_texts_and_meta(_data)
    if len(texts) == 0:
        return {"ok": False, "error": "No text"}

    vectors = embed_texts(texts)
    index, dim = build_faiss_index(vectors)

    save_index(index, FAISS_INDEX_PATH)
    save_metadata(meta, META_PATH)

    return {
        "ok": True,
        "chunks": len(_data),
        "embedded": len(texts),
        "dim": dim,
    }



def main():
    data = load_chunks(CHUNKS_PATH)
    result = ingest_chunks(data)

    if not result.get("ok"):
        print("no text")
        return

    print("chunks loaded:", result.get("chunks"))
    print("embedded:", result.get("embedded"))
    print("vector dim:", result.get("dim"))
    print("faiss index:", FAISS_INDEX_PATH)
    print("meta file:", META_PATH)



if __name__ == "__main__":
    main()
