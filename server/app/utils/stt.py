import subprocess


def _whisper(
    audio_path: str,
    output_path: str,
    model: str = "turbo",
    output_format: str = "srt",
    language: str = "id"
) -> str:
    command = [
        "whisper",
        audio_path,
        "--model", model,
        "--output_dir", output_path,
        "--output_format", output_format,
        "--language", language,
        "--word_timestamps", "True",
        "--max_words_per_line", "7"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(result.stderr)

    return output_path


def transcribe_speech(audio_path: str, output_path: str) -> str:
    output_path = _whisper(audio_path, output_path)

    return output_path
