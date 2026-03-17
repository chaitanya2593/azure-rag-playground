import streamlit as st
from app.search import semantic_hybrid_search
from app.llm import get_llm_response
from app.pipeline import process_document
import os

# Set page config FIRST and only ONCE
st.set_page_config(page_title="Researcher Playground", page_icon="🔍", layout="centered")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Research Assistant Chatbot", "Metadata Inventory & PDF Processing"])

if page == "Research Assistant Chatbot":
    st.title("Research Assistant Chatbot")
    st.write("Ask questions about the documents you uploaded and let the AI assistant help you find answers based on the content of those documents.")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    user_input = st.chat_input("Ask a question about the documents...")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.spinner("Searching and generating answer..."):
            search_results = semantic_hybrid_search(user_input, top_k=3)
            answer = get_llm_response(user_input, search_results)
        st.session_state["messages"].append({"role": "assistant", "content": answer})

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

elif page == "Metadata Inventory & PDF Processing":
    st.title("Metadata Inventory & PDF Processing")
    st.write("Upload new PDFs and run the end-to-end pipeline to process, chunk, embed, and index your documents.")

    pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'papers')
    processed = False

    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        save_path = os.path.join(pdf_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name} successfully!")
        if st.button("Run Pipeline on Uploaded PDF"):
            process_document(save_path)
            st.success(f"Pipeline completed for {uploaded_file.name}!")
            processed = True

    # Refresh/Run pipeline on all PDFs
    if st.button("Refresh & Run Pipeline on All PDFs"):
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        for pdf_file in pdf_files:
            process_document(os.path.join(pdf_dir, pdf_file))
        st.success("Pipeline completed for all PDFs!")
        processed = True
    if st.button("Available PDFs"):
        # List all PDFs with processing status and option to process
        st.subheader("Available PDFs in Inventory:")
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        processed_files = set()
        # Check for processed files by existence of FAISS index
        faiss_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'faiss')
        for pdf_file in pdf_files:
            doc_name = os.path.splitext(pdf_file)[0]
            faiss_index_path = os.path.join(faiss_dir, f"{doc_name}_faiss.index")
            if os.path.exists(faiss_index_path):
                processed_files.add(pdf_file)

        import pandas as pd
        table_data = []
        for pdf_file in pdf_files:
            status = "Processed" if pdf_file in processed_files else "Not Processed"
            table_data.append({"PDF File": pdf_file, "Status": status})
        df = pd.DataFrame(table_data)
        st.table(df)
