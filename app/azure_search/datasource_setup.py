from app import config
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndexerDataContainer, SearchIndexerDataSourceConnection

class DataSourceSetup:
    def __init__(self):
        self.credential = AzureKeyCredential(config.AZURE_SEARCH_SERVICE_ADMIN_KEY)
        self.indexer_client = SearchIndexerClient(endpoint=config.AZURE_SEARCH_SERVICE_ENDPOINT, credential=self.credential)

    def create(self):
        container = SearchIndexerDataContainer(name=config.BLOB_CONTAINER_NAME)
        data_source_connection = SearchIndexerDataSourceConnection(
            name=config.DATASOURCE_NAME,
            type="azureblob",
            connection_string=config.AZURE_STORAGE_CONNECTION_STRING,
            container=container
        )
        data_source = self.indexer_client.create_or_update_data_source_connection(data_source_connection)
        print(f"Data source '{data_source.name}' created or updated.")

if __name__ == "__main__":
    setup = DataSourceSetup()
    setup.create()