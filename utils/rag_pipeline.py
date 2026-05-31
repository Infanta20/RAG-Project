from pathlib import Path
from typing import List, Tuple

import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


VECTORSTORE_DIR = "vectorstore"
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"


@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def build_vectorstore(documents):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(VECTORSTORE_DIR)
    return vectorstore


def load_vectorstore():
    vector_path = Path(VECTORSTORE_DIR)
    if not vector_path.exists():
        return None

    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore


def search_resumes(query: str, k: int = 15) -> List[Tuple]:
    vectorstore = load_vectorstore()
    if vectorstore is None:
        return []

    results = vectorstore.similarity_search_with_score(query, k=k)
    return results