from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = BASE_DIR / "app"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE_PATH = LOG_DIR / "app.log"

TTS_MODEL_PATH = BASE_DIR / "tts/model.pth"
TTS_CONFIG_PATH = BASE_DIR / "tts/config.json"
TTS_SPEAKERS_PATH = BASE_DIR / "tts/speakers.pth"

STORAGE_DIR = BASE_DIR / "storage"
