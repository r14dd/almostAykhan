
03.02.2026

# almostAykhan

This project is not going to be an overkill but rather a small RAG concentrated AI assistant built for the case study. The goal is to make it possible for users to retrieve info about ABB. This is like ABB's existing Aykhan, but not quite so; which is precisely why I called it almostAykhan ;)!

**PS. Focuses heavily on backend and not the UI.**


## Arch: 

- A scraping service that extracts data from the webpage
- A RAG backend
- A Vector DB for semantic search (top-k chunks)
- A minimal front end for questions and visualizations
- A small db for logging

## Tech Stack

- Python(FastAPI)
- OpenAI API
- FAISS
- SQLite
- Alpine.js
- Chart.js
- Docker & Docker Compose

## Flow:

Scraping -> Chunking -> Embedding -> Q&A -> Logging -> Statistics