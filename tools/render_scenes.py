#!/usr/bin/env python3
"""render_scenes.py - Generate crisp 1920x1080 scene slides for each beat of the script.

Usage:
    .venv/bin/python tools/render_scenes.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size: int, bold: bool = False):
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

def draw_window_frame(draw, width=1920, height=1080, title="zsh - devbox@macbook: ~/youtube-agent-skill"):
    # Dark modern canvas
    # Window rect
    pad_x, pad_y = 120, 100
    w_w, w_h = width - pad_x * 2, height - pad_y * 2

    # Window shadow / glow
    draw.rectangle([pad_x - 4, pad_y - 4, pad_x + w_w + 4, pad_y + w_h + 4], fill="#1f242c", outline="#30363d", width=2)
    # Window background
    draw.rectangle([pad_x, pad_y, pad_x + w_w, pad_y + w_h], fill="#0d1117")

    # Title bar
    draw.rectangle([pad_x, pad_y, pad_x + w_w, pad_y + 56], fill="#161b22")
    draw.line([pad_x, pad_y + 56, pad_x + w_w, pad_y + 56], fill="#30363d", width=2)

    # Window control dots
    draw.ellipse([pad_x + 24, pad_y + 20, pad_x + 40, pad_y + 36], fill="#ff5f56") # red
    draw.ellipse([pad_x + 50, pad_y + 20, pad_x + 66, pad_y + 36], fill="#ffbd2e") # yellow
    draw.ellipse([pad_x + 76, pad_y + 20, pad_x + 92, pad_y + 36], fill="#27c93f") # green

    # Title text
    font_title = get_font(20)
    draw.text((pad_x + 120, pad_y + 16), title, font=font_title, fill="#8b949e")

    return pad_x + 40, pad_y + 80

def create_scene_3_title_linter(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Terminal - skills/yt-package/title.py")

    font_cmd = get_font(26)
    font_bold = get_font(34)
    font_body = get_font(28)
    font_tag = get_font(22)

    # Header Badge
    draw.rectangle([x, y, x + 380, y + 40], fill="#1f6feb")
    draw.text((x + 16, y + 6), "BEAT 1: PACKAGING LINTER", font=font_tag, fill="#ffffff")

    y += 70
    draw.text((x, y), "$ .venv/bin/python skills/yt-package/title.py \\", font=font_cmd, fill="#58a6ff")
    y += 40
    draw.text((x + 40, y), '--title "11 AI Agents Ran My Entire Channel" \\', font=font_cmd, fill="#79c0ff")
    y += 40
    draw.text((x + 40, y), '--thumb "ZERO HUMANS?"', font=font_cmd, fill="#79c0ff")

    y += 70
    draw.rectangle([x, y, x + 1600, y + 360], fill="#161b22", outline="#238636", width=2)

    # Output text inside box
    bx = x + 40
    by = y + 40
    draw.text((bx, by), '"11 AI Agents Ran My Entire Channel"', font=font_bold, fill="#f0883e")
    by += 55
    draw.text((bx, by), "34 chars   SCORE: 100 / 100", font=font_bold, fill="#3fb950")
    by += 60
    draw.text((bx, by), "✔  ok    34 characters, inside the 60-character desktop cut", font=font_body, fill="#e6edf3")
    by += 45
    draw.text((bx, by), "✔  ok    carries a concrete figure (11)", font=font_body, fill="#e6edf3")
    by += 45
    draw.text((bx, by), "✔  ok    thumbnail and title carry different words (0 duplicate terms)", font=font_body, fill="#e6edf3")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_4_hook_scorer(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Terminal - skills/yt-script/hookscore.py")

    font_cmd = get_font(26)
    font_bold = get_font(32)
    font_mono = get_font(26)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 380, y + 40], fill="#8957e5")
    draw.text((x + 16, y + 6), "BEAT 2: HOOK SCORE ENGINE", font=font_tag, fill="#ffffff")

    y += 65
    draw.text((x, y), '$ .venv/bin/python skills/yt-script/hookscore.py --hook \\', font=font_cmd, fill="#58a6ff")
    y += 38
    draw.text((x + 40, y), '"Before you let 11 AI agents run your channel, look at what broke in 7 days."', font=font_cmd, fill="#f2cc60")

    y += 65
    draw.rectangle([x, y, x + 1600, y + 460], fill="#161b22", outline="#8957e5", width=2)

    bx = x + 40
    by = y + 35
    draw.text((bx, by), "EVALUATION SUMMARY: 5 PARAMETERS", font=font_bold, fill="#58a6ff")
    by += 50
    draw.line([bx, by, bx + 1520, by], fill="#30363d", width=2)
    by += 25

    metrics = [
        ("SPECIFICITY", "79", "###############      (Concrete number: 11, timeframe: 7 days)", "#3fb950"),
        ("ADDRESS    ", "96", "###################  (Direct 'you' in first six words)", "#3fb950"),
        ("STAKES     ", "88", "#################    ('look at what broke')", "#3fb950"),
        ("CURIOSITY  ", "58", "###########          (Cut half of sentence that answers itself)", "#f0883e"),
        ("BREVITY    ", "100", "#################### (15 words / 7 seconds spoken)", "#3fb950"),
    ]

    for name, score, bar, color in metrics:
        draw.text((bx, by), f"{name}   {score.rjust(3)}  {bar}", font=font_mono, fill=color)
        by += 40

    by += 20
    draw.rectangle([bx, by, bx + 500, by + 50], fill="#238636")
    draw.text((bx + 20, by + 8), "FINAL VERDICT: 74 / 100 - STRONG", font=font_bold, fill="#ffffff")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_5_dead_air(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Terminal - skills/yt-edit/deadair.py")

    font_cmd = get_font(26)
    font_bold = get_font(32)
    font_mono = get_font(26)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 420, y + 40], fill="#da3633")
    draw.text((x + 16, y + 6), "BEAT 3: DEAD AIR & CUT LIST", font=font_tag, fill="#ffffff")

    y += 65
    draw.text((x, y), '$ .venv/bin/python skills/yt-edit/deadair.py transcript.srt --floor 0.8s', font=font_cmd, fill="#58a6ff")

    y += 65
    draw.rectangle([x, y, x + 1600, y + 460], fill="#161b22", outline="#da3633", width=2)

    bx = x + 40
    by = y + 35
    draw.text((bx, by), "EDIT DECISION LIST (EDL) - AUTOMATED SILENCE CUTTER", font=font_bold, fill="#f85149")
    by += 50
    draw.line([bx, by, bx + 1520, by], fill="#30363d", width=2)
    by += 25

    cuts = [
        ("00:00:14.200 -> 00:00:15.800", "1.60s PAUSE", "Dead air between hook and turn"),
        ("00:00:44.100 -> 00:00:45.300", "1.20s RETAKE", "Restarted sentence on title formula"),
        ("00:01:22.500 -> 00:01:23.700", "1.20s PAUSE", "Terminal command execution silence"),
        ("00:02:08.900 -> 00:02:10.100", "1.20s SILENCE", "Scrubbing transition cut"),
    ]

    for tc, dur, note in cuts:
        draw.text((bx, by), f"✂  CUT [{tc}]   ({dur}) - {note}", font=font_mono, fill="#e6edf3")
        by += 45

    by += 25
    draw.rectangle([bx, by, bx + 650, by + 50], fill="#b62324")
    draw.text((bx + 20, by + 8), "TOTAL CUT: 5.20s SAVED (0 MANUAL SCRUBBING)", font=font_bold, fill="#ffffff")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_6_the_catch(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Configuration - ~/.claude/youtube/voice.md")

    font_bold = get_font(32)
    font_mono = get_font(26)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 440, y + 40], fill="#d29922")
    draw.text((x + 16, y + 6), "BEAT 4: THE CATCH (HUMAN TASTE)", font=font_tag, fill="#ffffff")

    y += 65
    draw.rectangle([x, y, x + 780, y + 480], fill="#161b22", outline="#f85149", width=2)
    draw.rectangle([x + 820, y, x + 1600, y + 480], fill="#161b22", outline="#3fb950", width=2)

    # Left: AI Sludge (Banned)
    bx1 = x + 30
    by1 = y + 30
    draw.text((bx1, by1), "❌ WORDS I NEVER USE (AI SLUDGE)", font=font_bold, fill="#f85149")
    by1 += 50
    banned = [
        '"Game-changer"',
        '"Mind-blowing"',
        '"Unlock the power"',
        '"Let\'s dive right in"',
        '"Without further ado"',
        '"Secret hack to passive income"'
    ]
    for b in banned:
        draw.text((bx1, by1), f"  • {b}", font=font_mono, fill="#8b949e")
        by1 += 45

    # Right: Voice Profile (Allowed)
    bx2 = x + 850
    by2 = y + 30
    draw.text((bx2, by2), "✔ WORDS I DO USE (SOLO BUILDER)", font=font_bold, fill="#3fb950")
    by2 += 50
    allowed = [
        '"Look at line 42"',
        '"Here is what broke"',
        '"Look at the terminal"',
        '"Under the hood"',
        '"Tested in production"',
        '"The skills write. You upload."'
    ]
    for a in allowed:
        draw.text((bx2, by2), f"  • {a}", font=font_mono, fill="#e6edf3")
        by2 += 45

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_7_github_repo(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="GitHub - Jakeschincariol/youtube-agent-skill")

    font_cmd = get_font(28)
    font_bold = get_font(34)
    font_mono = get_font(26)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 400, y + 40], fill="#238636")
    draw.text((x + 16, y + 6), "PAYOFF & SETUP: 100% FREE", font=font_tag, fill="#ffffff")

    y += 65
    draw.rectangle([x, y, x + 1600, y + 460], fill="#161b22", outline="#30363d", width=2)

    bx = x + 50
    by = y + 40
    draw.text((bx, by), "Jakeschincariol / youtube-agent-skill", font=font_bold, fill="#58a6ff")
    by += 45
    draw.text((bx, by), "11 Claude Skills & 6 Python Creator Tools • MIT License • No API Key Needed", font=font_mono, fill="#8b949e")
    by += 60

    draw.rectangle([bx, by, bx + 1500, by + 120], fill="#0d1117", outline="#238636", width=2)
    draw.text((bx + 30, by + 25), "$ git clone https://github.com/Jakeschincariol/youtube-agent-skill.git", font=font_cmd, fill="#7ee787")
    draw.text((bx + 30, by + 68), "$ cp -r youtube-agent-skill/skills/yt-* ~/.claude/skills/", font=font_cmd, fill="#7ee787")

    by += 160
    draw.text((bx, by), "⭐ Clone the repo, test hookscore.py on your next script, and see what it scores.", font=font_bold, fill="#f0883e")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def main():
    out_dir = "output/scenes"
    os.makedirs(out_dir, exist_ok=True)

    create_scene_3_title_linter(f"{out_dir}/scene-3-title-linter.png")
    create_scene_4_hook_scorer(f"{out_dir}/scene-4-hook-scorer.png")
    create_scene_5_dead_air(f"{out_dir}/scene-5-dead-air.png")
    create_scene_6_the_catch(f"{out_dir}/scene-6-the-catch.png")
    create_scene_7_github_repo(f"{out_dir}/scene-7-github-repo.png")

if __name__ == "__main__":
    main()
