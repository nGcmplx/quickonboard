import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CHROMA_DIR = "/code/chroma_db"
THRESHOLD_HIGH = 0.75
THRESHOLD_LOW = 0.4

embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.Client(chromadb.config.Settings(persist_directory=CHROMA_DIR))
collection = None  # Lazy-loaded global collection


def get_collection():
    global collection
    if collection is None:
        collection = client.get_collection("hr_docs")
        collection._embedding_function = embedding_func
    return collection


def truncate(text: str, max_len: int = 50) -> str:
    return text if len(text) <= max_len else text[:max_len - 3] + "..."


def retrieve_relevant_chunks(query: str) -> tuple[list[str], str]:
    col = get_collection()

    print(f"Querying Chroma with: {truncate(query)}")
    print(f"Chroma dir: {CHROMA_DIR}")
    print(f"Collections: {[c.name for c in client.list_collections()]}")
    print(f"Collection count: {col.count()}")

    results = col.query(
        query_texts=[query],
        n_results=3,
        include=["documents", "distances"]
    )

    if not results["documents"] or not results["documents"][0]:
        print("No relevant documents found.")
        return [], "none"

    chunks = results["documents"][0]
    scores = results["distances"][0]

    print("Retrieved Chunks:")
    for i, chunk in enumerate(chunks):
        print(f"  {i + 1}. {truncate(chunk)}")

    print(f"Scores: {scores}")

    best_score = scores[0] if scores else 0

    if best_score >= THRESHOLD_HIGH:
        return chunks, "faq+llm"
    elif best_score >= THRESHOLD_LOW:
        return chunks, "partial+llm"
    else:
        return [], "none"
