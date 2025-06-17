# QuickOnboard – AI-Powered Internal HR Assistant

**QuickOnboard** is a modular, containerized, API-first chatbot that helps employees quickly find answers to HR and onboarding questions. It blends predefined structured knowledge with local LLMs for flexible, secure, and contextual support — running fully offline.

---

## Core Features

### 1. RAG + LLM Fusion

- Queries are first matched against a curated **FAQ dataset** (JSON or CSV).
- If no good match is found, a fallback query is sent to a local **Ollama LLM** (Mistral, Phi-3, etc).
- Combines stability of known answers with generative flexibility.

### 2. Contextual Memory (via Redis or SQLite)

- Session-based Q&A memory is stored in a lightweight in-memory database.
- This allows the LLM to understand previous messages and follow-ups.
- Future support for persistent memory (e.g., Redis volume or SQLite file).

### 3. API-First Microservice Design

- Core chatbot logic is served via a FastAPI `/chat` endpoint.
- Designed to plug into Slack, web dashboards, or internal HR tools.
- Easily extendable into a multi-channel chatbot.

### 4. Query Logging

- Each chat is logged with timestamp, session ID, response source (FAQ or LLM), and raw text.
- Supports analytics, feedback loops, and error tracing.

### 5. Vector Search with ChromaDB

- Embeds HR docs and FAQs using sentence-transformers or Ollama embeddings.
- Uses **ChromaDB** or **FAISS** to retrieve top-n most relevant chunks.
- Improves accuracy and recall for ambiguous questions.

### 6. Docker-Based Microservices

All components are split into microservices:

- `api-service`: FastAPI interface
- `ollama-service`: Local LLM inference engine
- `vector-db`: Chroma or FAISS container
- `session-store`: Redis (or SQLite as fallback)

Managed via `docker-compose` for seamless local setup.

---

## Tech Stack

| Component    | Tech                          |
| ------------ | ----------------------------- |
| API Layer    | FastAPI                       |
| LLM Engine   | Ollama (Mistral, Phi-3, etc)  |
| Retrieval    | JSON FAQ + Vector DB (Chroma) |
| Memory Store | Redis or SQLite               |
| Deployment   | Docker + Docker Compose       |

---

## Architecture Components

| Service          | Description                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `api-service`    | FastAPI app that handles `/chat` endpoint, performs FAQ lookup and RAG      |
| `ollama-service` | Local LLM engine (Mistral, Phi-3, etc.) served via Ollama                   |
| `vector-db`      | Vector database (ChromaDB or FAISS) for semantic document similarity search |
| `session-store`  | In-memory store (Redis or SQLite) to track conversation context             |
| `logger`         | Logs all user interactions for audit, analytics, and improvement            |


---

## Example Usage

**Request:**

```json
POST /chat
{
  "session_id": "abc123",
  "question": "How do I reset my password?"
}
```

**Response:**

```json
{
  "response": "You can reset your password via the internal HR portal under Account Settings.",
  "source": "faq"
}
```

---

<!-- ## Author

**Faris Muhović**  
Building AI & web systems with real-world value. -->

<!-- Portfolio: https://farismuhovic.com (coming soon) -->
