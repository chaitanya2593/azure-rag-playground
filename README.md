# RAG based Playground app for analyzing research papers
This repository explores an experimental Retrieval-Augmented Generation (RAG) pipeline using Azure AI services and local tools. The goal is to create a simple, local RAG setup that can ingest PDF research papers, vectorize them, and answer user queries based on the content.

## Prerequisites
Before running the app, make sure you have the following installed on your machine:

1. Python 3.8 or higher
2. Redis (for caching)
3. Storage space for uploaded PDFs and vector indexes. Approximately 1GB should be sufficient for testing with a few papers.
4. Azure OpenAI access (optional, for using GPT-5) or have the LLM of your choice set up locally.

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


## Run the Streamlit App
```bash
streamlit run streamlit.py
```
Please chat with the bot in the Streamlit UI and observe how it retrieves and generates answers based on the uploaded documents.

## Redis Setup (for Caching)

This app uses Redis to cache answers for repeated questions, speeding up response time.

To set up Redis locally, you can use Docker. Run the following command in your terminal:
```bash
redis-server
```

The app expects Redis to be running on `localhost:6379` by default. You can change this in your environment variables if needed.


***

## RAG Pipeline – Tools Used

| Step                | Purpose                 | Tool / Choice                            | Reason                             |
| ------------------- | ----------------------- | ---------------------------------------- | ---------------------------------- |
| Document ingestion  | Read PDF files          | pypdf                                    | Simple, sufficient for PDFs        |
| Chunking            | Split text into chunks  | LangChain TextSplitter                   | Predictable, fast, easy to debug   |
| Embeddings          | Convert text to vectors | sentence‑transformers (all‑MiniLM‑L6‑v2) | Local, free, lightweight           |
| Vector store        | Store & search vectors  | FAISS                                    | Fast, local, semantic search       |
| Retrieval           | Find relevant chunks    | FAISS similarity search                  | Embedding‑based semantic retrieval |
| Query understanding | Improve user query      | GPT‑5 (Azure OpenAI)                     | Better semantic matching           |
| Orchestration       | Connect RAG components  | LangChain                                | Flexible, minimal abstraction      |
| Caching             | Speed up repeated calls | Redis (local)                            | Simple local cache                 |
| Storage             | Persist files & data    | Local filesystem                         | No external dependency             |
| UI                  | User interaction        | Streamlit                                | Fast prototyping                   |
| Monitoring          | Tracing & observability | Not used                                 | Demo / research only               |


Please refer to the `app/rag_search/research.md` file for a detailed breakdown of the tool choices and rationale. If you want to understand the step-by-step flow of how the RAG search works, check out `app/rag_search/processing_flow.md` for a clear explanation.
***

## Sources &  Research
- When we need RAG: https://www.youtube.com/watch?v=UabBYexBD4k

## FAQ
Find quick answers to common questions in the [FAQ](FAQ.md).
