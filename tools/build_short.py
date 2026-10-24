#!/usr/bin/env python3
"""build_short.py - Assemble 9:16 vertical Short video (1080x1920) with timed scenes and burned subtitles.

Usage:
    .venv/bin/python tools/build_short.py \
        --scenes-dir output/scenes/short-01 \
        --audio output/short-01-tara.m4a \
        --subtitles output/short-01-tara.srt \
        --output output/short-01-tara.mp4
"""

import argparse
import os
import subprocess
import sys

SHORT_SCHEDULE = [
    ("short-scene-1.png", 7.92),
    ("short-scene-2.png", 10.60),
    ("short-scene-3.png", 11.95),
    ("short-scene-4.png", 6.50),
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

def build_short(scenes_dir: str, audio_path: str, srt_path: str, output_path: str):
    ffmpeg_bin = check_ffmpeg()
    if not ffmpeg_bin:
        print("❌ Error: ffmpeg not found.")
        sys.exit(1)

    concat_file = "output/short_concat.txt"
    lines = []
    for filename, dur in SHORT_SCHEDULE:
        full_path = os.path.abspath(os.path.join(scenes_dir, filename))
        lines.append(f"file '{full_path}'")
        lines.append(f"duration {dur:.2f}")

    # Concat demuxer last frame requirement
    last_file = os.path.abspath(os.path.join(scenes_dir, SHORT_SCHEDULE[-1][0]))
    lines.append(f"file '{last_file}'")

    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    escaped_srt = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")
    # Vertical Shorts subtitle styling: centered, high-contrast, prominent
    style = "FontSize=26,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=4,Outline=2,Shadow=0,Alignment=2,MarginV=320"

    cmd = [
        ffmpeg_bin, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-i", audio_path,
        "-vf", f"fps=25,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,subtitles='{escaped_srt}':force_style='{style}'",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path
    ]

    print("🚀 Encoding 9:16 Vertical Short with FFmpeg...")
    res = subprocess.run(cmd)

    if res.returncode != 0:
        print("❌ FFmpeg encoding failed.")
        sys.exit(res.returncode)

    print(f"✅ Vertical Short created successfully: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Assemble 9:16 vertical Short")
    parser.add_argument("--scenes-dir", default="output/scenes/short-01", help="Scenes directory")
    parser.add_argument("--audio", default="output/short-01-tara.m4a", help="Audio path")
    parser.add_argument("--subtitles", default="output/short-01-tara.srt", help="Subtitles SRT path")
    parser.add_argument("--output", default="output/short-01-tara.mp4", help="Output MP4 path")
    args = parser.parse_args()

    build_short(args.scenes_dir, args.audio, args.subtitles, args.output)

if __name__ == "__main__":
    main()
