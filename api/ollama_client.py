from ollama import Client
from typing import List, Dict
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")

client = Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")

def ask_ollama(
        messages: List[Dict[str, str]],
        model: str = "phi:2.7b",
        options: Dict = {
            "temperature": 0.2,
            "num_predict": 256,
            "top_k": 30,
            "top_p": 0.9
        }
) -> str:
    response = client.chat(
        model=model,
        messages=messages,
        options=options
    )

    content = response["message"]["content"]
    return content


def warm_up_ollama(model: str = "phi:2.7b"):
    try:
        print("Warming up Ollama model...")
        _ = client.generate(model=model, prompt="hello")
        print("Ollama model is ready.")
    except Exception as e:
        print("Failed to warm up Ollama:", str(e))
