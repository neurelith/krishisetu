"""Multilingual MP3 advisory generation."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


AUDIO_DIR = Path(__file__).resolve().parent.parent / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

GTTS_LANG = {
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Marathi": "mr",
    "English": "en",
    "Punjabi": "pa",
}


class AudioService:
    """Creates downloadable MP3 files using gTTS when available."""

    def generate(self, text: str, language: str, grower_id: Optional[str]) -> Optional[str]:
        if not text:
            return None
        try:
            from gtts import gTTS
        except Exception:
            return None

        safe_id = re.sub(r"[^a-zA-Z0-9_-]+", "_", grower_id or "demo").strip("_") or "demo"
        filename = f"{safe_id}_{language.lower()}.mp3"
        path = AUDIO_DIR / filename
        try:
            tts = gTTS(text=text, lang=GTTS_LANG.get(language, "hi"), slow=False)
            tts.save(str(path))
            return f"/audio/{filename}"
        except Exception:
            return None
