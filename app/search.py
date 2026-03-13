from app.config import *
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery

def hybrid_search(query, top_k=3, k_nearest_neighbors=50):
    credential = AzureKeyCredential(AZURE_SEARCH_SERVICE_ADMIN_KEY)
    search_client = SearchClient(
        endpoint=AZURE_SEARCH_SERVICE_ENDPOINT,
        credential=credential,
        index_name=AZURE_SEARCH_SERVICE_INDEX_NAME
    )
    vector_query = VectorizableTextQuery(
        text=query,
        k_nearest_neighbors=k_nearest_neighbors,
        fields="contentVector",
        weight=1
    )
    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query] ,
        select=["title", "content"],
        top=top_k
    )
    return list(results)

def semantic_hybrid_search(query, top_k=3, k_nearest_neighbors=50, tags=None):
    credential = AzureKeyCredential(AZURE_SEARCH_SERVICE_ADMIN_KEY)
    search_client = SearchClient(
        endpoint=AZURE_SEARCH_SERVICE_ENDPOINT,
        credential=credential,
        index_name=AZURE_SEARCH_SERVICE_INDEX_NAME
    )
    vector_query = VectorizableTextQuery(
        text=query,
        k_nearest_neighbors=k_nearest_neighbors,
        fields="contentVector",
        weight=1
    )

    results = search_client.search(
        query_type="semantic",
        semantic_configuration_name=SEMANTIC_CONFIG_NAME,
        scoring_profile=SCORING_PROFILE_NAME,
        scoring_parameters=["tags-beach, 'United States'"],
        search_text=query,
        vector_queries=[vector_query],
        select=["title", "content"],
        top=top_k
    )
    print("Semantic Hybrid Search Results:" + str("".join([item for item in results])))
    return sorted(list(results), key=lambda x: x['@search.score'], reverse=True)
