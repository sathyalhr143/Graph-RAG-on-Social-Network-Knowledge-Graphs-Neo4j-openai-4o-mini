import os
from langchain_community.document_loaders import CSVLoader

from load_data import USERS_CSV, EDGES_CSV
from langchain_text_splitters import TokenTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
# from lanchain_openai import OpenAIEmbeddings
from langchain_experimental.graph_transformers import LLMGraphTransformer
# from langchain_community.graphs import Neo4jGraph
from langchain_neo4j import Neo4jGraph
import pandas as pd
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()   

df_users = pd.read_csv(USERS_CSV)
df_edges = pd.read_csv(EDGES_CSV)


loader_users = CSVLoader(file_path=USERS_CSV)
docs_users = loader_users.load()
print(docs_users[0])

loader_edges = CSVLoader(file_path=EDGES_CSV)
docs_edges = loader_edges.load()
print(docs_edges[0])


# Example of formatting a row into a "chunk" for the LLM
def row_to_chunk(users, edges):
    return (
        f"""User {users['name']} works in {users['company']} company has
        {users['followers']} followers and follows {users['following']} people in facebook with {users['posts_30d']} posts in last 30 days and interested in {users['topics']}. 
        """
    )








# 1. Create all User Nodes
# We will store them in a dictionary so we can easily look them up when creating edges
user_nodes = {}
for _, row in df_users.iterrows():
    user_id = str(row['login'])
    node = Node(
        id=user_id, 
        type="User", 
        properties={
            # Add any other useful metadata you want Neo4j to index
            "topics": row.get('topics', ''),
            "company": row.get('company', ''),
            "followers": row.get('followers', 0),
            "following": row.get('following', 0),
            "posts_30d": row.get('posts_30d', 0)
        }
    )
    user_nodes[user_id] = node

# 2. Create all Relationships (Edges)
relationships = []
for _, row in df_edges.iterrows():
    src_id = str(row['src'])
    dst_id = str(row['dst'])
    
    # Only create an edge if both the source and target nodes exist
    if src_id in user_nodes and dst_id in user_nodes:
        rel = Relationship(
            source=user_nodes[src_id],
            target=user_nodes[dst_id],
            type=str(row['etype']).upper()  # Usually standard to uppercase relationships (e.g., "FOLLOW")
        )
        relationships.append(rel)

# 3. Create a unified GraphDocument
# A GraphDocument expects a source document, a list of Nodes, and a list of Relationships
graph_doc = GraphDocument(
    nodes=list(user_nodes.values()),
    relationships=relationships,
    source=Document(page_content="Graph built from curated CSVs")
)

# 4. Insert into Graph Database
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"), # Update with your Neo4j credentials
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE")
)

# Set baseEntityLabel to True if you want a generic '__Entity__' label on all nodes alongside 'User'
graph.add_graph_documents([graph_doc], baseEntityLabel=True,include_source=True )

print(f"Added {len(user_nodes)} nodes and {len(relationships)} relationships to Neo4j!")
print(graph.get_schema)