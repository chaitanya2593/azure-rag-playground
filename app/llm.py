from app.config import *
from app.cache import get_cached_answer, set_cached_answer
from openai import AzureOpenAI

SYSTEM_PROMPT = """
You are an AI assistant whose only task is to answer questions strictly based on the source materials provided in the prompt.

RESPONSE RULES:
1. Use ONLY information explicitly stated in the provided sources.  
   - Do NOT infer, assume, or introduce outside knowledge.
   - If a fact is not present in the sources, you must not use it.

2. Structure your response as follows:
   A) Explanation: Briefly explain the answer using ONLY the supported facts.  
   B) Sources: List up to 3 specific sources that directly support the answer.
      - Choose the most relevant ones.
      - If no source directly supports the answer, state: “I don’t know.”

3. If the question cannot be answered using the provided sources:
   - Say: “I don’t know.”
   - Do NOT attempt to fill gaps with external knowledge.

4. If the question is unrelated to the content of the provided sources:
   - Say: “This question is irrelevant to the provided research area.”

5. Keep the tone factual, neutral, and helpful.
6. Keep answers concise and avoid speculation.

Your entire output MUST comply with the above rules.
Query: {query}
Sources:\n{sources}
"""

def format_sources(results):
    return "=================\n".join([
        f'TITLE: {doc["title"]}, CONTENT: {doc["content"]}' for doc in results
    ])

def get_llm_response(query, results):
    if not results:
        return "Sorry, we can't answer this question. We are happy to help with any other question?"
    # Check Redis cache first
    cached = get_cached_answer(query, results)
    if cached:
        print("[CACHE] Returning cached answer for query.")
        return cached
    openai_client = AzureOpenAI(
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY
    )
    sources_formatted = format_sources(results)
    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": SYSTEM_PROMPT.format(query=query, sources=sources_formatted)
            }
        ],
        model=AZURE_OPENAI_DEPLOYMENT
    )
    answer = response.choices[0].message.content
    set_cached_answer(query, answer, results)
    return answer
