# QuickOnboard – AI-Powered Internal HR Assistant

**QuickOnboard** is a modular, containerized, API-first chatbot that helps employees quickly find answers to HR and onboarding questions. It blends predefined structured knowledge with local LLMs for flexible, secure, and contextual support - running fully offline.

---

## Core Features

### 1. RAG + LLM Fusion

- Matches incoming queries against a curated **FAQ dataset**.
- If no relevant match is found, it sends the query to a **local LLM via Ollama** (`phi:2.7b`).
- Hybrid responses are returned from either `"faq"`, `"faq+llm"`, or `"llm"` source.

### 2. Contextual Session Memory

- Uses **Redis** (or in-memory fallback) to store Q\&A per session.
- Enables follow-up understanding and smoother conversation history.
- Accessed via `/memory/{session_id}`.

### 3. Restful API-First Microservice Design

- Exposes `/chat`, `/logs`, `/memory/{session_id}`, and `/health` endpoints.
- Cleanly designed with FastAPI for easy integration with Slack, dashboards, etc.

### 4. Query Logging

- Every interaction logs: session ID, prompt, response, source, and timestamp.
- Optional logging toggle (`log: true | false`) for user privacy.
- Viewable at `/logs`.

### 5. Semantic Vector Retrieval

  - Chunks markdown or HR documents using **ChromaDB** + Ollama Embeddings.
  - Returns the top relevant context chunk to the LLM.
  - Helpful for ambiguous queries or edge cases.
  - frontend (Streamlit chat interface)

### 6. Fully Containerized Deployment

- Built with **Docker Compose** for local development and testing.
- Services:

  - **api-service** (FastAPI)
  - **ollama-service** (local LLM via Ollama)
  - **db** (PostgreSQL)
  - **redis** (session memory)
  - **chroma** (vector search)
  - **streamlit-frontend** (Streamlit chat interface)

---

## Tech Stack

| Layer        | Technology              |
| ------------ | ----------------------- |
| Frontend UI  | Streamlit                 |
| Backend API  | FastAPI                 |
| Local LLM    | Ollama (`phi:2.7b`)     |
| Vector DB    | ChromaDB                |
| Memory Store | Redis                   |
| Embeddings   | sentence-transformers   |
| Deployment   | Docker & Docker Compose |

---

## API Endpoints

### `POST /chat`

Handles prompt routing: checks Redis memory, performs RAG with Chroma, queries Ollama if needed.

```json
{
  "session_id": "faris",
  "prompt": "What should I expect during my first week?",
  "log": true
}
```

Response:

```json
{
  "response": "You’ll get access to a welcome project in Basecamp, meet your manager and buddy, and begin your onboarding tasks.",
  "source": "faq+llm"
}
```

---

### `GET /logs`

Returns last 100 (default) chat logs.

### `GET /memory/{session_id}`

Returns conversation history.

### `GET /health`

Returns `{ "status": "ok" }` if app is ready (used for Docker healthcheck).

---

## Run Locally

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the Repo

```bash
git clone https://github.com/nGcmplx/quickonboard.git
cd quickonboard
```

### 2. Start All Services

```bash
docker-compose up --build
```

This spins up:

* `api-service`: FastAPI backend on [http://localhost:80](http://localhost:80)
* `ollama`: local LLM server (`phi:2.7b`)
* `redis`: for session memory
* `postgres`: for logging
* `chroma`: for vector search (HR docs)
* `frontend`: for frontend UI

### 3. Test the API

You can send a test chat using `curl` or Postman:

```bash
curl -X POST http://localhost/chat \
  -H "Content-Type: application/json" \
  -d '{
        "session_id": "demo",
        "prompt": "What’s my first week like?",
        "log": true
      }'
```

You should get a hybrid LLM + FAQ response if everything is wired correctly.