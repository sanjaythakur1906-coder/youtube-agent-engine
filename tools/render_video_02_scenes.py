#!/usr/bin/env python3
"""render_video_02_scenes.py - Generate 1920x1080 scene slides for Video 02.

Usage:
    .venv/bin/python tools/render_video_02_scenes.py
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

def draw_window_frame(draw, width=1920, height=1080, title="zsh - devbox@macbook: ~/ollama"):
    pad_x, pad_y = 120, 100
    w_w, w_h = width - pad_x * 2, height - pad_y * 2

    draw.rectangle([pad_x - 4, pad_y - 4, pad_x + w_w + 4, pad_y + w_h + 4], fill="#1f242c", outline="#30363d", width=2)
    draw.rectangle([pad_x, pad_y, pad_x + w_w, pad_y + w_h], fill="#0d1117")

    draw.rectangle([pad_x, pad_y, pad_x + w_w, pad_y + 56], fill="#161b22")
    draw.line([pad_x, pad_y + 56, pad_x + w_w, pad_y + 56], fill="#30363d", width=2)

    draw.ellipse([pad_x + 24, pad_y + 20, pad_x + 40, pad_y + 36], fill="#ff5f56")
    draw.ellipse([pad_x + 50, pad_y + 20, pad_x + 66, pad_y + 36], fill="#ffbd2e")
    draw.ellipse([pad_x + 76, pad_y + 20, pad_x + 92, pad_y + 36], fill="#27c93f")

    font_title = get_font(20)
    draw.text((pad_x + 120, pad_y + 16), title, font=font_title, fill="#8b949e")

    return pad_x + 40, pad_y + 80

def create_scene_2_turn(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Comparison - Cloud vs Local AI")

    font_bold = get_font(34)
    font_sub = get_font(28)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 420, y + 40], fill="#1f6feb")
    draw.text((x + 16, y + 6), "LOCAL VS CLOUD REALITY", font=font_tag, fill="#ffffff")

    y += 70
    draw.rectangle([x, y, x + 760, y + 460], fill="#161b22", outline="#f85149", width=2)
    draw.rectangle([x + 820, y, x + 1580, y + 460], fill="#161b22", outline="#3fb950", width=2)

    # Cloud Side
    bx1 = x + 40
    by1 = y + 40
    draw.text((bx1, by1), "☁️ CLOUD AI (ChatGPT / Claude)", font=font_bold, fill="#f85149")
    by1 += 60
    draw.text((bx1, by1), "• $20 / month subscription", font=font_sub, fill="#e6edf3")
    by1 += 50
    draw.text((bx1, by1), "• All prompt data sent to cloud", font=font_sub, fill="#8b949e")
    by1 += 50
    draw.text((bx1, by1), "• Rate limits & outage risk", font=font_sub, fill="#8b949e")
    by1 += 50
    draw.text((bx1, by1), "• Requires fast constant internet", font=font_sub, fill="#8b949e")

    # Local Side
    bx2 = x + 860
    by2 = y + 40
    draw.text((bx2, by2), "💻 LOCAL DEEPSEEK R1 (Ollama)", font=font_bold, fill="#3fb950")
    by2 += 60
    draw.text((bx2, by2), "• $0 / month (100% Free Forever)", font=font_sub, fill="#3fb950")
    by2 += 50
    draw.text((bx2, by2), "• Zero data tracking (100% Private)", font=font_sub, fill="#e6edf3")
    by2 += 50
    draw.text((bx2, by2), "• Unlimited queries, zero rate limits", font=font_sub, fill="#e6edf3")
    by2 += 50
    draw.text((bx2, by2), "• Runs 100% offline (Airplane mode)", font=font_sub, fill="#e6edf3")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_3_hardware(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Hardware Benchmarks - RAM vs Token Speed")

    font_bold = get_font(32)
    font_mono = get_font(26)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 440, y + 40], fill="#8957e5")
    draw.text((x + 16, y + 6), "HARDWARE BENCHMARK: 7B vs 14B vs 32B", font=font_tag, fill="#ffffff")

    y += 70
    draw.rectangle([x, y, x + 1580, y + 460], fill="#161b22", outline="#8957e5", width=2)

    bx = x + 40
    by = y + 35
    draw.text((bx, by), "MODEL SIZE      RAM NEEDED      SPEED           VERDICT", font=font_bold, fill="#58a6ff")
    by += 45
    draw.line([bx, by, bx + 1500, by], fill="#30363d", width=2)
    by += 30

    rows = [
        ("DeepSeek 7B   ", " 8 GB RAM   ", "35 tokens/sec  ", "Lightweight, but hallucinates on deep bugs", "#8b949e"),
        ("DeepSeek 14B  ", "16 GB RAM   ", "22 tokens/sec  ", "⭐ BEST SWEET SPOT for Apple Silicon / PC", "#3fb950"),
        ("DeepSeek 32B  ", "32+ GB RAM  ", " 2 tokens/sec  ", "Chokes on 16GB laptops (Swap memory lag)", "#f85149"),
    ]

    for model, ram, spd, note, col in rows:
        draw.text((bx, by), f"{model}  {ram}  {spd}  {note}", font=font_mono, fill=col)
        by += 65

    by += 20
    draw.rectangle([bx, by, bx + 950, by + 50], fill="#238636")
    draw.text((bx + 20, by + 10), "RECOMMENDATION: 14B (Q4 Quantized) = Production Ready", font=font_bold, fill="#ffffff")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_4_code_benchmark(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Terminal - DeepSeek R1 Live Reasoning Stream")

    font_cmd = get_font(26)
    font_bold = get_font(30)
    font_mono = get_font(24)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 460, y + 40], fill="#238636")
    draw.text((x + 16, y + 6), "LIVE REASONING STREAM TEST", font=font_tag, fill="#ffffff")

    y += 65
    draw.text((x, y), '$ ollama run deepseek-r1:14b "Fix circular import AST recursion in parser.py"', font=font_cmd, fill="#58a6ff")

    y += 55
    draw.rectangle([x, y, x + 1580, y + 470], fill="#161b22", outline="#238636", width=2)

    bx = x + 35
    by = y + 30
    draw.text((bx, by), "<think>", font=font_bold, fill="#f2cc60")
    by += 40
    thoughts = [
        "Analyzing call stack in recursive import resolution...",
        "Detected cycle between module_a and module_b AST nodes.",
        "Need memoization: maintain a 'visited = set()' tracking active parent traversal.",
        "If node in visited: raise CircularDependencyError instead of stack overflow.",
        "Refactoring parser method to pass visited context state down the tree...",
    ]
    for t in thoughts:
        draw.text((bx + 20, by), f"• {t}", font=font_mono, fill="#8b949e")
        by += 35

    draw.text((bx, by), "</think>", font=font_bold, fill="#f2cc60")
    by += 45
    draw.text((bx, by), "def resolve_ast_imports(node, visited=None):", font=font_mono, fill="#79c0ff")
    by += 32
    draw.text((bx + 40, by), "visited = visited or set()", font=font_mono, fill="#e6edf3")
    by += 32
    draw.text((bx + 40, by), "if node.id in visited: return CircularRef(node.id)", font=font_mono, fill="#7ee787")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_5_the_catch(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Monitoring - Local Limitations & Hardware Drain")

    font_bold = get_font(32)
    font_sub = get_font(26)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 440, y + 40], fill="#da3633")
    draw.text((x + 16, y + 6), "THE CATCH: WHERE LOCAL AI FAILS", font=font_tag, fill="#ffffff")

    y += 70
    draw.rectangle([x, y, x + 1580, y + 460], fill="#161b22", outline="#da3633", width=2)

    bx = x + 40
    by = y + 40
    draw.text((bx, by), "⚠️ TWO CRITICAL BOTTLENECK LIMITS:", font=font_bold, fill="#f85149")
    by += 60

    draw.text((bx, by), "1. CONTEXT WINDOW (8,000 TOKENS CEILING)", font=font_bold, fill="#f2cc60")
    by += 45
    draw.text((bx + 30, by), "• Once repository files exceed 8K tokens, model starts hallucinating.", font=font_sub, fill="#e6edf3")
    by += 40
    draw.text((bx + 30, by), "• Cannot ingest 50+ file codebases like Claude 3.5 Sonnet (200k window).", font=font_sub, fill="#8b949e")
    by += 65

    draw.text((bx, by), "2. BATTERY & THERMAL THROTTLING", font=font_bold, fill="#f2cc60")
    by += 45
    draw.text((bx + 30, by), "• Battery drops 100% -> 20% in under 2 hours of reasoning workloads.", font=font_sub, fill="#e6edf3")
    by += 40
    draw.text((bx + 30, by), "• Fans run at maximum RPM; best used plugged into wall power at desk.", font=font_sub, fill="#8b949e")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def create_scene_6_setup_commands(output_path: str):
    img = Image.new("RGB", (1920, 1080), "#080b0f")
    draw = ImageDraw.Draw(img)
    x, y = draw_window_frame(draw, title="Terminal - Quick Setup Commands")

    font_cmd = get_font(30)
    font_bold = get_font(34)
    font_mono = get_font(26)
    font_tag = get_font(22)

    draw.rectangle([x, y, x + 440, y + 40], fill="#238636")
    draw.text((x + 16, y + 6), "OFFLINE SETUP IN 3 COMMANDS", font=font_tag, fill="#ffffff")

    y += 65
    draw.rectangle([x, y, x + 1580, y + 470], fill="#161b22", outline="#238636", width=2)

    bx = x + 50
    by = y + 45
    draw.text((bx, by), "RUN COMPLETELY OFFLINE IN 5 MINUTES:", font=font_bold, fill="#58a6ff")
    by += 65

    draw.rectangle([bx, by, bx + 1480, by + 180], fill="#0d1117", outline="#30363d", width=2)
    draw.text((bx + 30, by + 30), "$ brew install ollama", font=font_cmd, fill="#7ee787")
    draw.text((bx + 30, by + 80), "$ ollama run deepseek-r1:14b", font=font_cmd, fill="#7ee787")
    draw.text((bx + 30, by + 130), "$ # Optional 8GB laptop fallback: ollama run deepseek-r1:7b", font=font_mono, fill="#8b949e")

    by += 220
    draw.text((bx, by), "⭐ Description me pinned commands aur memory guides check karo!", font=font_bold, fill="#f2cc60")

    img.save(output_path, quality=95)
    print(f"Generated {output_path}")

def main():
    out_dir = "output/scenes/video-02"
    os.makedirs(out_dir, exist_ok=True)

    # Scene 1: use resized thumbnail
    thumb_path = "output/thumbnails/video-02-zero-cloud.jpg"
    if os.path.exists(thumb_path):
        im = Image.open(thumb_path).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
        im.save(f"{out_dir}/scene-1-hook.png", "PNG")
        print(f"Generated {out_dir}/scene-1-hook.png")

    create_scene_2_turn(f"{out_dir}/scene-2-turn.png")
    create_scene_3_hardware(f"{out_dir}/scene-3-hardware.png")
    create_scene_4_code_benchmark(f"{out_dir}/scene-4-code-benchmark.png")
    create_scene_5_the_catch(f"{out_dir}/scene-5-the-catch.png")
    create_scene_6_setup_commands(f"{out_dir}/scene-6-setup-commands.png")

if __name__ == "__main__":
    main()
