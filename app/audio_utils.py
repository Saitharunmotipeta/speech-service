import subprocess
import uuid
import os
import shutil
from app.config import TEMP_DIR

# -------------------------
# FFMPEG PATH (cross-platform)
# -------------------------
FFMPEG_PATH = shutil.which("ffmpeg") or "ffmpeg"

# ensure temp dir exists
os.makedirs(TEMP_DIR, exist_ok=True)


# -------------------------
# VALIDATION
# -------------------------
def is_supported_audio(filename: str):
    allowed = [".wav", ".mp3", ".webm", ".ogg", ".m4a"]
    return any(filename.lower().endswith(ext) for ext in allowed)


# -------------------------
# SAVE FILE (STREAM SAFE)
# -------------------------
def save_temp_file(upload_file):
    file_id = str(uuid.uuid4())

    input_path = os.path.join(TEMP_DIR, f"{file_id}.input")

    # stream-safe write (important for large files)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

    # validation
    if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
        raise Exception("Empty audio file received")

    return input_path, file_id


# -------------------------
# CONVERT TO WAV (VOSK READY)
# -------------------------
def convert_to_wav(input_path, file_id):
    if not input_path:
        raise Exception("Invalid input file")

    output_path = os.path.join(TEMP_DIR, f"{file_id}.wav")

    command = [
        FFMPEG_PATH,
        "-y",
        "-loglevel", "error",   # clean logs
        "-i", input_path,
        "-vn",
        "-acodec", "pcm_s16le",  # required for vosk
        "-ar", "16000",          # 16kHz
        "-ac", "1",              # mono
        output_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30
    )

    if result.returncode != 0:
        print("FFMPEG ERROR:", result.stderr.decode())
        raise Exception("FFmpeg conversion failed")

    if not os.path.exists(output_path):
        raise Exception("WAV file not created")

    return output_path


# -------------------------
# CLEANUP (SAFE)
# -------------------------
def cleanup_files(*paths):
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print("Cleanup failed:", e)