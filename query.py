# # from main import graph
# from langchain_openai import ChatOpenAI
# from langchain_neo4j import Neo4jGraph
# from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
# from dotenv import load_dotenv
# import os

# load_dotenv()

# graph = Neo4jGraph(
#     url=os.getenv("NEO4J_URL"), 
#     username=os.getenv("NEO4J_USERNAME"), 
#     password=os.getenv("NEO4J_PASSWORD"),
#     database="b98fda26"
# )

# graph.refresh_schema()

# chain = GraphCypherQAChain.from_llm(
#     llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4o-mini", temperature=0),
#     graph=graph, 
#     verbose=True
#     )

# result = chain.invoke({"query": "who is the most followed person?"})

# print(result['result'])


import importlib.machinery
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# 1. Initialize the Graph
# This uses the newer langchain_neo4j library which is more stable for GraphRAG
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE")
)

# 2. Refresh the schema 
# This helps the LLM understand your specific "User" and "FOLLOW" structure
graph.refresh_schema()

# 3. Setup the Chain
# Using Neo4jCypherChain instead of GraphCypherQAChain to avoid the Pydantic error
chain = GraphCypherQAChain.from_llm(
    llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini", temperature=0),
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True # Required in newer versions for Cypher execution
)

# 4. Run a test query
response = chain.invoke({"query": "Who follows user 19837?"})
print(response)