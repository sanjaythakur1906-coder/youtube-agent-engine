#!/usr/bin/env python3
"""telegram_reviewer.py - Telegram Review & 1-Tap Approval Gate for YouTube Videos.

Features:
1. Sends video preview, thumbnail, title, and SEO to your Telegram on phone.
2. Attaches inline buttons: [ ✅ Approve & Upload ] and [ ❌ Reject ].
3. When you tap Approve on your phone, uploads video to YouTube automatically.

Usage:
    .venv/bin/python tools/telegram_reviewer.py \
        --video output/short-01-tara.mp4 \
        --thumbnail output/thumbnails/concept-1-terminal.jpg \
        --title "Test Short via Telegram" \
        --description "Automated test description #Shorts" \
        --privacy private
"""

import argparse
import json
import os
import subprocess
import sys
import time
import requests

def load_telegram_credentials(cred_path: str = "credentials/telegram.json"):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        if os.path.exists(cred_path):
            with open(cred_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                token = token or data.get("bot_token")
                chat_id = chat_id or data.get("chat_id")

    if not token or not chat_id:
        print("❌ Error: Telegram credentials not found.")
        print("Provide credentials/telegram.json or set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
        sys.exit(1)

    return token, str(chat_id)

def send_telegram_message(token: str, chat_id: str, text: str, reply_markup=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    res = requests.post(url, json=payload, timeout=15)
    return res.json()

def send_telegram_photo(token: str, chat_id: str, photo_path: str, caption: str):
    if not os.path.exists(photo_path):
        return None
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(photo_path, "rb") as f:
        res = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption[:1024]},
            files={"photo": f},
            timeout=30
        )
    return res.json()

def send_telegram_video(token: str, chat_id: str, video_path: str, caption: str, reply_markup=None):
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return None

    url = f"https://api.telegram.org/bot{token}/sendVideo"
    data = {
        "chat_id": chat_id,
        "caption": caption[:1024],
        "supports_streaming": True,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    print(f"📤 Uploading video preview to Telegram ({os.path.getsize(video_path) / (1024*1024):.1f}MB)...")
    with open(video_path, "rb") as f:
        res = requests.post(url, data=data, files={"video": f}, timeout=120)
    return res.json()

def upload_to_youtube(video_path: str, title: str, description: str, thumbnail: str, privacy: str):
    """Call tools/youtube_uploader.py directly."""
    cmd = [
        sys.executable,
        "tools/youtube_uploader.py",
        "--file", video_path,
        "--title", title,
        "--privacy", privacy
    ]
    if description:
        cmd.extend(["--description", description])
    if thumbnail and os.path.exists(thumbnail):
        cmd.extend(["--thumbnail", thumbnail])

    print("🚀 Triggering YouTube Upload...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    output = res.stdout + res.stderr

    import re
    watch_match = re.search(r"Watch URL:\s+(https://youtu\.be/[a-zA-Z0-9_-]+)", output)
    studio_match = re.search(r"Studio:\s+(https://studio\.youtube\.com/video/[a-zA-Z0-9_-]+/edit)", output)

    watch_url = watch_match.group(1) if watch_match else None
    studio_url = studio_match.group(1) if studio_match else None

    return res.returncode == 0, watch_url, studio_url

def wait_for_decision(token: str, chat_id: str, action_key: str, poll_timeout: int = 86400):
    """Poll for callback query from inline buttons."""
    print("⏳ Waiting for your decision on Telegram phone app...")
    start_time = time.time()
    last_update_id = 0

    while time.time() - start_time < poll_timeout:
        url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}&timeout=20"
        try:
            res = requests.get(url, timeout=25).json()
            if not res.get("ok"):
                time.sleep(3)
                continue

            for update in res.get("result", []):
                last_update_id = update["update_id"]
                if "callback_query" in update:
                    cb = update["callback_query"]
                    data = cb.get("data", "")
                    sender_id = str(cb.get("from", {}).get("id"))

                    if sender_id != chat_id:
                        continue

                    # Answer callback query so button stops loading spinner
                    requests.post(
                        f"https://api.telegram.org/bot{token}/answerCallbackQuery",
                        json={"callback_query_id": cb["id"]}
                    )

                    if data == f"approve_{action_key}":
                        return "approve"
                    elif data == f"reject_{action_key}":
                        return "reject"
        except Exception:
            time.sleep(3)
            continue

    return "timeout"

def review_and_gate(video_path: str, thumbnail_path: str, title: str, description: str, privacy: str = "private"):
    token, chat_id = load_telegram_credentials()
    action_key = str(int(time.time()))

    # Build inline keyboard buttons
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve & Upload", "callback_data": f"approve_{action_key}"},
                {"text": "❌ Reject", "callback_data": f"reject_{action_key}"}
            ]
        ]
    }

    # 1. Send Thumbnail first if available
    if thumbnail_path and os.path.exists(thumbnail_path):
        send_telegram_photo(token, chat_id, thumbnail_path, f"🖼 <b>Thumbnail Concept</b>\nTitle: <b>{title}</b>")

    # 2. Send Video with action buttons
    caption = (
        f"🎬 <b>NEW VIDEO READY FOR REVIEW</b>\n\n"
        f"📌 <b>Title:</b> {title}\n"
        f"🔒 <b>Privacy:</b> {privacy}\n\n"
        f"<i>Watch the video above on your phone. Tap Approve to publish to YouTube or Reject to cancel.</i>"
    )

    resp = send_telegram_video(token, chat_id, video_path, caption, reply_markup=keyboard)
    if not resp or not resp.get("ok"):
        # Fallback to text message with buttons if video upload fails
        send_telegram_message(token, chat_id, caption, reply_markup=keyboard)

    print("📲 Notification sent to your phone. Waiting for your tap...")

    decision = wait_for_decision(token, chat_id, action_key)

    if decision == "approve":
        send_telegram_message(token, chat_id, "⏳ <b>Uploading to your YouTube channel now...</b>")
        success, watch_url, studio_url = upload_to_youtube(video_path, title, description, thumbnail_path, privacy)
        if success:
            msg = (
                f"🎉 <b>UPLOAD COMPLETE!</b>\n\n"
                f"📺 <b>Watch:</b> {watch_url or 'Live in Studio'}\n"
                f"⚙️ <b>Studio Edit:</b> {studio_url or 'Check YouTube Studio'}\n"
                f"🔒 <b>Status:</b> {privacy}"
            )
            send_telegram_message(token, chat_id, msg)
            print("✅ Approved and uploaded successfully!")
            return True
        else:
            send_telegram_message(token, chat_id, "❌ <b>Upload failed. Check server logs.</b>")
            return False
    elif decision == "reject":
        send_telegram_message(token, chat_id, "❌ <b>Video Rejected. Will not be uploaded.</b>")
        print("❌ Video rejected by user.")
        return False
    else:
        send_telegram_message(token, chat_id, "⏰ <b>Review timed out. Video queued for later.</b>")
        return False

def main():
    parser = argparse.ArgumentParser(description="Telegram Review & Approval Gateway")
    parser.add_argument("--video", required=True, help="Video MP4 path")
    parser.add_argument("--thumbnail", default=None, help="Thumbnail path")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    args = parser.parse_args()

    review_and_gate(
        video_path=args.video,
        thumbnail_path=args.thumbnail,
        title=args.title,
        description=args.description,
        privacy=args.privacy
    )

if __name__ == "__main__":
    main()
