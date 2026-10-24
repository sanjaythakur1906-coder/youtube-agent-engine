#!/usr/bin/env python3
"""generate_voice.py - Generate voiceover from a video script using macOS speech engine or Microsoft Neural TTS.

Supports:
1. Native macOS voice (`say` engine) - offline on Mac.
2. Microsoft Neural TTS (`edge-tts`) - cloud-ready, runs on Linux/Docker/Render with zero API keys.

Usage:
    .venv/bin/python tools/generate_voice.py docs/scripts/video-01-script.md --voice Aman --output output/test_aman.m4a
    .venv/bin/python tools/generate_voice.py docs/scripts/video-01-script.md --engine edge-tts --voice Prabhat --output output/test_cloud.mp3
"""

import argparse
import asyncio
import os
import platform
import re
import subprocess
import sys

# Mapping simple names to edge-tts neural voices
EDGE_VOICE_MAP = {
    "aman": "en-IN-PrabhatNeural",
    "prabhat": "en-IN-PrabhatNeural",
    "tara": "en-IN-NeerjaNeural",
    "neerja": "en-IN-NeerjaNeural",
    "rishi": "hi-IN-MadhurNeural",
    "madhur": "hi-IN-MadhurNeural",
    "swara": "hi-IN-SwaraNeural",
    "daniel": "en-GB-RyanNeural",
    "samantha": "en-US-JennyNeural",
}

def extract_spoken_blocks(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    spoken_lines = []
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
            spoken_lines.append(line_str)

    if not spoken_lines:
        cleaned = re.sub(r"\[ON SCREEN:[^\]]*\]", "", content)
        cleaned = re.sub(r"\[\d+:\d+[^\]]*\]", "", cleaned)
        cleaned = re.sub(r"#[^\n]*", "", cleaned)
        cleaned = re.sub(r"\*\*[^*]*\*\*", "", cleaned)
        spoken_lines = [l.strip() for l in cleaned.split("\n") if l.strip()]

    return spoken_lines

def generate_mac_voice(text_list, voice: str, output_path: str):
    full_text = "\n\n".join(text_list)
    temp_txt = "output/temp_script.txt"
    os.makedirs(os.path.dirname(temp_txt), exist_ok=True)
    with open(temp_txt, "w", encoding="utf-8") as f:
        f.write(full_text)

    cmd = ["say", "-v", voice, "-f", temp_txt, "-o", output_path]
    print(f"Running macOS speech engine ({voice})...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_txt):
        os.remove(temp_txt)

    if res.returncode != 0:
        print(f"Error running say: {res.stderr}")
        sys.exit(1)

    print(f"✅ Generated audio: {output_path}")

async def generate_edge_voice_async(text_list, voice_name: str, output_path: str):
    import edge_tts
    neural_voice = EDGE_VOICE_MAP.get(voice_name.lower(), voice_name)
    if not neural_voice.endswith("Neural"):
        neural_voice = "en-IN-PrabhatNeural"

    full_text = " ".join(text_list)
    print(f"Running Microsoft Neural TTS ({neural_voice})...")
    communicate = edge_tts.Communicate(full_text, neural_voice)
    await communicate.save(output_path)
    print(f"✅ Generated cloud neural audio: {output_path}")

def generate_edge_voice(text_list, voice_name: str, output_path: str):
    asyncio.run(generate_edge_voice_async(text_list, voice_name, output_path))

def main():
    parser = argparse.ArgumentParser(description="Generate AI voiceover from script")
    parser.add_argument("script", help="Path to markdown script file")
    parser.add_argument("--voice", default="Aman", help="Voice name (e.g. Aman, Tara, Rishi, Daniel)")
    parser.add_argument("--engine", choices=["auto", "mac", "edge-tts"], default="auto", help="TTS Engine")
    parser.add_argument("--output", default="output/video-voice.m4a", help="Output audio file path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    spoken_lines = extract_spoken_blocks(args.script)

    if not spoken_lines:
        print("Error: No spoken lines found in script.")
        sys.exit(1)

    print(f"Extracted {len(spoken_lines)} spoken sections ({sum(len(s.split()) for s in spoken_lines)} words).")

    engine = args.engine
    if engine == "auto":
        # If Linux/Docker, default to edge-tts; if Mac with say available, default to mac
        if platform.system() != "Darwin":
            engine = "edge-tts"
        else:
            engine = "mac"

    if engine == "edge-tts":
        generate_edge_voice(spoken_lines, args.voice, args.output)
    else:
        generate_mac_voice(spoken_lines, args.voice, args.output)

if __name__ == "__main__":
    main()
