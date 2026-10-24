# Faceless Production Pipeline

This document details the automated faceless video generation workflow.

## 1. Overview
The channel runs without on-camera recording or manual microphone voiceover.
- **Script:** Generated and scored via `skills/yt-script` and `skills/yt-package`.
- **Voiceover:** Generated using macOS native Speech Synthesizer (`say`) or `edge-tts` via `.venv/bin/python`.
- **Subtitles:** Automatically exported as `.vtt` / `.srt` with sentence-level timing.
- **Visual Scenes:** Automated generation of 1080p terminal cards and high-CTR visuals matching script beats.
- **Visual Assembly:** Automated FFmpeg compilation of dynamic multi-scene cuts + audio + burned-in subtitles into ready-to-upload MP4.

---

## 2. Voice Generation (`tools/generate_voice.py`)
Supports two engines:
1. **macOS Native (`say`)**: Works completely offline on Mac (`Aman`, `Tara`, `Rishi`, `Daniel`).
2. **Microsoft Neural TTS (`edge-tts`)**: Cloud-ready for Linux, Docker, and Render without API keys.
   - `Aman` -> `en-IN-PrabhatNeural` (Male Indian Tech)
   - `Tara` -> `en-IN-NeerjaNeural` (Female Indian Tech)
   - `Rishi` -> `hi-IN-MadhurNeural` (Hindi Conversational)
   - `Daniel` -> `en-GB-RyanNeural` (UK Tech)

- **Execution:**
  ```bash
  # Local macOS Speech Engine
  .venv/bin/python tools/generate_voice.py docs/scripts/video-01-hinglish.md --voice Aman --output output/video-01-voice.m4a

  # Cloud Neural Engine (Linux / Render / Docker)
  .venv/bin/python tools/generate_voice.py docs/scripts/video-01-hinglish.md --engine edge-tts --voice Aman --output output/video-01-voice.mp3
  ```
- **Generated Outputs:**
  - Local macOS: `output/video-01-hinglish-aman.m4a`
  - Cloud Neural: `output/test_cloud_aman.mp3`, `output/test_cloud_tara.mp3`

---

## 3. Subtitle Generation (`tools/generate_subtitles.py`)
Extracts spoken segments from script markdown, calculates proportional durations matching audio length, and writes formatted SRT and WebVTT tracks.
- **Execution:**
  ```bash
  # English
  .venv/bin/python tools/generate_subtitles.py docs/scripts/video-01-script.md --audio output/video-01-voice.m4a --output-srt output/video-01.srt --output-vtt output/video-01.vtt

  # Hinglish
  .venv/bin/python tools/generate_subtitles.py docs/scripts/video-01-hinglish.md --audio output/video-01-hinglish.m4a --output-srt output/video-01-hinglish.srt --output-vtt output/video-01-hinglish.vtt
  ```
- **Generated Outputs:**
  - `output/video-01.srt` / `output/video-01.vtt` (English)
  - `output/video-01-hinglish.srt` / `output/video-01-hinglish.vtt` (Hinglish)

---

## 4. Scene Card Rendering (`tools/render_scenes.py`)
Generates 1920x1080 high-contrast dark-mode macOS terminal cards for each script beat:
- `output/scenes/scene-1-hook.png` (Hook: Terminal crash)
- `output/scenes/scene-2-overview.png` (11 agent skills overview)
- `output/scenes/scene-3-title-linter.png` (Beat 1: `title.py` 100/100 score)
- `output/scenes/scene-4-hook-scorer.png` (Beat 2: `hookscore.py` 74 STRONG)
- `output/scenes/scene-5-dead-air.png` (Beat 3: `deadair.py` silence cuts)
- `output/scenes/scene-6-the-catch.png` (Beat 4: `voice.md` rules vs AI sludge)
- `output/scenes/scene-7-github-repo.png` (Payoff: GitHub repo clone instructions)

- **Execution:**
  ```bash
  .venv/bin/python tools/render_scenes.py
  ```

---

## 5. Dynamic Video Assembly (`tools/build_video.py`)
Uses `ffmpeg` to stitch dynamic scene schedule, voiceover audio track, and burned-in subtitles into 1080p 16:9 MP4.
- **Execution:**
  ```bash
  # English 1080p Video
  .venv/bin/python tools/build_video.py \
      --scenes-dir output/scenes \
      --audio output/video-01-voice.m4a \
      --subtitles output/video-01.srt \
      --output output/video-01.mp4

  # Hinglish 1080p Video (Rishi - Male)
  .venv/bin/python tools/build_video.py \
      --scenes-dir output/scenes \
      --audio output/video-01-hinglish.m4a \
      --subtitles output/video-01-hinglish.srt \
      --output output/video-01-hinglish.mp4

  # Hinglish 1080p Video (Aman - Male)
  .venv/bin/python tools/build_video.py \
      --scenes-dir output/scenes \
      --audio output/video-01-hinglish-aman.m4a \
      --subtitles output/video-01-hinglish-aman.srt \
      --output output/video-01-hinglish-aman.mp4

  # Hinglish 1080p Video (Tara - Female)
  .venv/bin/python tools/build_video.py \
      --scenes-dir output/scenes \
      --audio output/video-01-hinglish-tara.m4a \
      --subtitles output/video-01-hinglish-tara.srt \
      --output output/video-01-hinglish-tara.mp4
  ```
