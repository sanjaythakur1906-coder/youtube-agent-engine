#!/usr/bin/env python3
"""render_short_scenes.py - Generate 1080x1920 vertical scene slides for Short 01.

Usage:
    .venv/bin/python tools/render_short_scenes.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size: int):
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf"
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_vertical_window(draw, title="Terminal - skills/yt-package/title.py"):
    # Window rect centered vertically
    pad_x = 60
    pad_y = 480
    w_w = 1080 - pad_x * 2
    w_h = 960

    draw.rectangle([pad_x - 3, pad_y - 3, pad_x + w_w + 3, pad_y + w_h + 3], fill="#1f242c", outline="#30363d", width=2)
    draw.rectangle([pad_x, pad_y, pad_x + w_w, pad_y + w_h], fill="#0d1117")

    # Title bar
    draw.rectangle([pad_x, pad_y, pad_x + w_w, pad_y + 54], fill="#161b22")
    draw.line([pad_x, pad_y + 54, pad_x + w_w, pad_y + 54], fill="#30363d", width=2)

    # Dots
    draw.ellipse([pad_x + 20, pad_y + 20, pad_x + 34, pad_y + 34], fill="#ff5f56")
    draw.ellipse([pad_x + 44, pad_y + 20, pad_x + 58, pad_y + 34], fill="#ffbd2e")
    draw.ellipse([pad_x + 68, pad_y + 20, pad_x + 82, pad_y + 34], fill="#27c93f")

    font_title = get_font(20)
    draw.text((pad_x + 100, pad_y + 16), title, font=font_title, fill="#8b949e")

    return pad_x + 35, pad_y + 75

def render_short_scene_1(out_path: str):
    img = Image.new("RGB", (1080, 1920), "#080b0f")
    draw = ImageDraw.Draw(img)

    font_huge = get_font(72)
    font_sub = get_font(36)
    font_tag = get_font(28)

    # Top Tag
    draw.rectangle([100, 220, 980, 310], fill="#b62324")
    draw.text((140, 240), "CRITICAL YOUTUBE MISTAKE", font=font_tag, fill="#ffffff")

    # Warning Box
    draw.rectangle([60, 480, 1020, 1340], fill="#161b22", outline="#ff5f56", width=4)

    draw.text((100, 540), "⚠️ STOP!", font=font_huge, fill="#f85149")
    draw.text((100, 650), "DON'T UPLOAD YET", font=font_huge, fill="#f2cc60")

    draw.line([100, 770, 980, 770], fill="#30363d", width=3)

    draw.text((100, 830), "Your thumbnail might be", font=font_sub, fill="#e6edf3")
    draw.text((100, 880), "wasting 50% of your click surface.", font=font_sub, fill="#f85149")

    draw.rectangle([100, 980, 980, 1240], fill="#0d1117", outline="#8b949e", width=2)
    draw.text((130, 1020), "$ python title.py check", font=font_sub, fill="#58a6ff")
    draw.text((130, 1080), "FAIL: Duplicate words found!", font=font_sub, fill="#f85149")
    draw.text((130, 1140), "Score: 35 / 100 (REJECTED)", font=font_sub, fill="#ff5f56")

    img.save(out_path, quality=95)
    print(f"Generated {out_path}")

def render_short_scene_2(out_path: str):
    img = Image.new("RGB", (1080, 1920), "#080b0f")
    draw = ImageDraw.Draw(img)

    font_title = get_font(44)
    font_bold = get_font(34)
    font_mono = get_font(28)

    # Top Header
    draw.rectangle([100, 220, 980, 310], fill="#da3633")
    draw.text((140, 240), "THE DUPLICATION TRAP", font=font_bold, fill="#ffffff")

    # Bad example card
    draw.rectangle([60, 480, 1020, 1340], fill="#161b22", outline="#f85149", width=3)

    draw.text((100, 540), "❌ WHAT 90% OF CREATORS DO:", font=font_title, fill="#f85149")

    by = 640
    draw.rectangle([100, by, 980, by + 180], fill="#0d1117", outline="#30363d", width=2)
    draw.text((130, by + 25), "VIDEO TITLE:", font=font_bold, fill="#8b949e")
    draw.text((130, by + 80), '"How AI Built My Channel"', font=font_bold, fill="#f2cc60")

    by += 240
    draw.rectangle([100, by, 980, by + 180], fill="#0d1117", outline="#30363d", width=2)
    draw.text((130, by + 25), "THUMBNAIL TEXT (DUPLICATE):", font=font_bold, fill="#8b949e")
    draw.text((130, by + 80), '"AI BUILT MY CHANNEL"', font=font_bold, fill="#f85149")

    by += 240
    draw.rectangle([100, by, 980, by + 110], fill="#b62324")
    draw.text((140, by + 30), "WASTES 50% OF CLICK SURFACE!", font=font_bold, fill="#ffffff")

    img.save(out_path, quality=95)
    print(f"Generated {out_path}")

def render_short_scene_3(out_path: str):
    img = Image.new("RGB", (1080, 1920), "#080b0f")
    draw = ImageDraw.Draw(img)

    x, y = draw_vertical_window(draw, "Terminal - yt-package/title.py")

    font_cmd = get_font(26)
    font_bold = get_font(32)
    font_body = get_font(26)

    draw.text((x, y), "$ .venv/bin/python title.py \\", font=font_cmd, fill="#58a6ff")
    y += 40
    draw.text((x + 20, y), '--title "11 AI Agents Ran My Entire Channel" \\', font=font_cmd, fill="#79c0ff")
    y += 40
    draw.text((x + 20, y), '--thumb "ZERO HUMANS?"', font=font_cmd, fill="#79c0ff")

    y += 65
    draw.rectangle([x, y, x + 900, y + 540], fill="#161b22", outline="#238636", width=2)

    bx = x + 30
    by = y + 35
    draw.text((bx, by), "PERFECT 100/100 SCORE", font=font_bold, fill="#3fb950")
    by += 55
    draw.text((bx, by), 'Title: 34 characters (Mobile OK)', font=font_body, fill="#e6edf3")
    by += 45
    draw.text((bx, by), '✔ Carries concrete figure (11)', font=font_body, fill="#3fb950")
    by += 45
    draw.text((bx, by), '✔ 0 duplicate words between title & thumb', font=font_body, fill="#3fb950")
    by += 60

    draw.rectangle([bx, by, bx + 840, by + 120], fill="#0d1117", outline="#30363d", width=2)
    draw.text((bx + 20, by + 20), "TITLE: 11 AI Agents Ran My Entire Channel", font=font_body, fill="#58a6ff")
    draw.text((bx + 20, by + 65), "THUMB: ZERO HUMANS?", font=font_bold, fill="#f2cc60")

    img.save(out_path, quality=95)
    print(f"Generated {out_path}")

def render_short_scene_4(out_path: str):
    img = Image.new("RGB", (1080, 1920), "#080b0f")
    draw = ImageDraw.Draw(img)

    font_huge = get_font(52)
    font_bold = get_font(34)
    font_mono = get_font(26)

    draw.rectangle([100, 220, 980, 310], fill="#238636")
    draw.text((140, 240), "FREE & OPEN SOURCE TOOL", font=font_bold, fill="#ffffff")

    draw.rectangle([60, 480, 1020, 1340], fill="#161b22", outline="#238636", width=3)

    draw.text((100, 540), "CLONE & RUN LOCAL:", font=font_huge, fill="#58a6ff")

    by = 650
    draw.rectangle([100, by, 980, by + 150], fill="#0d1117", outline="#238636", width=2)
    draw.text((130, by + 30), "$ git clone \\", font=font_mono, fill="#7ee787")
    draw.text((130, by + 75), "  youtube-agent-skill.git", font=font_mono, fill="#7ee787")

    by += 220
    draw.rectangle([100, by, 980, by + 240], fill="#0d1117", outline="#f0883e", width=2)
    draw.text((130, by + 35), "WATCH FULL LONG VIDEO ⬇️", font=font_bold, fill="#f0883e")
    draw.text((130, by + 90), '"11 AI Agents Ran My Entire Channel"', font=font_mono, fill="#e6edf3")
    draw.text((130, by + 145), "Click related video linked below!", font=font_mono, fill="#8b949e")

    img.save(out_path, quality=95)
    print(f"Generated {out_path}")

def main():
    out_dir = "output/scenes/short-01"
    os.makedirs(out_dir, exist_ok=True)
    render_short_scene_1(f"{out_dir}/short-scene-1.png")
    render_short_scene_2(f"{out_dir}/short-scene-2.png")
    render_short_scene_3(f"{out_dir}/short-scene-3.png")
    render_short_scene_4(f"{out_dir}/short-scene-4.png")

if __name__ == "__main__":
    main()
