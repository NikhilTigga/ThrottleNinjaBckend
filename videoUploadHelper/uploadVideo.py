import os
import tempfile
import subprocess

from dotenv import load_dotenv
from imageKit.imagekit_config import imagekit

load_dotenv()

FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")


def upload_feed_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        for chunk in video_file.chunks():
            temp_video.write(chunk)

    input_path = temp_video.name
    output_path = input_path.replace(".mp4", "_compressed.mp4")
    thumbnail_path = input_path.replace(".mp4", "_thumbnail.jpg")

    try:
        # Compress Video
        subprocess.run(
            [
                FFMPEG_PATH,
                "-i",
                input_path,
                "-vf",
                "scale='min(720,iw)':-2",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "28",
                "-movflags",
                "+faststart",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                output_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Generate Thumbnail
        subprocess.run(
            [
                FFMPEG_PATH,
                "-i",
                input_path,
                "-ss",
                "00:00:01",
                "-vframes",
                "1",
                thumbnail_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Upload Video to ImageKit
        with open(output_path, "rb") as video_file_obj:
            video_upload = imagekit.files.upload(
                file=video_file_obj,
                file_name=os.path.basename(output_path),
                use_unique_file_name=True,
                folder="/feeds/videos"
            )

        video_url = video_upload.url

        # Upload Thumbnail to ImageKit
        thumbnail_url = None

        if os.path.exists(thumbnail_path):
            with open(thumbnail_path, "rb") as thumb_file_obj:
                thumbnail_upload = imagekit.files.upload(
                    file=thumb_file_obj,
                    file_name=os.path.basename(thumbnail_path),
                    use_unique_file_name=True,
                    folder="/feeds/thumbnails"
                )

            thumbnail_url = thumbnail_upload.url
            thumbnail_file_id = thumbnail_upload.file_id

        return {
            "video_url": video_url,
            "thumbnail_url": thumbnail_url,
            "video_file_id": video_upload.file_id,
            "thumbnail_file_id": thumbnail_file_id,
        }

    except subprocess.CalledProcessError as e:
        print("FFmpeg Error:")
        print(e.stderr)
        raise

    except Exception as e:
        print("ImageKit Upload Error:")
        print(str(e))
        raise

    finally:
        for file_path in [input_path, output_path, thumbnail_path]:
            if os.path.exists(file_path):
                os.remove(file_path)