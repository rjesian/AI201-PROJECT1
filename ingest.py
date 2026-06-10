import os

def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({"filename": filename, "text": text})
    return documents

def clean_text(text):
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith("LINK:"):
            continue
        if "reddit.com" in line:
            continue
        if line == "":
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def chunk_text(text, filename, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk) > 0:
            chunks.append({"text": chunk, "source": filename})
            start = end - overlap
    return chunks



docs = load_documents("redditdocs")

if __name__ == "__main__":
    docs = load_documents("redditdocs")

    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, doc["filename"])
        all_chunks.extend(chunks)

    print(f"Total chunks: {len(all_chunks)}")
    print("--- Sample Chunk 1 ---")
    print(all_chunks[0]["text"])
    print("--- Sample Chunk 2 ---")
    print(all_chunks[5]["text"])