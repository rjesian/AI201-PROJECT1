import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_documents, clean_text, chunk_text

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="sbu_guide")

docs = load_documents("redditdocs")

all_chunks = []
for doc in docs:
    cleaned = clean_text(doc["text"])
    chunks = chunk_text(cleaned, doc["filename"])
    all_chunks.extend(chunks)

print(f"Embedding {len(all_chunks)} chunks...")

for i, chunk in enumerate(all_chunks):
    embedding = model.encode(chunk["text"]).tolist()
    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[embedding],
        documents=[chunk["text"]],
        metadatas=[{"source": chunk["source"]}]
    )

print("Done. All chunks embedded and stored in ChromaDB.")

