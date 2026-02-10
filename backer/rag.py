import json
from pathlib import Path

import faiss
import numpy as np
from openai import OpenAI
# https://www.youtube.com/watch?v=VPZimBvm_5g 


from backer.config import *


def load_index(_path: str):
    """
    Input: faiss index file path
    Output: faiss index object
    """

    return faiss.read_index(_path)


def load_meta(_path: str) -> list:
    """
    Input: metadata JSON path
    Output: list of chunk dicts
    """
    
    raw = Path(_path).read_text(encoding="utf-8")
    return json.loads(raw)


def embed_query(_query: str) -> list:
    """
    Input: user question
    Output: embedding vector
    """

    client = OpenAI()
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[_query],
    )
    return resp.data[0].embedding


def search_index(_index, _vector: list, _top_k: int):
    """
    Input: faiss index, vector list, top_k
    Output: indices, distances
    """

    vec = np.array([_vector], dtype="float32")
    distances, indices = _index.search(vec, _top_k)

    idx_list = []
    dist_list = []

    i = 0
    while i < len(indices[0]):
        idx_list.append(int(indices[0][i]))
        dist_list.append(float(distances[0][i]))
        i = i + 1

    return idx_list, dist_list


def get_results(_meta: list, _indices: list, _distances: list) -> list:
    """
    Input: meta, indices, distances
    Output: l ist of chunk dicts with distance
    """

    results = []

    i = 0
    while i < len(_indices):
        idx = _indices[i]
        if idx >= 0 and idx < len(_meta):
            item = _meta[idx].copy()
            item["distance"] = _distances[i]
            results.append(item)
        i = i + 1

    return results


def retrieve(_query: str, _top_k: int = TOP_K) -> list:
    """
    Input: query, top_k
    Output: top matching chunks
    """
    
    index = load_index(FAISS_INDEX_PATH)
    meta = load_meta(META_PATH)

    vector = embed_query(_query)
    indices, distances = search_index(index, vector, _top_k)

    return get_results(meta, indices, distances)
