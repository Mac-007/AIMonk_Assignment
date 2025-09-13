# AI_Backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (needed for torch + pillow)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY ai_backend.py /app/ai_backend.py

# Create output folders
RUN mkdir -p /app/outputs/images /app/outputs/json

EXPOSE 8000

CMD ["uvicorn", "ai_backend:app", "--host", "0.0.0.0", "--port", "8000"]
