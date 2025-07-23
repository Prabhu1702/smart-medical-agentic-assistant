# # langmen_memory.py

# from langmem import create_memory_store_manager
# from pydantic import BaseModel
# from langgraph.store.memory import InMemoryStore
# from sentence_transformers import SentenceTransformer

# # Define memory schema for LangMem
# class Triple(BaseModel):
#     subject: str
#     predicate: str
#     object: str
#     context: str | None = None

# # Initialize HuggingFace embedding model
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# def hf_embed(texts: list[str]) -> list[list[float]]:
#     """Embed text using HuggingFace model"""
#     return embedding_model.encode(texts).tolist()

# # InMemoryStore with custom embedding function
# store = InMemoryStore(
#     index={
#         "dims": 384,  # all-MiniLM-L6-v2 returns 384-dimensional vectors
#         "embed": hf_embed,
#     }
# )

# # Create memory manager using LangMem
# manager = create_memory_store_manager(
#     "anthropic:claude-3-5-sonnet-latest",
#     store=store,  # ✅ Attach your in-memory store here
#     namespace=("chat", "{user_id}", "triples"),
#     schemas=[Triple],
#     instructions="Extract all user medical information, symptoms, diagnosis, and treatment.",
#     enable_inserts=True,
#     enable_deletes=True,
# )

# def store_user_memory(messages: list, user_id: str):
#     """Store triples from a user interaction"""
#     manager.invoke(
#     input={"messages": messages, "input": "user medical interaction"},
#     config={"configurable": {"user_id": user_id}},
# )
# def retrieve_user_memory(user_id: str):
#     """Retrieve stored memory triples for a user"""
#     return list(store.search(("chat", user_id)))

# def manually_store_dummy_data(user_id: str):
#     """Manually store example triples for testing retrieval"""
#     dummy_data = [
#         {"subject": "User", "predicate": "has symptom", "object": "dry cough"},
#         {"subject": "User", "predicate": "has diagnosis", "object": "viral fever"},
#         {"subject": "User", "predicate": "requires treatment", "object": "paracetamol and rest"},
#     ]
#     content = "\n".join([f"{t['subject']} {t['predicate']} {t['object']}" for t in dummy_data])
#     messages = [{"role": "user", "content": content}]
#     store_user_memory(messages, user_id)
#     print(f"\n✅ Dummy data stored successfully for user: {user_id}")
