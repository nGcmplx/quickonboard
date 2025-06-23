import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CHROMA_DIR = "/code/chroma_db"
THRESHOLD_HIGH = 0.75
THRESHOLD_LOW = 0.4

embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.Client(chromadb.config.Settings(persist_directory=CHROMA_DIR))

# 👇 Lazy-loaded global collection reference
collection = None

def get_collection():
    global collection
    if collection is None:
        collection = client.get_collection("hr_docs")
        collection._embedding_function = embedding_func
    return collection

def retrieve_relevant_chunks(query: str) -> tuple[list[str], str]:
    col = get_collection()

    print("🔍 Querying Chroma with:", query)
    print("📁 Chroma dir:", CHROMA_DIR)
    print("📚 Collections:", [c.name for c in client.list_collections()])
    print("📊 Collection count:", col.count())

    results = col.query(
        query_texts=[query],
        n_results=3,
        include=["documents", "distances"]
    )

    if not results["documents"] or not results["documents"][0]:
        print("❌ No relevant documents found.")
        return [], "none"

    chunks = results["documents"][0]
    scores = results["distances"][0]

    print("🧠 Retrieved Chunks:", chunks)
    print("📈 Scores:", scores)

    best_score = scores[0] if scores else 0

    if best_score >= THRESHOLD_HIGH:
        return chunks, "faq+llm"
    elif best_score >= THRESHOLD_LOW:
        return chunks, "partial+llm"
    else:
        return [], "none"



