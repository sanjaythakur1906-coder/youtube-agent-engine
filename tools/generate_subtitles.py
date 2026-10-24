#!/usr/bin/env python3
"""generate_subtitles.py - Generate synced SRT and VTT subtitles from script and audio duration.

Usage:
    .venv/bin/python tools/generate_subtitles.py docs/scripts/video-01-script.md --duration 171.78 --output-srt output/video-01.srt --output-vtt output/video-01.vtt
"""

import argparse
import os
import re
import subprocess
import sys

def get_audio_duration(audio_path: str) -> float:
    """Get audio duration using afinfo or ffprobe."""
    if not os.path.exists(audio_path):
        return 0.0

    # Try afinfo (macOS native)
    try:
        res = subprocess.run(["afinfo", audio_path], capture_output=True, text=True, check=True)
        for line in res.stdout.split("\n"):
            if "estimated duration:" in line:
                match = re.search(r"estimated duration:\s+([0-9.]+)", line)
                if match:
                    return float(match.group(1))
    except Exception:
        pass

    # Fallback to ffprobe if available
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True,
            text=True,
            check=True
        )
        return float(res.stdout.strip())
    except Exception:
        pass

    return 0.0

def extract_spoken_segments(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    spoken_segments = []
    is_spoken_block = False

    for line in lines:
        line_str = line.strip()
        if line_str.startswith("#") or line_str.startswith("---"):
            is_spoken_block = False
            continue
        if re.search(r"^\[\d+:\d+", line_str) or line_str.startswith("[ON SCREEN:"):
            is_spoken_block = False
            continue
        if line_str.startswith("**Spoken:**"):
            is_spoken_block = True
            continue
        if line_str.startswith("## ") or line_str.startswith("- **") or line_str.startswith("**Ship"):
            is_spoken_block = False
            continue

        if is_spoken_block and line_str:
            # Split into sentence-level chunks for subtitles
            sentences = re.split(r"(?<=[.!?])\s+", line_str)
            for s in sentences:
                s_clean = s.strip()
                if s_clean:
                    spoken_segments.append(s_clean)

    if not spoken_segments:
        cleaned = re.sub(r"\[ON SCREEN:[^\]]*\]", "", content)
        cleaned = re.sub(r"\[\d+:\d+[^\]]*\]", "", cleaned)
        cleaned = re.sub(r"#[^\n]*", "", cleaned)
        cleaned = re.sub(r"\*\*[^*]*\*\*", "", cleaned)
        for line in cleaned.split("\n"):
            line = line.strip()
            if line:
                sentences = re.split(r"(?<=[.!?])\s+", line)
                for s in sentences:
                    s_clean = s.strip()
                    if s_clean:
                        spoken_segments.append(s_clean)

    return spoken_segments

def format_timestamp_srt(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def format_timestamp_vtt(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{millis:03d}"

def generate_subtitles(segments, total_duration: float, srt_path: str, vtt_path: str):
    if not segments:
        print("No spoken segments found.")
        return

    # Total characters used for weighting
    total_chars = sum(max(len(s), 5) for s in segments)
    if total_chars == 0:
        return

    srt_lines = []
    vtt_lines = ["WEBVTT\n"]

    current_time = 0.5  # slight initial offset
    usable_duration = max(total_duration - 1.0, 1.0)

    for i, seg in enumerate(segments, 1):
        seg_len = max(len(seg), 5)
        # Allocate duration proportionally with small pause buffer
        duration = (seg_len / total_chars) * usable_duration
        duration = max(duration, 1.2)  # min 1.2s per subtitle
        end_time = min(current_time + duration, total_duration)

        # SRT format
        srt_lines.append(str(i))
        srt_lines.append(f"{format_timestamp_srt(current_time)} --> {format_timestamp_srt(end_time)}")
        srt_lines.append(seg)
        srt_lines.append("")

        # VTT format
        vtt_lines.append(str(i))
        vtt_lines.append(f"{format_timestamp_vtt(current_time)} --> {format_timestamp_vtt(end_time)}")
        vtt_lines.append(seg)
        vtt_lines.append("")

        current_time = end_time + 0.1
        if current_time >= total_duration:
            break

    if srt_path:
        os.makedirs(os.path.dirname(srt_path), exist_ok=True)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))
        print(f"✅ Generated SRT: {srt_path}")

    if vtt_path:
        os.makedirs(os.path.dirname(vtt_path), exist_ok=True)
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(vtt_lines))
        print(f"✅ Generated VTT: {vtt_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate SRT/VTT subtitles from script")
    parser.add_argument("script", help="Path to markdown script file")
    parser.add_argument("--audio", default="output/video-01-voice.m4a", help="Audio file path to detect duration")
    parser.add_argument("--duration", type=float, default=None, help="Explicit audio duration in seconds")
    parser.add_argument("--output-srt", default="output/video-01.srt", help="Output SRT file path")
    parser.add_argument("--output-vtt", default="output/video-01.vtt", help="Output VTT file path")
    args = parser.parse_args()

    duration = args.duration
    if duration is None:
        duration = get_audio_duration(args.audio)
        if duration <= 0:
            print("Could not auto-detect duration. Defaulting to 171.78s.")
            duration = 171.78
        else:
            print(f"Detected audio duration: {duration:.2f}s")

    segments = extract_spoken_segments(args.script)
    print(f"Extracted {len(segments)} subtitle segments.")
    generate_subtitles(segments, duration, args.output_srt, args.output_vtt)

if __name__ == "__main__":
    main()
