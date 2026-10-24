# Topic Engine & Deduplication System

This document details the autonomous topic selection, breaking news scanner, and quality validation engine (`tools/topic_engine.py`).

---

## 1. How It Works
The engine executes before any script or video is created:

1. **GitHub Release Scanner:**
   - Automatically polls official repositories (`ollama/ollama`, `browser-use/browser-use`, `deepseek-ai`, `BerriAI/litellm`).
   - If a new version or breaking update was released in the last 48 hours, it instantly prioritizes a "Day 1 Test / What Broke" video.

2. **4 Core Content Pillars:**
   If no breaking update exists, it selects the next topic from `data/topics_bank.json` across 4 rotating pillars:
   - `local_llms`: Ollama, DeepSeek R1, vLLM, quantizations, Apple Silicon limits.
   - `coding_agents`: Claude Code, Cursor, Aider, Antigravity.
   - `python_automation`: Browser-use, Playwright, Scrapy, API scrapers.
   - `ai_voice_media`: Whisper offline transcription, Kokoro TTS, video automation.

3. **Deduplication Engine (`output/history.json`):**
   - Reads all published video IDs.
   - Filters out previously covered topics and tools so the channel never repeats angles within 30 days.

4. **Quality Gate:**
   - Automatically executes `skills/yt-package/title.py` to ensure package score is near 100/100.
   - Automatically executes `skills/yt-script/hookscore.py` to ensure hook meets threshold (> 65-70).

---

## 2. Usage
```bash
.venv/bin/python tools/topic_engine.py
```
Outputs selected topic, validated scores, and visual beat roadmap.
