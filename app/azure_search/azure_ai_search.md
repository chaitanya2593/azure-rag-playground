
# Tool Usage and Module Overview

This project uses several Azure AI Search and OpenAI tools to build a Retrieval-Augmented Generation (RAG) pipeline. Below is a summary of each core module, what it does, and where it is used.

## Module Overview

### 1. `app/azure_search/index_setup.py`
**Purpose:** Defines and creates the Azure Search index schema, including fields for vector search, semantic configuration, and scoring profiles.
**Where Used:** Called in `app/azure_search_setup.py` as the first step of setup.

### 2. `app/azure_search/datasource_setup.py`
**Purpose:** Configures the Azure Blob Storage data source for Azure Search, connecting the indexer to your document storage.
**Where Used:** Called in `app/azure_search_setup.py` as the second step of setup.

### 3. `app/azure_search/skillset_setup.py`
**Purpose:** Sets up AI enrichment skills for data processing in Azure Search. This includes splitting documents into pages and generating vector embeddings for each page using Azure OpenAI. It also configures index projections and connects to a Cognitive Services account.
**Where Used:** Called in `app/azure_search_setup.py` as the third step of setup.

### 4. `app/azure_search/indexer_setup.py`
**Purpose:** Creates and runs the indexer, which populates the Azure Search index from the data source and applies the skillset for enrichment.
**Where Used:** Called in `app/azure_search_setup.py` as the fourth step of setup.

### 5. `app/azure_search_setup.py`
**Purpose:** Orchestrates the setup of the Azure Search index, data source, skillset, and indexer. Run this script once to initialize your Azure Search environment.
**Where Used:** Run directly as a script for initial setup.


## Setup Flow

1. Run `app/azure_search_setup.py` to create the index, data source, skillset, and indexer.
2. Use `app/streamlit.py` to interact with the system: ask questions, retrieve answers, and view results.

---

For more details, see the docstrings and comments in each module.
