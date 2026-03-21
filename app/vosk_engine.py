import json
from vosk import Model, KaldiRecognizer
import wave
from app.config import MODEL_PATH

# Load model once
model = Model(MODEL_PATH)


def recognize_audio(wav_path):
    with wave.open(wav_path, "rb") as wf:
        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            recognizer.AcceptWaveform(data)

        final_result = json.loads(recognizer.FinalResult())

    text = final_result.get("text", "")
    words = final_result.get("result", [])

    # filter low confidence noise
    filtered_words = [w for w in words if w.get("conf", 0) > 0.3]

    if filtered_words:
        avg_conf = sum(w["conf"] for w in filtered_words) / len(filtered_words)
    else:
        avg_conf = 0.0

    return {
        "text": text,
        "confidence": round(avg_conf, 2),
        "words": filtered_words
    }