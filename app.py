import os
from pathlib import Path

import streamlit as st

from utils.pdf_handler import save_uploaded_files, process_all_pdfs
from utils.rag_pipeline import build_vectorstore, search_resumes, load_vectorstore
from utils.ranker import rank_candidates


st.set_page_config(page_title="Resume RAG Chatbot", page_icon="📄", layout="wide")

st.title("📄 Resume RAG Chatbot")
st.write("Upload multiple resumes in PDF format, build a FAISS index, and search top matching candidates by skills.")

if "indexed" not in st.session_state:
    st.session_state.indexed = False


with st.sidebar:
    st.header("Project Info")
    st.write("Tech Stack:")
    st.write("- Streamlit")
    st.write("- LangChain")
    st.write("- HuggingFace Embeddings")
    st.write("- FAISS")
    st.write("- PyPDFLoader")

    if Path("vectorstore").exists():
        st.success("Vectorstore found.")
    else:
        st.warning("No vectorstore built yet.")


st.subheader("1. Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Process and Build Index", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one PDF resume.")
        else:
            with st.spinner("Saving files and creating chunks..."):
                file_paths = save_uploaded_files(uploaded_files)
                documents = process_all_pdfs(file_paths)

            if not documents:
                st.error("No text could be extracted from the uploaded PDFs.")
            else:
                with st.spinner("Building FAISS vectorstore..."):
                    build_vectorstore(documents)

                st.session_state.indexed = True
                st.success(f"Index built successfully from {len(uploaded_files)} resumes.")

with col2:
    if st.button("Load Existing Index", use_container_width=True):
        vectorstore = load_vectorstore()
        if vectorstore is not None:
            st.session_state.indexed = True
            st.success("Existing vectorstore loaded.")
        else:
            st.error("No saved vectorstore found.")


st.subheader("2. Search Candidates")
query = st.text_input(
    "Enter required skills or job description",
    placeholder="Example: Python, React, Node.js, MongoDB, LangChain"
)

top_k = st.slider("How many chunk matches to retrieve?", min_value=5, max_value=30, value=15, step=5)
top_n = st.slider("How many top candidates to show?", min_value=1, max_value=10, value=5, step=1)

if st.button("Search Top Matching Resumes", use_container_width=True):
    if not st.session_state.indexed and load_vectorstore() is None:
        st.error("Please build or load the vector index first.")
    elif not query.strip():
        st.error("Please enter a skill query.")
    else:
        with st.spinner("Searching resumes..."):
            raw_results = search_resumes(query, k=top_k)
            ranked_results = rank_candidates(raw_results, top_n=top_n)

        if not ranked_results:
            st.warning("No matching resumes found.")
        else:
            st.subheader("Top Matching Candidates")

            for idx, candidate in enumerate(ranked_results, start=1):
                with st.container(border=True):
                    st.markdown(f"### {idx}. {candidate['candidate_name']}")
                    st.write(f"**File Name:** {candidate['file_name']}")
                    st.write(f"**Match Score:** {candidate['match_score']}%")
                    st.write(f"**Best Match Page:** {candidate['best_page']}")
                    st.write(f"**Matched Chunks:** {candidate['matched_chunks']}")
                    st.write("**Relevant Snippet:**")
                    st.info(candidate["best_snippet"])


st.subheader("3. Example Queries")
st.write("- Python developer with Django and REST API")
st.write("- React Node.js MongoDB full stack developer")
st.write("- Data scientist with NLP and machine learning")
st.write("- Java Spring Boot backend developer")