import os
import subprocess


def run_ffmpeg(command):
    """
    Execute an FFmpeg command.

    Args:
        command (list): FFmpeg command as a list.

    Raises:
        RuntimeError: If FFmpeg execution fails.
    """
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"FFmpeg Error:\n{e.stderr.decode()}"
        )


def transcode_video(input_file, output_directory):
    """
    Generate 720p, 480p videos and a thumbnail.

    Args:
        input_file (str): Path to uploaded video.
        output_directory (str): Directory for output files.

    Returns:
        dict
    """

    os.makedirs(output_directory, exist_ok=True)

    filename = os.path.splitext(os.path.basename(input_file))[0]

    output_720 = os.path.join(output_directory, f"{filename}_720p.mp4")
    output_480 = os.path.join(output_directory, f"{filename}_480p.mp4")
    thumbnail = os.path.join(output_directory, f"{filename}_thumbnail.jpg")

    # 720p
    command_720 = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vf", "scale=-2:720",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        output_720
    ]

    # 480p
    command_480 = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vf", "scale=-2:480",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        output_480
    ]

    # Thumbnail at 5 seconds
    thumbnail_command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-ss", "00:00:05",
        "-frames:v", "1",
        thumbnail
    ]

    run_ffmpeg(command_720)
    run_ffmpeg(command_480)
    run_ffmpeg(thumbnail_command)

    return {
        "720p": output_720,
        "480p": output_480,
        "thumbnail": thumbnail
    }