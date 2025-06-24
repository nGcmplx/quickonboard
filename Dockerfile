FROM python:3.11-slim

WORKDIR /code

COPY api/requirements.txt .

# Install torch CPU-only first to avoid CUDA downloads
RUN pip install --no-cache-dir torch==2.1.2+cpu --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
