# Graph RAG on Social Network Knowledge Graphs using Neo4j and OpenAI

This repository demonstrates the implementation of a **Graph Retrieval-Augmented Generation (GraphRAG)** system built on a social network dataset. It transforms structured tabular data (CSVs) into a powerful Neo4j property graph, allowing an LLM (OpenAI's `gpt-4o-mini`) to seamlessly answer questions about relationships and user metadata using LangChain.

## 🚀 Features

*   **Native Graph Construction**: Bypasses expensive and error-prone LLM extraction by directly converting deterministic tabular data (`users.csv` and `edges_follow.csv`) into Neo4j Nodes and Relationships.
*   **LangChain Integration**: Utilizes LangChain's `Neo4jGraph` and `GraphCypherQAChain` to bridge natural language and Cypher queries.
*   **Decoupled Architecture**: 
    *   `main.py`: Handles data loading from the cloud, node/edge parsing, and populates the Neo4j database.
    *   `query.py`: Connects to the active Neo4j database and executes autonomous Natural-Language-to-Cypher translations to answer user questions.

## 🗂️ Dataset
The data mimics a social network environment:
*   **Users**: Contains metadata such as `name`, `company`, `followers`, `following`, `topics` of interest, and recent post activity.
*   **Edges**: Maps explicit `FOLLOWS` relationships between source and destination users.

## 🛠️ Setup Instructions

### 1. Prerequisites
*   Python 3.10+
*   A running instance of [Neo4j](https://neo4j.com/cloud/platform/aura-graph-database/) (AuraDB Free Tier works perfectly).
*   An OpenAI API Key.

### 2. Installation
Clone the repository and install the dependencies (assuming you are using a virtual environment like `.venv`):

```bash
git clone https://github.com/sathyalhr143/Graph-RAG-on-Social-Network-Knowledge-Graphs-Neo4j-openai-4o-mini.git
cd Graph-RAG-on-Social-Network-Knowledge-Graphs-Neo4j-openai-4o-mini
pip install pandas langchain-community langchain-core langchain-openai langchain-neo4j neo4j python-dotenv
```

### 3. Environment Variables
Create a `.env` file in the root of the project with your database and API credentials:

```ini
NEO4J_URI=neo4j+s://<YOUR_AURA_INSTANCE_ID>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>
NEO4J_DATABASE=<YOUR_AURA_INSTANCE_ID>
OPENAI_API_KEY=sk-<YOUR_OPENAI_API_KEY>
```

### 4. Running the Project

**Step 1: Ingest the Graph Data**
Run the main script to download the CSVs, generate the graph schema, and push 340,000+ relationships into your Neo4j database.
```bash
python main.py
```

**Step 2: Ask Questions!**
Once the database is populated, use `query.py` to chat with the graph.
```bash
python query.py
```

*Example Query output:*
```text
> Entering new GraphCypherQAChain chain...
Generated Cypher:
MATCH (u:User)-[:FOLLOW]->(f:User {id: '19837'}) RETURN u

> Finished chain.
{'query': 'Who follows user 19837?', 'result': '...'}
```

## ⚠️ Notes
*   If using Neo4j free Aura tier, ensure your `NEO4J_DATABASE` variable is set correctly in `.env` (it usually matches your instance ID or defaults to `neo4j`).

* This project does not use any embeddings or vector stores. It uses Neo4j's native graph database to store and query the data.
* This project does not yield complicated results as it is built on a small dataset. I aim to build a different project with the same dataset but with a different approach.
