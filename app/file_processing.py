"""
Common utilities and constants for the pipeline.
"""
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
CHUNKS_DIR = os.path.join(DATA_DIR, 'chunks')
EMBEDDINGS_DIR = os.path.join(DATA_DIR, 'embeddings')
FAISS_DIR = os.path.join(DATA_DIR, 'faiss')

os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
os.makedirs(FAISS_DIR, exist_ok=True)

