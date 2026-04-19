# nlp/Dockerfile
# Containerize the FastAPI-based NLP sentiment service.

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code.
COPY . /app

# Default NLP port from Taskfile is 8001.
EXPOSE 8001

# Keep the port configurable to match local/dev/prod needs.
ENV NLP_PORT=8001

# Start FastAPI with Uvicorn, listening on all interfaces in the container.
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${NLP_PORT}"]