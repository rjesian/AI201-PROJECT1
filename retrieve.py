from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="sbu_guide")

def retrieve(query, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results = k,
        include=["documents", "metadatas", "distances"]
    )
    chunks =[]
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

query = "What are some easy SBC classes to take at SBU?"
results = retrieve(query)

print(f"Query: {query}\n")
for i, result in enumerate(results):
    print(f"--- Result {i+1} ---")
    print(f"Source: {result['source']}")
    print(f"Distance: {result['distance']:.4f}")
    print(f"Text: {result['text']}")
    print()