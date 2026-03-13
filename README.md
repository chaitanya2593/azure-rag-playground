# azure-rag-playground
This repository explores an experimental Retrieval-Augmented Generation (RAG) pipeline using Azure AI Search + Azure OpenAI. The project is intended for learning and rapid prototyping.

## Azure Prerequisites
Before running the app, create these Azure resources:

1. **Azure OpenAI resource**
   - Create at least two deployments:
     - one chat/completions model deployment (for answer generation)
     - one embeddings model deployment (for vectorization)
     - Note the deployments should be latest available models in your region.
2. **Azure AI Search service**
   - Admin key enabled
   - Index name available (or let setup scripts create it)
3. **Azure Storage account (Blob Storage)**
   - Create a blob container for source documents (default used in code: `fileupload-researchpaper`)
4. **Azure AI multi-service resource key**
   - Used by search skillset enrichment in this project

5. This app is intended to process the PDF research papers, so you can upload some sample PDFs to the blob container or modify the code to use other document types.

- Please refer to the azure setup readme for detailed instructions on creating these resources and configuring access: `app/azure_search/azure_ai_search.md`

## Local Setup (with uv)
1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install [uv](https://github.com/astral-sh/uv) if needed:
```bash
pip install uv
```

3. Sync dependencies:
```bash
uv sync
```

## Initialize Azure Search Assets
Run the setup script once to create datasource, index, skillset, and indexer:

```bash
python app/azure_search_setup.py
```

## Run the Streamlit App
```bash
streamlit run streamlit.py
```
Please chat with the bot in the Streamlit UI and observe how it retrieves and generates answers based on the uploaded documents.

## Sources &  Research
- Based on the https://www.linkedin.com/learning/azure-for-developers-retrieval-augmented-generation-rag-with-azure-ai
- When we need RAG: https://www.youtube.com/watch?v=UabBYexBD4k

