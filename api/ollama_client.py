from ollama import Client
from typing import List, Dict
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")

client = Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")

def ask_ollama(messages: List[Dict[str, str]]) -> str:
    response = client.chat(model="gemma:2b", messages=messages)
    return response["message"]["content"]
