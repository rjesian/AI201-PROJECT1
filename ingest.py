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
        if line == "":
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


docs = load_documents("redditdocs")
print(f"Loaded {len(docs)} documents")

cleaned_text = clean_text(docs[0]["text"])
print(cleaned_text[:500])


