
import importlib.machinery
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

load_dotenv()

llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini", temperature=0)




#-------------------------Will use this part for improving the performance of the Graph later-------------
#------------------------------------------------------------------------------------------------------------
# example_prompt = PromptTemplate.from_template(
#     "User input: {question}\nCypher query: {query}"
#     )


# cypher_prompt = FewShotPromptTemplate(
#     examples=examples,    
#     example_prompt=example_prompt,    
#     prefix="""
#     You are a Neo4j expert. Given an input question, create a syntactically correct    
#     Cypher query to run. \n\nHere is the schema information\n{schema}.\n\n    
#     Below are a number of examples of questions and their corresponding Cypher queries.
#     """,    
#     suffix="User input: {question}\nCypher query: ",    
#     input_variables=["question"],
#     )
 
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

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
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True, # Required in newer versions for Cypher execution
    validate_cypher=True 
)

# 4. Run a test query
response = chain.invoke({"query": "how many users are following user 701?"})

print(response)