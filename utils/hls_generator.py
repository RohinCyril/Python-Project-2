import os
import subprocess

from config import FFMPEG_BINARY


def generate_hls(input_video, output_directory):
    """
    Generate HLS playlist and video segments.

    Args:
        input_video (str): Path to the input MP4 video.
        output_directory (str): Directory where HLS files will be stored.

    Returns:
        str: Path to the generated playlist (.m3u8).
    """

    os.makedirs(output_directory, exist_ok=True)

    playlist_path = os.path.join(output_directory, "playlist.m3u8")
    segment_pattern = os.path.join(output_directory, "segment%03d.ts")

    command = [
        FFMPEG_BINARY,
        "-y",
        "-i", input_video,
        "-codec:", "copy",
        "-start_number", "0",
        "-hls_time", "10",
        "-hls_list_size", "0",
        "-hls_segment_filename", segment_pattern,
        "-f", "hls",
        playlist_path
    ]

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"HLS generation failed:\n{e.stderr}"
        )

    return playlist_path