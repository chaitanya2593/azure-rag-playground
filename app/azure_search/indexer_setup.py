from app import config
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndexer, IndexingSchedule
from datetime import timedelta

class IndexerSetup:
    def __init__(self):
        self.credential = AzureKeyCredential(config.AZURE_SEARCH_SERVICE_ADMIN_KEY)
        self.indexer_client = SearchIndexerClient(endpoint=config.AZURE_SEARCH_SERVICE_ENDPOINT, credential=self.credential)

    def create(self):
        schedule = IndexingSchedule(interval=timedelta(days=1))
        indexer = SearchIndexer(
            name=config.INDEXER_NAME,
            description="Indexer to index documents, generate embeddings, and extract entities",
            skillset_name=config.SKILLSET_NAME,
            target_index_name=config.AZURE_SEARCH_SERVICE_INDEX_NAME,
            data_source_name=config.DATASOURCE_NAME,
            parameters=None,
            schedule=schedule
        )
        self.indexer_client.create_or_update_indexer(indexer)
        print(f"{config.INDEXER_NAME} created and running.")

