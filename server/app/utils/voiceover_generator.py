from pathlib import Path
import re
from pydub import AudioSegment
from num2words import num2words
from g2p_id import G2P
from TTS.api import TTS
from app.utils.constant import (
    TTS_MODEL_PATH,
    TTS_CONFIG_PATH,
    TTS_SPEAKERS_PATH,
)

SYMBOL_MAP = {
    " + ": " plus ",
    " - ": " minus ",
    " / ": " bagi ",
    " × ": " kali ",
    " = ": " sama dengan "
}

DEFAULT_SPEAKER = "wibowo"


def _preprocess_text(text: str) -> str:
    for symbol, word in SYMBOL_MAP.items():
        text = text.replace(symbol, word)

    # Replace digits with words in Indonesian
    text = re.sub(r'\d+', lambda m: num2words(int(m.group()), lang="id"), text)

    # Convert text to phonetics using G2P
    phonetic_text = G2P()(text)
    return phonetic_text


def _coqui(text: str, output_path: str) -> str:
    tts = TTS(config_path=TTS_CONFIG_PATH, model_path=TTS_MODEL_PATH,
              speakers_file_path=TTS_SPEAKERS_PATH)
    tts.tts_to_file(text=text, file_path=output_path,
                    speaker=DEFAULT_SPEAKER)


def generate_voiceover(text: str, output_dir: str) -> tuple[str, float]:
    processed_text = _preprocess_text(text)
    output_dir_path = Path(output_dir)
    output_path = output_dir_path / "voiceover.wav"

    _coqui(processed_text, output_path)

    audio = AudioSegment.from_file(output_path)
    duration = len(audio) / 1000  # in seconds

    return str(output_path), duration
