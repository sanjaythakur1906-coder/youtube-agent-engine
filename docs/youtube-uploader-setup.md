# YouTube Uploader Setup Guide

This guide explains how to connect your YouTube channel and upload videos/Shorts using `tools/youtube_uploader.py`.

---

## 1. Prerequisites: Google Cloud Console Setup (Free)

YouTube requires an OAuth 2.0 Client ID to upload videos on your behalf.

### Step 1: Create a Project in Google Cloud
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown at the top and select **New Project**.
3. Name it `YouTube Agent Skill` and click **Create**.

### Step 2: Enable YouTube Data API v3
1. In the search bar at the top, type `YouTube Data API v3`.
2. Click on **YouTube Data API v3** from the marketplace/APIs list.
3. Click the blue **Enable** button.

### Step 3: Configure OAuth Consent Screen
1. In the left sidebar, navigate to **APIs & Services** > **OAuth consent screen**.
2. Select **External** and click **Create**.
3. Fill in:
   - **App name:** `YouTube Agent Uploader`
   - **User support email:** (your email)
   - **Developer contact info:** (your email)
4. Click **Save and Continue**.
5. Under **Scopes**, click **Add or Remove Scopes**:
   - Filter and select: `.../auth/youtube.upload`
6. Click **Save and Continue**.
7. Under **Test users**:
   - Click **Add Users** and enter your Google account email (the one that owns your YouTube channel).
8. Click **Save and Continue**.

### Step 4: Create OAuth 2.0 Client ID
1. Navigate to **APIs & Services** > **Credentials**.
2. Click **+ Create Credentials** at the top > select **OAuth client ID**.
3. **Application type:** Select **Desktop app**.
4. **Name:** `YouTube Desktop Client`.
5. Click **Create**.
6. A popup appears with your credentials. Click **Download JSON**.
7. Rename the downloaded file to `client_secrets.json`.
8. Place it in the project root: `credentials/client_secrets.json`.

*(Note: `credentials/` is already in `.gitignore` so your secrets will never be committed).*

---

## 2. Using the Uploader (`tools/youtube_uploader.py`)

### First Run (Authentication):
The first time you run the command, it opens your browser asking you to authorize your YouTube channel.
Once you log in and grant permission, it saves a reusable token in `credentials/token.json`. Future uploads will run automatically with zero clicks.

### Example 1: Upload Long Video as Private/Draft
```bash
.venv/bin/python tools/youtube_uploader.py \
    --file output/video-01-hinglish-aman.mp4 \
    --title "11 AI Agents Ran My Entire Channel" \
    --desc-file docs/scripts/video-01-seo.md \
    --thumbnail output/thumbnails/concept-1-terminal.jpg \
    --privacy private
```

### Example 2: Upload Short
```bash
.venv/bin/python tools/youtube_uploader.py \
    --file output/short-01-tara.mp4 \
    --title "Don't Upload YouTube Thumbnails Before Checking This #Shorts" \
    --description "Stop wasting 50% of your click surface. Tested on 11 AI creator agents. #Shorts #YouTubeAutomation" \
    --privacy unlisted
```

---

## 3. Privacy Options
- `private`: Only you can view the video in YouTube Studio (Recommended for reviewing).
- `unlisted`: Anyone with the link can view, but does not appear on your public channel feed.
- `public`: Immediately public on your channel.
