# azure-rag-playground
This repository explores an experimental Retrieval‑Augmented Generation (RAG) pipeline using Sentence Transformers as the embedding encoder. It processes research papers and stores embeddings in a local vector database to study retrieval quality and downstream answer generation. The project is intended for learning and rapid prototyping purposes.


## Local Setup (with uv)

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install [uv](https://github.com/astral-sh/uv) if needed:
   ```bash
   pip install uv
   ```
3. Sync dependencies:
   ```bash
   uv sync
   ```