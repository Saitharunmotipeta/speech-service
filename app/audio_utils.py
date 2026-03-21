import subprocess
import uuid
import os
import shutil
from app.config import TEMP_DIR

# 🔥 cross-platform ffmpeg (works in Docker + local)
FFMPEG_PATH = shutil.which("ffmpeg") or "ffmpeg"


def save_temp_file(upload_file):
    file_id = str(uuid.uuid4())

    input_path = os.path.join(TEMP_DIR, f"{file_id}.input")

    with open(input_path, "wb") as f:
        f.write(upload_file.file.read())

    if os.path.getsize(input_path) == 0:
        raise Exception("Empty audio file received")

    return input_path, file_id


def convert_to_wav(input_path, file_id):
    output_path = os.path.join(TEMP_DIR, f"{file_id}.wav")

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", input_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_path
    ]

    result = subprocess.run(command, timeout=10)

    if result.returncode != 0:
        raise Exception("FFmpeg conversion failed")

    if not os.path.exists(output_path):
        raise Exception("WAV file not created")

    return output_path


def cleanup_files(*paths):
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass