# file: embedding.py
import os
import time
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
from app.file_processing import EMBEDDINGS_DIR

MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'


class Embedder:
    _model_cache = None
    _device_cache = None

    def __init__(self, model_name: str = MODEL_NAME):
        import torch
        if Embedder._model_cache is not None:
            self.model = Embedder._model_cache
            self.device = Embedder._device_cache
            print(f"[Embedder] Reusing cached model on device '{self.device}' at {time.strftime('%X')}")
        else:
            if torch.backends.mps.is_available():
                self.device = "mps"
                print(f"[Embedder] Using Apple Silicon GPU (MPS) at {time.strftime('%X')}")
            else:
                self.device = "cpu"
                print(f"[Embedder] Using CPU at {time.strftime('%X')}")
            print(f"[Embedder] Initializing SentenceTransformer at {time.strftime('%X')}")
            self.model = SentenceTransformer(model_name, device=self.device)
            print(f"[Embedder] Model loaded at {time.strftime('%X')}")
            Embedder._model_cache = self.model
            Embedder._device_cache = self.device

    def embed_chunks(self, chunks: List[str]) -> np.ndarray:
        print(f"[Embedder] Embedding {len(chunks)} chunks at {time.strftime('%X')}")
        start = time.time()
        embeddings = self.model.encode(chunks, show_progress_bar=True, device=self.device)
        print(f"[Embedder] Embedding completed in {time.time() - start:.2f} seconds at {time.strftime('%X')}")
        return embeddings

    def save_embeddings(self, embeddings: np.ndarray, doc_name: str):
        print(f"[Embedder] Saving embeddings for {doc_name} at {time.strftime('%X')}")
        out_path = os.path.join(EMBEDDINGS_DIR, f'{doc_name}_embeddings.npy')
        np.save(out_path, embeddings)
        return out_path

    def save_metadata(self, chunks: List[str], doc_name: str):
        print(f"[Embedder] Saving metadata for {doc_name} at {time.strftime('%X')}")
        meta_path = os.path.join(EMBEDDINGS_DIR, f'{doc_name}_chunks.pkl')
        with open(meta_path, 'wb') as f:
            pickle.dump(chunks, f)
        return meta_path
