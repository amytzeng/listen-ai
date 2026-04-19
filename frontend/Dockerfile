# frontend/Dockerfile
# Build a lightweight image for the Streamlit dashboard.

FROM python:3.13-slim

# Avoid Python writing .pyc files and ensure logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to maximize Docker layer cache reuse.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code.
COPY . /app

# Streamlit default port used in Taskfile is 8501.
EXPOSE 8501

# Provide a reasonable default. In Docker Compose, you will override this
# to use the gateway service name, e.g. http://gateway:8000.
ENV GATEWAY_URL=http://localhost:8000

# Run Streamlit and listen on all interfaces inside the container.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]