import os


CHUNKS_PATH = "scraper/output/abb_chunks.json"
FAISS_INDEX_PATH = "backer/data/abb.index"
META_PATH = "backer/data/abb_meta.json"
DB_PATH = "backer/data/qa.sqlite"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

TOP_K = 10
EMBED_LIMIT = 0

RETRIEVAL_MAX_DISTANCE = 1.35

QA_SERVICE_URL = os.getenv("QA_SERVICE_URL", "http://127.0.0.1:8001/answer")
