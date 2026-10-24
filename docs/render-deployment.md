# Render.com Cloud Deployment Guide

This guide details how to deploy the autonomous daily YouTube publishing engine to [Render.com](https://dashboard.render.com/) so it runs 24/7 in the cloud with zero laptop dependency.

---

## 1. How It Runs on Render
- **Docker Environment:** Includes Python 3.11, FFmpeg, system fonts, and Microsoft Neural TTS (`edge-tts`).
- **Cron Job (`render.yaml`):** Fires automatically every day at 10:00 AM UTC (or your preferred schedule).
- **Execution Flow:**
  1. Finds a fresh breaking AI update or selects from 4 content pillars (`tools/topic_engine.py`).
  2. Generates script, neural voiceover, and synced subtitles.
  3. Compiles 1080p / Short MP4.
  4. Sends video preview + thumbnail to your Telegram app.
  5. Waits for your **[ ✅ Approve & Upload ]** tap on your phone.
  6. Upon approval, uploads the video directly to your YouTube channel!

---

## 2. Step-by-Step Deployment

### Step 1: Push Code to your GitHub Repository
Ensure your latest changes are committed and pushed to your private GitHub repository:
```bash
git add .
git commit -m "Add autonomous daily publisher with Render blueprint and Telegram review"
git push origin main
```

### Step 2: Create a New Blueprint on Render
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** at the top right > select **Blueprint**.
3. Connect your GitHub repository (`youtube-agent-skill`).
4. Render automatically reads `render.yaml`.

### Step 3: Set Environment Variables on Render
Under the service settings, enter the following environment variables:
- `TELEGRAM_BOT_TOKEN`: `8791683238:AAHVP7IpcU3vBig5k-KAhlaZPoYGtHCPSJo`
- `TELEGRAM_CHAT_ID`: `622049170`

To enable YouTube upload from cloud:
- In Render Dashboard under **Secret Files**, add:
  - Filename: `credentials/token.json`
  - Contents: (Paste the contents of your local `credentials/token.json`)
  - Filename: `credentials/client_secrets.json`
  - Contents: (Paste the contents of your local `credentials/client_secrets.json`)

---

## 3. Manual Local Trigger
You can also run the full pipeline anytime locally on your Mac:
```bash
# Generate and send Short to Telegram for 1-tap upload
.venv/bin/python tools/daily_publisher.py --format short

# Generate and send Long video to Telegram for 1-tap upload
.venv/bin/python tools/daily_publisher.py --format long
```
