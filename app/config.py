import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    os.path.join(BASE_DIR, "models", "vosk-model-en-us")
)

TEMP_DIR = os.getenv(
    "TEMP_DIR",
    os.path.join(BASE_DIR, "temp")
)

os.makedirs(TEMP_DIR, exist_ok=True)