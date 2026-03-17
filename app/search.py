import os
import numpy as np
import pickle
from app.rag_search.faiss_index import FaissIndexer
from app.rag_search.embedding import Embedder
from app.file_processing import FAISS_DIR, EMBEDDINGS_DIR


def semantic_hybrid_search(query, top_k=3, k_nearest_neighbors=3, context_limit= 3):
    """
    Semantic search using FAISS and sentence-transformers.
    : param query: User query string.
    : param top_k: Number of top results to return.
    : param k_nearest_neighbors: Number of nearest neighbors to retrieve from FAISS for each index.
    : context_limit: Number of chunks to return per document to avoid overwhelming the user.
    Returns top_k most similar chunks for the query.
    """
    # Find all available FAISS indices
    indices = [f for f in os.listdir(FAISS_DIR) if f.endswith('_faiss.index')]
    if not indices:
        return []
    embedder = Embedder()
    query_embedding = embedder.model.encode([query])[0]
    results = []
    for index_file in indices:
        doc_name = index_file.replace('_faiss.index', '')
        index = FaissIndexer.load_index(doc_name)
        # Load chunk metadata
        meta_path = os.path.join(EMBEDDINGS_DIR, f'{doc_name}_chunks.pkl')
        with open(meta_path, 'rb') as f:
            chunks = pickle.load(f)
        _, I = index.search(np.array([query_embedding]), k_nearest_neighbors)
        for idx in I[0][:top_k]:
            if idx < len(chunks):
                results.append({"title": doc_name, "content": chunks[idx]})
    return results[:context_limit]
