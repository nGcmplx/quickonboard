FROM python:3.11-slim

WORKDIR /code

COPY api/requirements.txt .

# 🛠 Install curl + torch + Python deps
RUN apt-get update && apt-get install -y curl \
 && pip install --no-cache-dir torch==2.1.2+cpu --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