- **Generated Outputs:**
  - `output/video-01.mp4` (1080p English - Daniel, 6.5MB)
  - `output/video-01-hinglish.mp4` (1080p Hinglish - Rishi, 6.6MB)
  - `output/video-01-hinglish-aman.mp4` (1080p Hinglish - Aman, 6.2MB)
  - `output/video-01-hinglish-tara.mp4` (1080p Hinglish - Tara, 6.3MB)

---

## 6. YouTube Shorts Production (`tools/build_short.py`)
Generates 9:16 vertical 1080x1920 video with centered terminal cards and bold subtitle captions.
- **Script:** [docs/scripts/short-01-script.md](docs/scripts/short-01-script.md) (45s hook on duplicate words trap)
- **Scene Generator:** `tools/render_short_scenes.py`
- **Execution:**
  ```bash
  # 1. Render vertical scenes
  .venv/bin/python tools/render_short_scenes.py

  # 2. Generate voiceover (Tara)
  .venv/bin/python tools/generate_voice.py docs/scripts/short-01-script.md --voice Tara --output output/short-01-tara.m4a

  # 3. Generate subtitles
  .venv/bin/python tools/generate_subtitles.py docs/scripts/short-01-script.md --audio output/short-01-tara.m4a --output-srt output/short-01-tara.srt --output-vtt output/short-01-tara.vtt

  # 4. Assemble 9:16 Short MP4
  .venv/bin/python tools/build_short.py \
      --scenes-dir output/scenes/short-01 \
      --audio output/short-01-tara.m4a \
      --subtitles output/short-01-tara.srt \
      --output output/short-01-tara.mp4
  ```
- **Generated Output:**
  - `output/short-01-tara.mp4` (1080x1920 9:16 vertical, 36s, 766KB)

---

## 7. YouTube Channel Uploader (`tools/youtube_uploader.py`)
Uploads long videos and vertical Shorts to your YouTube channel using Google YouTube Data API v3 and OAuth 2.0.
- **Setup Guide:** [docs/youtube-uploader-setup.md](youtube-uploader-setup.md)
- **Features:**
  - Resumable chunked upload.
  - Safe defaults (`private` / `unlisted`).
  - Sets title, description (from SEO file), tags, and custom thumbnail.
- **Execution:**
  ```bash
  # Upload Long Video
  .venv/bin/python tools/youtube_uploader.py \
      --file output/video-01-hinglish-aman.mp4 \
      --title "11 AI Agents Ran My Entire Channel" \
      --desc-file docs/scripts/video-01-seo.md \
      --thumbnail output/thumbnails/concept-1-terminal.jpg \
      --privacy private

  # Upload Short
  .venv/bin/python tools/youtube_uploader.py \
      --file output/short-01-tara.mp4 \
      --title "Don't Upload YouTube Thumbnails Before Checking This #Shorts" \
      --description "Stop wasting 50% of your click surface. Tested on 11 AI creator agents. #Shorts #YouTubeAutomation" \
      --privacy unlisted

  # Upload Video 02 (DeepSeek R1 Local)
  .venv/bin/python tools/youtube_uploader.py \
      --file output/video-02-hinglish-aman.mp4 \
      --title "I Ran DeepSeek R1 Locally for 7 Days" \
      --desc-file docs/scripts/video-02-seo.md \
      --thumbnail output/thumbnails/video-02-zero-cloud.jpg \
      --privacy private
  ```

---

## 8. Published YouTube Video Registry
| Video | Title | Type | Video ID | Watch Link | Studio Edit |
| --- | --- | --- | --- | --- | --- |
| **Video 01** | `11 AI Agents Ran My Entire Channel` | Long Form (1080p) | `Sij_i7jKCrY` | [Watch](https://youtu.be/Sij_i7jKCrY) | [Edit](https://studio.youtube.com/video/Sij_i7jKCrY/edit) |
| **Short 01** | `Don't Upload YouTube Thumbnails Before Checking This` | Short (9:16) | `q8gXzDksX4M` | [Watch](https://youtu.be/q8gXzDksX4M) | [Edit](https://studio.youtube.com/video/q8gXzDksX4M/edit) |
| **Video 02** | `I Ran DeepSeek R1 Locally for 7 Days` | Long Form (1080p) | `6hbMr5p3Bng` | [Watch](https://youtu.be/6hbMr5p3Bng) | [Edit](https://studio.youtube.com/video/6hbMr5p3Bng/edit) |
