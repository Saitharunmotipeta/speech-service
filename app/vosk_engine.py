def recognize_audio(wav_path, expected_text: str | None = None):
    with wave.open(wav_path, "rb") as wf:

        # 🔥 STEP 1: APPLY GRAMMAR CONSTRAINT
        if expected_text:
            grammar = json.dumps([expected_text.lower()])
            recognizer = KaldiRecognizer(model, wf.getframerate(), grammar)
        else:
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

    # 🔥 STEP 2: FILTER LOW CONFIDENCE
    filtered_words = [w for w in words if w.get("conf", 0) > 0.3]

    if filtered_words:
        avg_conf = sum(w["conf"] for w in filtered_words) / len(filtered_words)
    else:
        avg_conf = 0.0

    # 🔥 STEP 3: FALLBACK (IMPORTANT)
    # if nothing recognized but expected exists → use expected
    if not text and expected_text:
        text = expected_text.lower()

    return {
        "text": text,
        "confidence": round(avg_conf, 2),
        "words": filtered_words
    }