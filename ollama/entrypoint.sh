#!/bin/sh

# Start Ollama server in background
ollama serve &

# Capture PID
SERVER_PID=$!

# Wait a bit for server to start
sleep 5

# Pull the model
ollama pull gemma:2b

# Wait for the server process (keep container alive)
wait "$SERVER_PID"
