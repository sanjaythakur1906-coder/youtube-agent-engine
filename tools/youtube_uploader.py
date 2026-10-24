#!/usr/bin/env python3
"""youtube_uploader.py - Upload videos and Shorts to YouTube via YouTube Data API v3.

Usage:
    .venv/bin/python tools/youtube_uploader.py \
        --file output/video-01-hinglish-aman.mp4 \
        --title "11 AI Agents Ran My Entire Channel" \
        --desc-file docs/scripts/video-01-seo.md \
        --thumbnail output/thumbnails/concept-1-terminal.jpg \
        --privacy private
"""

import argparse
import http.client
import httplib2
import os
import random
import re
import sys
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Explicit upload scope
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Retry settings for resumable uploads
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error,
    IOError,
    http.client.NotConnected,
    http.client.IncompleteRead,
    http.client.ImproperConnectionState,
    http.client.CannotSendRequest,
    http.client.CannotSendHeader,
    http.client.ResponseNotReady,
    http.client.BadStatusLine,
)

def get_authenticated_service(client_secrets_file: str, token_file: str):
    """Authenticate with Google OAuth 2.0 and return YouTube service."""
    creds = None
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            if not os.path.exists(client_secrets_file):
                print(f"❌ Error: Client secrets file not found: {client_secrets_file}")
                print("👉 Follow setup guide: docs/youtube-uploader-setup.md")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            print("🔑 Starting authentication...", flush=True)
            print("If browser does not open automatically, copy the link below into your browser:", flush=True)
            creds = flow.run_local_server(port=0, open_browser=True)

        os.makedirs(os.path.dirname(token_file), exist_ok=True)
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"✅ Saved credentials to {token_file}")

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def extract_description_from_file(file_path: str) -> str:
    """Extract clean description text from SEO markdown or text file."""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # If it contains code block with description (like in video-01-seo.md)
    match = re.search(r"## Copy-Paste YouTube Description\s*```(?:text)?\s*([\s\S]*?)```", content)
    if match:
        return match.group(1).strip()
    return content.strip()

def resumable_upload(request):
    """Execute upload with exponential backoff retry."""
    response = None
    error = None
    retry = 0
    max_retries = 10

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%...")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error is not None:
            print(error)
            retry += 1
            if retry > max_retries:
                print("❌ Exceeded max retries. Upload failed.")
                sys.exit(1)
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"Sleeping {sleep_seconds:.1f} seconds and then retrying...")
            time.sleep(sleep_seconds)
            error = None

    return response

def set_thumbnail(youtube, video_id: str, thumbnail_path: str):
    """Set custom thumbnail for uploaded video."""
    if not os.path.exists(thumbnail_path):
        print(f"Warning: Thumbnail path does not exist: {thumbnail_path}")
        return

    print(f"Uploading thumbnail: {thumbnail_path}...")
    try:
        req = youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        )
        req.execute()
        print("✅ Custom thumbnail uploaded successfully.")
    except Exception as e:
        print(f"⚠️ Warning: Could not upload thumbnail: {e}")

def upload_video(youtube, options):
    """Upload video to YouTube."""
    if not os.path.exists(options.file):
        print(f"❌ Error: Video file not found: {options.file}")
        sys.exit(1)

    description = options.description or ""
    if options.desc_file:
        description = extract_description_from_file(options.desc_file)

    tags = None
    if options.tags:
        tags = [t.strip() for t in options.tags.split(",") if t.strip()]

    body = {
        "snippet": {
            "title": options.title,
            "description": description,
            "tags": tags,
            "categoryId": options.category
        },
        "status": {
            "privacyStatus": options.privacy,
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"🚀 Initializing upload for: {options.file}")
    print(f"   Title:   {options.title}")
    print(f"   Privacy: {options.privacy}")

    media = MediaFileUpload(
        options.file,
        chunksize=1024 * 1024 * 4,  # 4MB chunks
        resumable=True
    )

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    )

    response = resumable_upload(request)
    video_id = response.get("id")

    if video_id:
        print("\n🎉 Upload Successful!")
        print(f"   Video ID:  {video_id}")
        print(f"   Watch URL: https://youtu.be/{video_id}")
        print(f"   Studio:    https://studio.youtube.com/video/{video_id}/edit")

        if options.thumbnail:
            set_thumbnail(youtube, video_id, options.thumbnail)

    return video_id

def main():
    parser = argparse.ArgumentParser(description="Upload videos and Shorts to YouTube")
    parser.add_argument("--file", required=True, help="Video file path (.mp4)")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", default=None, help="Video description text")
    parser.add_argument("--desc-file", default=None, help="Markdown/text file containing description")
    parser.add_argument("--tags", default="ai agents, youtube automation, python, programming", help="Comma-separated tags")
    parser.add_argument("--category", default="28", help="Numeric category id (28 = Science & Technology)")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private", help="Privacy status")
    parser.add_argument("--thumbnail", default=None, help="Thumbnail image path")
    parser.add_argument("--credentials", default="credentials/client_secrets.json", help="Google OAuth client secrets JSON")
    parser.add_argument("--token", default="credentials/token.json", help="OAuth token cache path")
    args = parser.parse_args()

    youtube = get_authenticated_service(args.credentials, args.token)
    upload_video(youtube, args)

if __name__ == "__main__":
    main()
