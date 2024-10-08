# tag::setup[]
from neo4j import GraphDatabase
uri = "neo4j+s://demo.neo4jlabs.com"
username = "recommendations"
password = "recommendations"
driver = GraphDatabase.driver(uri, auth=(username, password))
# end::setup[]

# tag::embedder[]
import os
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = "sk-…"
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
# end::embedder[]

# tag::retriever[]
from neo4j_graphrag.retrievers import VectorRetriever

# Build the retriever
retriever = VectorRetriever(
    driver,
    index_name="moviePlotsEmbedding",
    embedder=embedder,
    return_properties=["title", "plot"],
)# end::retriever[]

# tag::graphrag[]
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.llm import OpenAILLM

llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
rag = GraphRAG(retriever=retriever, llm=llm)
query_text = "A movie about the famous Titanic ship"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)
# end::graphrag[]