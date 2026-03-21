FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (FFmpeg + tools)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create required directories
RUN mkdir -p models temp

# Download Vosk model (small, fast)
RUN wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip \
    && unzip vosk-model-small-en-us-0.15.zip -d models \
    && mv models/vosk-model-small-en-us-0.15 models/vosk-model-en-us \
    && rm vosk-model-small-en-us-0.15.zip

# Copy application code
COPY app ./app

# Expose port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]