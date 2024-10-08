from neo4j import GraphDatabase

# Demo database credentials
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

import os
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings

embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

from neo4j_graphrag.retrievers import HybridCypherRetriever

retrieval_query = """
MATCH (actor:Actor)-[:ACTED_IN]->(movie:Movie)
RETURN movie.title AS movie_title,
       movie.plot AS movie_plot,
       collect(actor.name) AS actors;
"""

retriever = HybridCypherRetriever(
    driver=driver,
    vector_index_name="moviePlotsEmbedding",
    fulltext_index_name="movieFulltext",
    retrieval_query=retrieval_query,
    embedder=embedder,
)

from neo4j_graphrag.generation import GraphRAG

llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
rag = GraphRAG(retriever=retriever, llm=llm)
query_text = "What are the names of the actors in the movie set in 1375 in Imperial China?"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)
