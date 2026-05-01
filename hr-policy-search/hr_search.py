# Python Version: 3.11.6
# pip install chromadb sentence-transformers
# Run: python hr_search.py

import chromadb
from sentence_transformers import SentenceTransformer
import os
import shutil

# 1. Create a persistent Chroma client
db_path = "./hr_chroma_store"
if os.path.exists(db_path):
    shutil.rmtree(db_path) # Start fresh for the demonstration

client = chromadb.PersistentClient(path=db_path)

# Create a collection with embedding_function=None
collection_name = "hr_policies"
collection = client.create_collection(name=collection_name, embedding_function=None)

# 2. Invent at least 5 HR-style policy lines
policies = [
    {"id": "p1", "text": "Employees are entitled to 20 days of paid annual leave per year.", "metadata": {"category": "leave", "version": 1}},
    {"id": "p2", "text": "Our health insurance plan covers dental and vision checkups for all full-time staff.", "metadata": {"category": "benefits", "version": 1}},
    {"id": "p3", "text": "All employees must complete mandatory harassment prevention training annually.", "metadata": {"category": "conduct", "version": 1}},
    {"id": "p4", "text": "Sick leave requires a medical certificate if the absence exceeds three consecutive days.", "metadata": {"category": "leave", "version": 1}},
    {"id": "p5", "text": "Company laptops must be used for business purposes only and kept secure at all times.", "metadata": {"category": "conduct", "version": 1}}
]

# 3. Embed all documents with Sentence Transformers
print("Loading model and embedding documents...")
model = SentenceTransformer('all-MiniLM-L6-v2')

ids = [p["id"] for p in policies]
documents = [p["text"] for p in policies]
metadatas = [p["metadata"] for p in policies]
embeddings = model.encode(documents).tolist()

# Upsert into Chroma
collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

# 4. Print collection.count() and one peek()
print(f"Collection count: {collection.count()}")
print("\nPeek at collection:")
print(collection.peek(1))

# 5. Search A: one natural-language question
query_text_a = "What are my dental insurance options?"
query_embedding_a = model.encode([query_text_a]).tolist()

results_a = collection.query(
    query_embeddings=query_embedding_a,
    n_results=3
)

print(f"\nSearch A (Query: '{query_text_a}'):")
for i in range(len(results_a['ids'][0])):
    print(f"Rank {i+1}: ID={results_a['ids'][0][i]}, Snippet='{results_a['documents'][0][i]}', Metadata={results_a['metadatas'][0][i]}")

# 6. Search B: filtered query
query_text_b = "How many sick days can I take?"
query_embedding_b = model.encode([query_text_b]).tolist()

results_b = collection.query(
    query_embeddings=query_embedding_b,
    where={"category": "leave"},
    n_results=2
)

print(f"\nSearch B (Query: '{query_text_b}', Filter: 'leave'):")
for i in range(len(results_b['ids'][0])):
    print(f"Rank {i+1}: ID={results_b['ids'][0][i]}, Snippet='{results_b['documents'][0][i]}', Metadata={results_b['metadatas'][0][i]}")

# 7. Update: add a new document or upsert existing
print("\nUpdating policy p1...")
new_policy = {"id": "p1", "text": "Employees are now entitled to 25 days of paid annual leave per year due to the new policy update.", "metadata": {"category": "leave", "version": 2}}

collection.upsert(
    ids=[new_policy["id"]],
    documents=[new_policy["text"]],
    metadatas=[new_policy["metadata"]],
    embeddings=model.encode([new_policy["text"]]).tolist()
)

# Run one more filtered query
print(f"Search after update (Query: 'annual leave', Filter: 'leave'):")
query_text_c = "annual leave"
query_embedding_c = model.encode([query_text_c]).tolist()
results_c = collection.query(
    query_embeddings=query_embedding_c,
    where={"category": "leave"},
    n_results=2
)
for i in range(len(results_c['ids'][0])):
    print(f"Rank {i+1}: ID={results_c['ids'][0][i]}, Snippet='{results_c['documents'][0][i]}', Metadata={results_c['metadatas'][0][i]}")
