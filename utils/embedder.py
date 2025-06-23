import json
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CHROMA_DIR = "/code/chroma_db"
CHUNKS_PATH = "hr_policies/hr_chunks.json"

client = chromadb.Client(
    chromadb.config.Settings(persist_directory=CHROMA_DIR)
)

embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

try:
    collection = client.get_collection(name="hr_docs")
except:
    collection = client.create_collection(name="hr_docs", embedding_function=embedding_func)

with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk["content"]],
        ids=[f"chunk_{i}"],
        metadatas=[{"source": chunk["source"]}]
    )

print(f"Embedded {len(chunks)} chunks into ChromaDB.")

