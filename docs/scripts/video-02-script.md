# Video 2 Script: "I Ran DeepSeek R1 Locally for 7 Days"

## Top Tested Hook
- **Hook Line:** "Before you pay 20 dollars for ChatGPT, look at what broke running local AI for 7 days."
- **Score:** 73/100 STRONG (`skills/yt-script/hookscore.py` - Formula: I Tried It)
- **Packaging:** Title `I Ran DeepSeek R1 Locally for 7 Days` | Thumb `ZERO CLOUD?` (100/100)

---

## Spoken Script with On-Screen Visual Beats

### [0:00 - 0:15] The Hook
**[ON SCREEN: Terminal window running `ollama run deepseek-r1:14b` with thermal monitor showing 98°C and memory usage spiking at 15.8GB / 16GB]**

**Spoken:**
Before you pay 20 dollars for ChatGPT, look at what broke running local AI for 7 days.

---

### [0:15 - 0:45] The Turn
**[ON SCREEN: Split view: Left showing Ollama local terminal with 0ms cloud latency; Right showing OpenAI subscription cancellation screen]**

**Spoken:**
Everyone is hyping local reasoning models as the instant death of cloud AI subscriptions. Zero API costs, zero data tracking, complete privacy. I ran DeepSeek R1 completely offline on this machine for one full week of actual coding work. Here is what actually worked, and the exact limits where your hardware will tap out.

---

### [0:45 - 2:00] Beat 1: The Hardware Reality (7B vs 14B vs 32B)
**[ON SCREEN: Terminal running `btop` / `htop` showing RAM memory pressure and token-per-second benchmarks across quantized models]**

**Spoken:**
First, let's kill the hype about hardware. You don't need a 5,000-dollar Nvidia rig, but you cannot run reasoning models on an 8-gigabyte laptop. 

The 7B model runs at 35 tokens per second, but its logic breaks on edge-case bug fixes. The 14B Q4 model is the sweet spot: 22 tokens per second on Apple Silicon, fitting inside 12 gigabytes of unified memory. 

If you try to push the 32B model without at least 32 gigs of RAM, your swap memory chokes, and generation speeds drop to 2 tokens per second. That is slower than typing by hand.

---

### [2:00 - 3:30] Beat 2: Live Code Generation Benchmark
**[ON SCREEN: Side-by-side terminal comparison: DeepSeek R1 local reasoning stream vs Claude 3.5 Sonnet on a real recursive tree parser bug]**

**Spoken:**
Now look at the actual code quality. We fed it a real production bug: a recursive AST parser that blew the stack on circular imports.

Watch the `<think>` reasoning block. Local DeepSeek spent 18 seconds thinking through the call stack before outputting a single line of code. It correctly implemented cycle detection using a memoized visited set. 

On single-file scripts and debugging, it matched GPT-4o with zero API costs and zero cloud calls.

---

### [3:30 - 4:45] Beat 3: The Catch (Where Local AI Fails)
**[ON SCREEN: Screen recording showing VS Code with 40-file repository context failing due to 8k context window limit and battery draining 30% in 45 mins]**

**Spoken:**
Now, here is the catch nobody talking about local AI wants to admit. 

First: context window. Local models start hallucinating once your repository context exceeds 8,000 tokens. It forgets files you gave it ten minutes ago.

Second: battery and thermal throttling. Running 14B reasoning on battery dropped a full charge from 100% to 20% in under two hours while the fans screamed at maximum RPM. Local AI is brilliant for sensitive code when plugged in at your desk, but it does not replace cloud models for massive codebases.

---

### [4:45 - 5:30] Payoff & Setup Guide
**[ON SCREEN: Clean terminal showing 3 commands: `brew install ollama`, `ollama run deepseek-r1:14b`, and setup config file]**

**Spoken:**
If you want to test this on your machine without spending a dime, here are the exact three terminal commands to run it locally in under five minutes.

The full benchmark logs, memory configurations, and setup commands are pinned in the description below.

Try it on your hardware, and see what token speed you get.
