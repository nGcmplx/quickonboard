from fastapi import FastAPI, Query
from contextlib import asynccontextmanager

from api.ollama_client import ask_ollama, warm_up_ollama
from api.prompt_utils import build_prompt
from api.logger import init_db, insert_log, get_logs
from api.memory_cache import get_session_history, append_to_session
from api.api_models import ChatRequest
from api.chroma_utils import retrieve_relevant_chunks
from api.embedding_loader import initialize_chroma


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_db()

    print("Initializing Chroma...")
    initialize_chroma()

    print("Warming up Ollama...")
    warm_up_ollama()

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/chat")
def chat(req: ChatRequest):
    session_id = req.session_id or "anon"
    prompt = req.prompt

    # Redis memory
    history = get_session_history(session_id)

    # Retrieve chunks
    retrieved_chunks, source = retrieve_relevant_chunks(prompt)
    print("Injected Context:", [c[:50] + "..." for c in retrieved_chunks])
    print("RAG Source:", source)

    # Limit to 1 chunk
    context_text = next(iter(retrieved_chunks), "")

    # LLM messages
    messages = build_prompt(history, prompt, context=context_text)
    response = ask_ollama(messages)

    # Memory + Logs
    append_to_session(session_id, prompt, response)
    insert_log(session_id, prompt if req.log else "REDACTED", response if req.log else "REDACTED")

    return {
        "session_id": session_id,
        "prompt": prompt,
        "response": response,
        "source": source
    }


@app.get("/logs")
def logs(limit: int = Query(100, gt=0, le=10000)):
    return get_logs(limit)


@app.get("/memory/{session_id}")
def memory(session_id: str):
    return get_session_history(session_id)


@app.get("/health")
def health():
    return {"status": "ok"}
