FROM python:3.11-slim

WORKDIR /code

COPY api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy the entire project root (assuming root contains api/)
COPY . /code/

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
