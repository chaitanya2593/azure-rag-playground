# file: pipeline.py
"""
Pipeline to process PDF, chunk, embed, and index with FAISS.
"""

import os
from app.rag_search.file_preprocess import process_pdf_to_chunks
from app.rag_search.embedding import Embedder
from app.rag_search.faiss_index import FaissIndexer


def process_document(pdf_path: str):
    # Step 1: Chunk PDF
    chunks = process_pdf_to_chunks(pdf_path)
    doc_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Step 2: Embed Chunks
    embedder = Embedder()
    embeddings = embedder.embed_chunks(chunks)
    embedder.save_embeddings(embeddings, doc_name)
    embedder.save_metadata(chunks, doc_name)

    # Step 3: Index with FAISS
    dim = embeddings.shape[1]
    indexer = FaissIndexer(dim)
    indexer.add_embeddings(embeddings)
    indexer.save_index(doc_name)

    print(f"Document '{doc_name}' processed: chunks, embeddings, and FAISS index saved.")

