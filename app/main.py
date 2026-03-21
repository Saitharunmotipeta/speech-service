from fastapi import FastAPI, UploadFile, File, HTTPException
from app.audio_utils import save_temp_file, convert_to_wav, cleanup_files
from app.vosk_engine import recognize_audio

app = FastAPI()


@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    input_path = None
    wav_path = None

    try:
        input_path, file_id = save_temp_file(file)
        wav_path = convert_to_wav(input_path, file_id)

        result = recognize_audio(wav_path)

        if result["text"] == "":
            return {
                "recognized_text": "",
                "confidence": 0,
                "message": "No speech detected"
            }

        return {
            "recognized_text": result["text"],
            "confidence": result["confidence"],
            "words": result["words"]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cleanup_files(input_path, wav_path)