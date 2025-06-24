import gzip
import os
import json
import re
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CHROMA_DIR = "/code/chroma_db"
SOURCE_DIR = "/code/hr_policies"
CHUNKS_PATH = os.path.join(SOURCE_DIR, "hr_chunks.json")

embedding_func = SentenceTransformerEmbeddingFunction(model_name="paraphrase-MiniLM-L3-v2")


def clean_markdown(text):
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text)
    text = re.sub(r"#+ ", "", text)
    return text.strip()


def chunk_text(text, max_words=100):
    paragraphs = text.split("\n\n")
    chunks = []
    buffer = ""
    for p in paragraphs:
        if len((buffer + p).split()) < max_words:
            buffer += " " + p
        else:
            chunks.append(buffer.strip())
            buffer = p
    if buffer:
        chunks.append(buffer.strip())
    return chunks


def load_markdown_files():
    chunks = []
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".md"):
            with open(os.path.join(SOURCE_DIR, filename), "r", encoding="utf-8") as f:
                raw = f.read()
                text = clean_markdown(raw)
                subchunks = chunk_text(text)
                for chunk in subchunks:
                    chunks.append({
                        "source": filename,
                        "content": chunk
                    })
    return chunks


def initialize_chroma():
    print("Initializing Chroma...")
    client = chromadb.Client(chromadb.config.Settings(persist_directory=CHROMA_DIR))

    if "hr_docs" in {c.name for c in client.list_collections()}:
        print("Chroma already initialized.")
        return

    gz_path = CHUNKS_PATH + ".gz"

    # Try loading from gzipped file
    if os.path.exists(gz_path):
        print("Loading chunks from compressed JSON...")
        with gzip.open(gz_path, "rt", encoding="utf-8") as f:
            chunks = json.load(f)
    else:
        print("Reading markdown files...")
        chunks = load_markdown_files()
        os.makedirs(os.path.dirname(gz_path), exist_ok=True)
        with gzip.open(gz_path, "wt", encoding="utf-8") as f:
            json.dump(chunks, f)

    # Embed
    collection = client.create_collection(name="hr_docs", embedding_function=embedding_func)
    print("Collection created: hr_docs")
    print(f"Embedding {len(chunks)} chunks...")

    documents = [c["content"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": c["source"]} for c in chunks]

    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    print(f"Finished embedding {len(chunks)} chunks.")

