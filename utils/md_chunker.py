import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SOURCE_DIR = os.path.join(PROJECT_ROOT, "hr_policies")
OUTPUT_JSON = os.path.join(SOURCE_DIR, "hr_chunks.json")


def clean_markdown(text):
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)  # Remove [link](url)
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text)  # Remove backticks
    text = re.sub(r"#+ ", "", text)  # Remove headers
    return text.strip()


def chunk_text(text, max_words=100):
    paragraphs = text.split("\n\n")
    chunks = []
    buffer = ""
    for p in paragraphs:
        if len((buffer + p).split()) < max_words:
            buffer += " " + p
        else:
            chunks.append(buffer.strip())
            buffer = p
    if buffer:
        chunks.append(buffer.strip())
    return chunks


def load_markdown_files(folder):
    chunks = []
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                raw = f.read()
                text = clean_markdown(raw)
                subchunks = chunk_text(text)
                for chunk in subchunks:
                    chunks.append({
                        "source": filename,
                        "content": chunk
                    })
    return chunks


if __name__ == "__main__":
    docs = load_markdown_files(SOURCE_DIR)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
        json.dump(docs, out, indent=2)
    print(f"Saved {len(docs)} chunks to {OUTPUT_JSON}")
