# file: faiss_index.py
import os
import numpy as np
import faiss
from app.file_processing import FAISS_DIR

class FaissIndexer:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)

    def add_embeddings(self, embeddings: np.ndarray):
        self.index.add(embeddings)

    def save_index(self, doc_name: str):
        index_path = os.path.join(FAISS_DIR, f'{doc_name}_faiss.index')
        faiss.write_index(self.index, index_path)
        return index_path

    @staticmethod
    def load_index(doc_name: str):
        index_path = os.path.join(FAISS_DIR, f'{doc_name}_faiss.index')
        return faiss.read_index(index_path)
