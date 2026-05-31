import os
import re
from pathlib import Path
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def save_uploaded_files(uploaded_files) -> List[str]:
    saved_paths = []

    for uploaded_file in uploaded_files:
        file_path = DATA_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(str(file_path))

    return saved_paths


def extract_candidate_name(text: str, file_name: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        if 2 <= len(first_line.split()) <= 5 and len(first_line) < 50:
            return first_line.title()

    fallback_name = Path(file_name).stem.replace("_", " ").replace("-", " ").title()
    return fallback_name


def load_pdf_documents(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs


def create_chunks_from_pdf(file_path: str):
    docs = load_pdf_documents(file_path)

    if not docs:
        return []

    full_text = "\n".join([doc.page_content for doc in docs])
    full_text = clean_text(full_text)
    candidate_name = extract_candidate_name(full_text, Path(file_path).name)
    candidate_id = Path(file_path).stem

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    split_docs = splitter.split_documents(docs)

    enriched_docs = []
    for doc in split_docs:
        doc.page_content = clean_text(doc.page_content)

        doc.metadata["candidate_id"] = candidate_id
        doc.metadata["candidate_name"] = candidate_name
        doc.metadata["file_name"] = Path(file_path).name
        doc.metadata["source"] = file_path
        doc.metadata["page"] = doc.metadata.get("page", 0)

        enriched_docs.append(doc)

    return enriched_docs


def process_all_pdfs(file_paths: List[str]):
    all_chunks = []

    for file_path in file_paths:
        chunks = create_chunks_from_pdf(file_path)
        all_chunks.extend(chunks)

    return all_chunks