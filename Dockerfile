FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 🔥 Install Python deps FIRST (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 Download model BEFORE app (cache)
RUN mkdir -p models temp

RUN wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip \
    && unzip vosk-model-small-en-us-0.15.zip -d models \
    && mv models/vosk-model-small-en-us-0.15 models/vosk-model-en-us \
    && rm vosk-model-small-en-us-0.15.zip

# 🔥 Copy app LAST (changes frequently)
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]