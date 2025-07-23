import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os
import re

# 🧠 Load model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Setup ChromaDB persistent client
chroma_client = chromadb.PersistentClient(path="./chroma_storage")
collection = chroma_client.get_or_create_collection(
    name="medical_memory",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

# 📥 Store user memory
def store_user_memory(messages, user_id):
    for i, msg in enumerate(messages):
        content = msg["content"] if isinstance(msg, dict) else msg
        collection.add(
            documents=[content],
            metadatas=[{"user_id": user_id}],
            ids=[f"{user_id}_{i}_{len(content)}"]
        )

# 📤 Retrieve user memory
def retrieve_user_memory(user_id, query="summary of previous interaction"):
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"user_id": user_id},
        include=["documents"]
    )
    return results["documents"][0] if results["documents"] else None

# 🧪 Dummy data
def manually_store_dummy_data(user_id):
    dummy_messages = [
        {"role": "user", "content": "Patient reports headache, nausea, and sensitivity to light."},
        {"role": "assistant", "content": "Possible migraine. Recommend hydration and rest."},
        {"role": "assistant", "content": "If persists, consult neurologist."}
    ]
    store_user_memory(dummy_messages, user_id)
    print("✅ Dummy data inserted into Chroma memory.")

# 📊 Extract structured summary from conversation
def extract_structured_summary(full_convo: str) -> str:
    # Simple regex-based summary extractor
    match = re.search(r"✅ Final Structured Summary:(.*?)($|\n\n|\Z)", full_convo, re.DOTALL)
    return match.group(0).strip() if match else "Summary not found."