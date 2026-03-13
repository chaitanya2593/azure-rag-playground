import streamlit as st
from app.search import semantic_hybrid_search, hybrid_search
from app.llm import get_llm_response

st.set_page_config(page_title="Azure RAG Playground", page_icon="🤖", layout="centered")
st.title("Research Assistant Chatbot")
st.write("Ask questions about the documents you uploaded and let the AI assistant help you find answers based on the content of those documents.")
if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("Ask a question about the documents...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Searching and generating answer..."):
        search_results = hybrid_search(user_input, top_k=5)
        answer = get_llm_response(user_input, search_results)
    st.session_state["messages"].append({"role": "assistant", "content": answer})

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

