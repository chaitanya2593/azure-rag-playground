from app import config
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SplitSkill, InputFieldMappingEntry, OutputFieldMappingEntry, AzureOpenAIEmbeddingSkill, EntityRecognitionSkill,
    SearchIndexerIndexProjection, SearchIndexerIndexProjectionSelector, SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode, SearchIndexerSkillset, CognitiveServicesAccountKey
)

DOCUMENT_PAGES_CONTEXT = "/document/pages/*"

class SkillsetSetup:
    def __init__(self):
        self.credential = AzureKeyCredential(config.AZURE_SEARCH_SERVICE_ADMIN_KEY)
        self.client = SearchIndexerClient(endpoint=config.AZURE_SEARCH_SERVICE_ENDPOINT, credential=self.credential)

    def create(self):
        split_skill = SplitSkill(
            description="Split skill to chunk documents",
            text_split_mode="pages",
            context="/document",
            maximum_page_length=2000,
            page_overlap_length=500,
            inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
            outputs=[OutputFieldMappingEntry(name="textItems", target_name="pages")],
        )
        embedding_skill = AzureOpenAIEmbeddingSkill(
            description="Skill to generate embeddings via Azure OpenAI",
            context=DOCUMENT_PAGES_CONTEXT,
            resource_url=config.AZURE_OPENAI_ENDPOINT,
            deployment_name=config.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT,
            model_name=config.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT,
            dimensions=1024,
            inputs=[InputFieldMappingEntry(name="text", source=DOCUMENT_PAGES_CONTEXT)],
            outputs=[OutputFieldMappingEntry(name="embedding", target_name="contentVector")],
        )
        index_projections = SearchIndexerIndexProjection(
            selectors=[
                SearchIndexerIndexProjectionSelector(
                    target_index_name=config.AZURE_SEARCH_SERVICE_INDEX_NAME,
                    parent_key_field_name="parent_id",
                    source_context=DOCUMENT_PAGES_CONTEXT,
                    mappings=[
                        InputFieldMappingEntry(name="content", source=DOCUMENT_PAGES_CONTEXT),
                        InputFieldMappingEntry(name="contentVector", source=f"{DOCUMENT_PAGES_CONTEXT}/contentVector"),
                        InputFieldMappingEntry(name="title", source="/document/metadata_storage_name"),
                    ],
                ),
            ],
            parameters=SearchIndexerIndexProjectionsParameters(
                projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS
            ),
        )
        cognitive_services_account = CognitiveServicesAccountKey(key=config.AZURE_AI_MULTISERVICE_KEY)
        skills = [split_skill, embedding_skill]
        skillset = SearchIndexerSkillset(
            name=config.SKILLSET_NAME,
            description="Skillset to chunk documents, generate embeddings",
            skills=skills,
            index_projection=index_projections,
            cognitive_services_account=cognitive_services_account
        )
        self.client.create_or_update_skillset(skillset)
        print(f"{skillset.name} created or updated.")

