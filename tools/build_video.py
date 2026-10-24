#!/usr/bin/env python3
"""build_video.py - Assemble faceless MP4 video from dynamic scenes, voiceover audio, and subtitles.

Supports:
1. Multi-scene dynamic cuts synchronized to script beats.
2. Single-image background loop.
3. Subtitle burning (SRT) and 1080p rendering via FFmpeg.

Usage:
    .venv/bin/python tools/build_video.py \
        --scenes-dir output/scenes \
        --audio output/video-01-voice.m4a \
        --subtitles output/video-01.srt \
        --output output/video-01.mp4
"""

import argparse
import os
import subprocess
import sys

DEFAULT_SCENE_SCHEDULE = [
    ("scene-1-hook.png", 5.37),
    ("scene-2-overview.png", 20.31),
    ("scene-3-title-linter.png", 41.10),
    ("scene-4-hook-scorer.png", 41.61),
    ("scene-5-dead-air.png", 27.76),
    ("scene-6-the-catch.png", 23.30),
    ("scene-7-github-repo.png", 15.00),
]

def check_ffmpeg():
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except ImportError:
        pass

    paths = ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "ffmpeg"]
    for p in paths:
        try:
            res = subprocess.run([p, "-version"], capture_output=True, text=True)
            if res.returncode == 0:
                return p
        except Exception:
            continue
    return None

def create_concat_file(scenes_dir: str, schedule, concat_file_path: str):
    lines = []
    for filename, duration in schedule:
        img_path = os.path.abspath(os.path.join(scenes_dir, filename))
        if not os.path.exists(img_path):
            print(f"Warning: Scene file not found: {img_path}")
            continue
        lines.append(f"file '{img_path}'")
        lines.append(f"duration {duration:.2f}")

    # FFmpeg concat requirement: repeat the last file without duration
    if schedule:
        last_file = os.path.abspath(os.path.join(scenes_dir, schedule[-1][0]))
        lines.append(f"file '{last_file}'")

    os.makedirs(os.path.dirname(concat_file_path), exist_ok=True)
    with open(concat_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✅ Created scene playlist: {concat_file_path} ({len(schedule)} scenes)")

def build_video(scenes_dir: str, image_path: str, audio_path: str, srt_path: str, output_path: str, burn_subtitles: bool = True):
    ffmpeg_bin = check_ffmpeg()
    if not ffmpeg_bin:
        print("❌ Error: ffmpeg not found. Ensure ffmpeg is installed.")
        sys.exit(1)

    if not os.path.exists(audio_path):
        print(f"❌ Error: Audio file not found: {audio_path}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    concat_file = "output/scenes_concat.txt"
    use_multi_scenes = False

    if scenes_dir and os.path.exists(scenes_dir):
        schedule = DEFAULT_SCENE_SCHEDULE
        schedule_file = os.path.join(scenes_dir, "scenes_schedule.json")
        if os.path.exists(schedule_file):
            import json
            with open(schedule_file, "r") as f:
                schedule = json.load(f)
        create_concat_file(scenes_dir, schedule, concat_file)
        use_multi_scenes = True

    cmd = [ffmpeg_bin, "-y"]

    if use_multi_scenes:
        cmd.extend([
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file
        ])
    else:
        if not os.path.exists(image_path):
            print(f"❌ Error: Image file not found: {image_path}")
            sys.exit(1)
        cmd.extend([
            "-loop", "1",
            "-i", image_path
        ])

    cmd.extend(["-i", audio_path])

    # Video filters (scaling to 1080p 1920x1080, standard 25fps and subtitle burning)
    vf_filters = ["fps=25", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"]

    if burn_subtitles and srt_path and os.path.exists(srt_path):
        escaped_srt = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")
        style = "FontSize=22,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=4,Outline=1,Shadow=0,Alignment=2,MarginV=45"
        vf_filters.append(f"subtitles='{escaped_srt}':force_style='{style}'")

    cmd.extend([
        "-vf", ",".join(vf_filters),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path
    ])

    print("🚀 Encoding video with dynamic scenes and subtitles...")
    print(f"Command: {' '.join(cmd)}")
    res = subprocess.run(cmd)

    if res.returncode != 0:
        print("❌ FFmpeg encoding failed.")
        sys.exit(res.returncode)

    print(f"✅ Video created successfully: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Assemble faceless MP4 video with dynamic scenes")
    parser.add_argument("--scenes-dir", default="output/scenes", help="Directory containing scene images")
    parser.add_argument("--image", default=None, help="Optional single background image fallback")
    parser.add_argument("--audio", default="output/video-01-voice.m4a", help="Path to voiceover audio")
    parser.add_argument("--subtitles", default="output/video-01.srt", help="Path to SRT subtitle file")
    parser.add_argument("--output", default="output/video-01.mp4", help="Output MP4 file path")
    parser.add_argument("--no-burn-subtitles", action="store_true", help="Do not burn subtitles into video")
    args = parser.parse_args()

    build_video(
        scenes_dir=args.scenes_dir,
        image_path=args.image,
        audio_path=args.audio,
        srt_path=args.subtitles,
        output_path=args.output,
        burn_subtitles=not args.no_burn_subtitles
    )

if __name__ == "__main__":
    main()
