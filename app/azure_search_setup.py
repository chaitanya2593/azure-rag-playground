"""
Run this script ONCE to set up the Azure Search index, data source, skillset, and indexer.
Not needed in the main Streamlit app.
"""

from app.azure_search.index_setup import IndexSetup
from app.azure_search.datasource_setup import DataSourceSetup
from app.azure_search.skillset_setup import SkillsetSetup
from app.azure_search.indexer_setup import IndexerSetup

if __name__ == "__main__":
    # IndexSetup().create() # Step 1: Create index (only if it doesn't exist). Basically we are creating the schema for the vector search index here, and we will populate it with the indexer that we create in Step 4.
    DataSourceSetup().create() # Step 2: Create data source (only if it doesn't exist)
    SkillsetSetup().create()  # Step 3: Create skillset (only if it doesn't exist)
    IndexerSetup().create() # Step 4: Create and run indexer (only if it doesn't exist)
    print("Azure Search setup complete.")
