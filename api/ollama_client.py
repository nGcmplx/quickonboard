from ollama import Client
from typing import List, Dict
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")

client = Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")

def ask_ollama(messages: List[Dict[str, str]]) -> str:
    response = client.chat(
        model="phi:2.7b",
        messages=messages,
        options={"num_predict": 64, "temperature": 0.7}
    )
    return response["message"]["content"]


def warm_up_ollama():
    try:
        print("Warming up Ollama model...")
        _ = client.generate(model="phi:2.7b", prompt="hello")
        print("Ollama model is ready.")
    except Exception as e:
        print("Failed to warm up Ollama:", str(e))
