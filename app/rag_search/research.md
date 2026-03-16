# Research Notes – Local RAG Design Decisions

This document consolidates the explored tooling options and explains what was selected and why. The focus is on a **local, free, learning‑oriented RAG setup**.

***

## 1) Document ingestion & parsing

**Options considered**

*   PDF parsing tools

**Selected**

*   **pypdf** ✅

**Why**

*   We are dealing with PDF research papers.
*   Simple and sufficient for text extraction.
*   No extra complexity needed.

***

## 2) Cleaning, splitting, enrichment

**Options considered**

*   LangChain TextSplitter
*   LlamaIndex NodeParser
*   Semantic‑chunking (LlamaIndex)

### ✅ Selected: LangChain TextSplitter

**Why LangChain TextSplitter is best in this case**  
(Local RAG, learning, fast iteration)

*   Documents are known (research papers).
*   Predictable and easy to debug.
*   Fixed‑size chunks work well with PDFs + embeddings.
*   Minimal abstraction.
*   Faster indexing and querying.
*   Easy to swap vector DBs or models later.

**Why the others are not ideal right now**

*   **LlamaIndex NodeParser**
    *   Adds structure not currently needed.
    *   Better suited for large, complex pipelines.
    *   More mental overhead.

*   **Semantic‑chunking**
    *   Higher retrieval quality but slower.
    *   Harder to tune and reason about.
    *   Overkill for a learning / prototype setup.

**Rule of thumb**

*   Prototype / learn → LangChain TextSplitter
*   Production + rich metadata → NodeParser
*   Max retrieval quality → Semantic chunking

***

## 3) Embeddings (Sentence Transformers)

**Options considered**

*   Local sentence‑transformers
*   LLM embeddings (e.g., OpenAI embeddings)

**Selected**

*   **sentence‑transformers: all‑MiniLM‑L6‑v2** ✅

**Why**

*   Fully local and free.
*   Fast and lightweight.
*   Good enough semantic quality for research papers.

***

## 4) Vector database (local‑first)

**Options considered**

*   FAISS
*   hnswlib

**Selected**

*   **FAISS** ✅

**Why**

*   Local‑only, no server needed.
*   Very fast semantic similarity search.
*   Simple integration.

***

## 5) Hybrid retrieval / ranking

**Options considered**

*   BM25 (Elasticsearch / OpenSearch / Whoosh)
*   ANN (FAISS / hnswlib)

### BM25 vs FAISS

**BM25**

*   Keyword search.
*   Excellent for exact matches.
*   No semantic understanding.

**FAISS** ✅

*   Semantic search.
*   Uses embeddings.
*   May miss exact keyword intent.

**Decision**

*   The goal is semantic search.
*   FAISS fits this requirement best.

***

## 6) Orchestration

**Options considered**

*   LangChain
*   LlamaIndex

### ✅ Selected: LangChain

**Why**

*   More flexible.
*   Lightweight abstractions.
*   Easy to mix FAISS and BM25 later.
*   Better for experimentation.
*   Easier to debug.

**Why not LlamaIndex**

*   More opinionated.
*   More abstraction / magic.
*   Better suited for document‑heavy production systems.

***

## 7) LLMs for query understanding

**Selected**

*   **GPT‑5 via Azure OpenAI**

**Why**

*   Used for query rewriting and understanding.
*   Improves semantic retrieval quality.

***

## 8) Caching & storage

**Options considered**

*   SQLite
*   Redis
*   Local filesystem
*   DuckDB / SQLite for metadata

**Selected**

*   **Local filesystem** ✅
*   **Redis (local)** ✅

**Why**

*   Simple setup.
*   Sufficient for demo and research purposes.

***

## 9) UI / API

**Selected**

*   **Streamlit**

***

## 10) Monitoring & observability

**Options considered**

*   Langfuse (open source)

**Decision**

*   Not used.
*   Reason: demo and research‑only application.

***

## Sources & Research
- https://docs.langchain.com/oss/python/integrations/splitters
