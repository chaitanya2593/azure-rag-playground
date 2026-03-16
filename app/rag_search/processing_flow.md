# Semantic Search Processing Flow

A step-by-step explanation of how your semantic search works when you ask a question like “What does inflation mean?”:

---

## Step 1: User Asks a Question
You type a question in the Streamlit app, e.g.,
> **“What does inflation mean?”**

---

## Step 2: The App Embeds Your Question
The app uses a pre-trained model (`sentence-transformers/all-MiniLM-L6-v2`) to turn your question into a vector (a list of numbers that represents the meaning of your question).

- This is called an **embedding**.
- It helps the computer compare your question to the content of your documents in a smart, meaning-based way.

---

## Step 3: The App Loads All Document Indexes
The app looks in your `data/faiss` folder for all FAISS index files. Each index represents the “memory” of one document’s chunks (small pieces of text).

---

## Step 4: The App Searches for Similar Chunks
For each document:
- It loads the FAISS index (which contains the embeddings of all the chunks from that document).
- It also loads the actual text chunks (from a `.pkl` file).
- It asks FAISS: “Which chunks are most similar to the question’s embedding?”
- FAISS returns the top N most similar chunks (by default, top 3).

---

## Step 5: The App Collects the Best Chunks
For each document, the app collects the most relevant chunks (the ones that are closest in meaning to your question).

---

## Step 6: The App Passes Chunks to the LLM
The app sends your question and the best-matching chunks to the language model (LLM).
- The LLM reads only those chunks and tries to answer your question using just that information.

---

## Step 7: The App Shows the Answer
The answer is shown in the chat, along with a message if there’s not enough information:
> _“Sorry, we can’t answer this question. We are happy to help with any other question?”_

---

## Visual Summary

```mermaid
flowchart TD
    A[You ask a question] --> B[App turns question into a vector (embedding)]
    B --> C[App loads all document indexes]
    C --> D[App finds the most similar text chunks in all documents]
    D --> E[App sends those chunks + your question to the LLM]
    E --> F[LLM answers using only those chunks]
    F --> G[You see the answer in the chat]
```
