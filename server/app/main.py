from fastapi import FastAPI
from app.utils.logger import setup_logger
from app.utils.tts import generate_speech
from app.utils.stt import transcribe_speech
from app.utils.keywords_extractor import extract_keywords
from app.utils.constant import STORAGE_DIR
from app.utils.videos_curator import curate_videos
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

logger = setup_logger(__name__)
app = FastAPI()


@app.get("/generate")
def generate_video():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = STORAGE_DIR / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / "output.wav"
    subtitle_path = output_dir / "output.srt"

    # Video Script
    text = (
        "Pedesaan adalah tempat yang identik dengan suasana tenang, "
        "udara segar, dan pemandangan alam yang asri. "
        "Di sana, kehidupan berjalan lebih lambat dibandingkan di kota, "
        "dengan penduduk yang ramah dan saling mengenal satu sama lain. "
        "Sawah yang hijau, suara burung di pagi hari, serta aroma tanah "
        "setelah hujan menjadi bagian dari keseharian yang menenangkan. "
        "Pedesaan juga sering dijadikan tempat untuk melepas penat dan "
        "mencari inspirasi karena kedekatannya dengan alam. "
        "Kehidupan sederhana namun penuh makna menjadi ciri khas dari "
        "suasana pedesaan."
    )

    # Generate audio dan subtitle
    # generate_speech(text, str(audio_path))
    # transcribe_speech(str(audio_path), str(output_dir))

    # Extract keywords
    # keywords = extract_keywords(text)

    # Curate videos
    videos = curate_videos(['Tranquil countryside', 'lush rice paddies'])

    return {
        "message": "TTS dan subtitle berhasil dibuat.",
        "audio_file": str(audio_path),
        "subtitle_file": str(subtitle_path),
        # "keywords": keywords,
        "videos": videos
    }
