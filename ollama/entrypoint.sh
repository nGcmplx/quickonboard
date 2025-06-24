#!/bin/sh

# Start Ollama server in background
ollama serve &

# Capture PID
SERVER_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama on port 11434..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done

# Now pull the model
echo "Pulling model..."
ollama pull phi:2.7b

# Wait for server to stay alive
wait "$SERVER_PID"
