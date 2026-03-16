# file_preprocess.py

import os
from typing import List
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.file_processing import CHUNKS_DIR

MASTER_CHUNKS_DIR = CHUNKS_DIR

os.makedirs(MASTER_CHUNKS_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text: str, chunk_size: int = 100, chunk_overlap: int = 0) -> List[str]:
    """Splits text into chunks using LangChain's RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

def process_pdf_to_chunks(pdf_path: str, output_dir: str = MASTER_CHUNKS_DIR, chunk_size: int = 1024, chunk_overlap: int = 0) -> List[str]:
    """Extracts text from a PDF, splits into chunks, and saves each chunk as a text file in output_dir."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    doc_dir = os.path.join(output_dir, base_name)
    os.makedirs(doc_dir, exist_ok=True)
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(doc_dir, f"chunk_{i+1}.txt")
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk)
    return chunks
