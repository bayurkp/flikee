import os
from pathlib import Path
from faster_whisper import WhisperModel
import ffmpeg
import pysubs2


def _export_srt(words, filename, max_words_per_line=7):
    def is_end_of_sentence(word):
        return word.strip().endswith((".", "!", "?"))

    def split_sentences(word_list):
        sentences = []
        current = []
        for word in word_list:
            current.append(word)
            if is_end_of_sentence(word[2]):
                sentences.append(current)
                current = []
        if current:
            sentences.append(current)
        return sentences

    def chunk_words(words, n):
        return [words[i:i + n] for i in range(0, len(words), n)]

    subs = pysubs2.SSAFile()
    sentences = split_sentences(words)

    for sentence in sentences:
        chunks = chunk_words(sentence, max_words_per_line)
        for chunk in chunks:
            start_time = int(chunk[0][0] * 1000)
            end_time = int(chunk[-1][1] * 1000)
            text = " ".join(w[2].strip() for w in chunk)
            event = pysubs2.SSAEvent(start=start_time, end=end_time, text=text)
            subs.append(event)

    subs.save(filename)


def _faster_whisper(
    voiceover_path: str,
        output_path: str,
        model: str = "tiny",
        text: str = "",
        language: str = "id"
) -> str:
    model = WhisperModel(model, device="cpu", compute_type="float32")
    segments, _ = model.transcribe(
        audio=voiceover_path,
        language=language,
        initial_prompt=text,
        word_timestamps=True
    )

    words = []
    for segment in segments:
        for word in segment.words:
            words.append((word.start, word.end, word.word))

    _export_srt(words, output_path)

    return output_path


def generate_subtitle(
    voiceover_path: str,
    text: str,
    output_dir: str
) -> str:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    srt_path = output_dir_path / "subtitle.srt"
    ass_path = output_dir_path / "subtitle.ass"

    _faster_whisper(voiceover_path, srt_path, text=text)

    (
        ffmpeg
        .input(str(srt_path))
        .output(str(ass_path))
        .overwrite_output()
        .run()
    )

    os.remove(srt_path)

    return str(ass_path)
