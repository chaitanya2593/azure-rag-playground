from app import config
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchField, SearchFieldDataType, VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
    AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters, SearchIndex, SemanticConfiguration,
    SemanticPrioritizedFields, SemanticField, SemanticSearch, ScoringProfile, TagScoringFunction, TagScoringParameters
)

class IndexSetup:
    def __init__(self):
        self.credential = AzureKeyCredential(config.AZURE_SEARCH_SERVICE_ADMIN_KEY)
        self.index_client = SearchIndexClient(endpoint=config.AZURE_SEARCH_SERVICE_ENDPOINT, credential=self.credential)

    def create(self):
        fields = [
            SearchField(name="parent_id", type=SearchFieldDataType.String),
            SearchField(name="title", type=SearchFieldDataType.String),
            SearchField(name="locations", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
            SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),
            SearchField(name="content", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),
            SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=1024, vector_search_profile_name=config.VECTOR_SEARCH_PROFILE_NAME)
        ]
        vector_search = VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name=config.VECTOR_ALGORITHM_NAME)],
            profiles=[VectorSearchProfile(name=config.VECTOR_SEARCH_PROFILE_NAME, algorithm_configuration_name=config.VECTOR_ALGORITHM_NAME, vectorizer_name=config.VECTORIZER_NAME)],
            vectorizers=[AzureOpenAIVectorizer(
                vectorizer_name=config.VECTORIZER_NAME, kind="azureOpenAI",
                parameters=AzureOpenAIVectorizerParameters(
                    resource_url=config.AZURE_OPENAI_ENDPOINT,
                    deployment_name=config.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT,
                    model_name=config.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT
                ),
            )],
        )
        semantic_config = SemanticConfiguration(
            name=config.SEMANTIC_CONFIG_NAME,
            prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="title"),
                keywords_fields=[SemanticField(field_name="locations")],
                content_fields=[SemanticField(field_name="chunk")]
            )
        )
        semantic_search = SemanticSearch(configurations=[semantic_config])
        scoring_profiles = [
            ScoringProfile(
                name=config.SCORING_PROFILE_NAME,
                functions=[
                    TagScoringFunction(
                        field_name="locations", boost=5.0,
                        parameters=TagScoringParameters(tags_parameter="tags"),
                    )
                ]
            )
        ]
        index = SearchIndex(
            name=config.AZURE_SEARCH_SERVICE_INDEX_NAME,
            fields=fields,
            vector_search=vector_search,
            semantic_search=semantic_search,
            scoring_profiles=scoring_profiles
        )
        result = self.index_client.create_or_update_index(index)
        print(f"{result.name} created or updated.")

