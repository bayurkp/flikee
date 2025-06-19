import os
from pathlib import Path
import shutil
import ffmpeg
from typing import List

import requests
from app.models.video import Video
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def _select_videos(
    videos: List[Video],
    duration: float
):
    selected = []
    total_duration = 0.0
    for video in videos:
        if total_duration + video.duration <= duration:
            selected.append(video)
            total_duration += video.duration
        else:
            break

    if total_duration < duration:
        remaining_videos = [v for v in videos if v not in selected]
        if remaining_videos:
            selected.append(remaining_videos[0])
            total_duration += remaining_videos[0].duration

    return selected


def _download_videos(
    videos: List[Video],
    output_dir: str
) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    downloaded_paths = []

    for i, video in enumerate(videos):
        file_name = f"{i}.mp4"
        file_path = os.path.join(output_dir, file_name)

        try:
            response = requests.get(str(video.url), stream=True, timeout=30)
            response.raise_for_status()

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            downloaded_paths.append(file_path)
        except Exception as e:
            logger.error(f"Failed to download video {video.url}: {e}")

    return downloaded_paths


def _reencode_videos(
    video_paths: List[str],
    output_dir: str,
    target_resolution=(1280, 720),
    target_fps=30
) -> List[str]:
    output_dir = Path(output_dir)
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    final_paths = []
    for i, video_path in enumerate(video_paths):
        temp_output = temp_dir / f"temp_{i}.mp4"
        final_output = output_dir / f"{i}.mp4"

        vf = (
            f"scale=w={target_resolution[0]}:h={target_resolution[1]}:force_original_aspect_ratio=decrease,"
            f"pad={target_resolution[0]}:{target_resolution[1]}:(ow-iw)/2:(oh-ih)/2:color=black"
        )

        (
            ffmpeg
            .input(video_path)
            .output(
                str(temp_output),
                vf=vf,
                r=target_fps,
                vcodec='libx264',
                acodec='aac',
                strict='experimental'
            )
            .overwrite_output()
            .run()
        )

        shutil.move(str(temp_output), str(final_output))
        final_paths.append(str(final_output))

    try:
        temp_dir.rmdir()  # only deletes if empty
    except OSError:
        pass  # if not empty or fails, just ignore

    return final_paths


def _concatenate_videos(
    video_paths: List[str],
    output_dir: str
):
    list_file = os.path.join(output_dir, "list.txt")

    with open(list_file, "w") as f:
        for path in video_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")

    (
        ffmpeg
        .input(list_file, format='concat', safe=0)
        .output(os.path.join(output_dir, "output.mp4"), c='copy')
        .overwrite_output()
        .run()
    )

    os.remove(list_file)

    return os.path.join(output_dir, "output.mp4")


def _burn_voiceover(
    video_path: str,
    voiceover_path: str
) -> str:
    video_path = Path(video_path)
    temp_output = video_path.with_name(f"temp_{video_path.name}")

    video_in = ffmpeg.input(str(video_path))
    audio_in = ffmpeg.input(str(voiceover_path))

    (
        ffmpeg
        .output(video_in.video, audio_in.audio, str(temp_output),
                vcodec='copy', acodec='aac', shortest=None)
        .overwrite_output()
        .run()
    )

    video_path.unlink()
    temp_output.rename(video_path)

    return str(video_path)


def _burn_subtitle(video_path: str, subtitle_path: str) -> str:
    ext = Path(subtitle_path).suffix.lower()

    if ext == ".srt":
        filter_args = {"vf": f"subtitles='{subtitle_path}'"}
    elif ext == ".ass":
        filter_args = {"vf": f"ass='{subtitle_path}'"}
    else:
        raise ValueError(
            "Unsupported subtitle format. Only .srt and .ass are supported.")

    temp_output = str(Path(video_path).with_name("temp_burned.mp4"))

    (
        ffmpeg
        .input(video_path)
        .output(temp_output, **filter_args)
        .overwrite_output()
        .run()
    )

    Path(video_path).unlink()
    Path(temp_output).rename(video_path)

    return video_path


def process_video(
    videos: List[Video],
    output_dir: str,
    voiceover_path: str,
    subtitle_path: str,
    duration: float
):
    selected_videos = _select_videos(videos, duration)
    downloaded_paths = _download_videos(selected_videos, output_dir)
    reencoded_paths = _reencode_videos(downloaded_paths, output_dir)
    concatenated_path = _concatenate_videos(reencoded_paths, output_dir)
    voiceovered_path = _burn_voiceover(concatenated_path, voiceover_path)
    output_path = _burn_subtitle(voiceovered_path, subtitle_path)

    return output_path, reencoded_paths
