# Video 1 Script: "11 AI Agents Ran My Entire Channel"

## Top 2 Tested Hooks

### Hook 1 (Winner - 74/100 STRONG - Formula: The Warning)
> "Before you let 11 AI agents run your channel, look at what broke in 7 days."

### Hook 2 (Runner-up - 69/100 WORKABLE - Formula: The Mistake)
> "Stop writing YouTube hooks yourself until you see how this script scores your first 15 seconds."

---

## Spoken Script with On-Screen Beats

### [0:00 - 0:15] The Hook
**[ON SCREEN: Fast 3-second split cut showing terminal errors in red, then YouTube studio retention graph with a sharp cliff, then full-screen VS Code IDE]**

**Spoken:**
Before you let 11 AI agents run your channel, look at what broke in 7 days.

---

### [0:15 - 0:45] The Turn
**[ON SCREEN: Zoom into terminal in VS Code showing the repository directory `youtube-agent-skill` with 11 skill folders highlighted]**

**Spoken:**
I tested 11 open-source agent skills designed to handle scriptwriting, hook scoring, title packaging, and edit cuts—with zero manual intervention until publishing. Today, we're testing the core three in real time on this exact video, and I’m showing you where they save hours versus where they completely hallucinate.

---

### [0:45 - 2:00] Beat 1: The Title & Thumbnail Linter
**[ON SCREEN: Terminal window running `.venv/bin/python skills/yt-package/title.py --title "..." --thumb "..."` displaying output scores]**

**Spoken:**
Most creators write a title, then open Photoshop and slap the exact same words on the thumbnail. That wastes half your click surface. 

Watch this. The package tool runs a Python linter checking two specific rules: character truncation for mobile feeds under 40 characters, and duplicate words across the title and thumbnail. 

When I tested a generic title: *"How AI Built My Entire YouTube Channel"*, it flagged it for vague buzzwords. But when we changed it to: *"11 AI Agents Ran My Entire Channel"* with the thumbnail text *"ZERO HUMANS?"*—it scored a 100 out of 100. It forces you to make the thumbnail say what the title does not.

---

### [2:00 - 3:30] Beat 2: Algorithmic Hook Scoring
**[ON SCREEN: Terminal running `hookscore.py` showing 5-property breakdown: Specificity, Address, Stakes, Curiosity, Brevity]**

**Spoken:**
Next is `hookscore.py`. A lot of people think hooks are just gut feel. This script scores the first 15 seconds against 74 calibrated short-form transcripts across five parameters.

Look at the terminal. If I input: *"I gave AI full control of my channel and promised not to touch it"*, it scores a 41—marked WEAK. Why? Because the curiosity is dead and it doesn't speak to "you" in the first six words.

When we reframe it to: *"Before you let 11 AI agents run your channel, look at what broke in 7 days"*, the score jumps to 74 STRONG. It forces concrete figures and personal stakes before you waste a single take recording on camera.

---

### [3:30 - 5:00] Beat 3: Transcript to Edit Decision List (Dead Air Removal)
**[ON SCREEN: Raw audio waveform in timeline with long pauses, running `.venv/bin/python skills/yt-edit/deadair.py audio.srt` outputting timestamps to cut]**

**Spoken:**
Here is where most creators lose 5 hours every weekend: scrubbing through an audio file cutting out 'ums', retakes, and awkward pauses. 

Instead of doing that manually, the edit agent parses the raw `.srt` transcript. It calculates silence thresholds over 800 milliseconds and flags repetitive sentences where you restarted a thought. It outputs a cut list with exact timecodes that you drop straight into Premiere or DaVinci Resolve.

---

### [5:00 - 6:15] Beat 4: Where The Agents Failed (The Honest Catch)
**[ON SCREEN: Screen capture of raw AI-generated script containing robotic filler words like "dive into the game-changing realm"]**

**Spoken:**
Now, here is the catch. The agents cannot run your channel completely unattended. 

If you don't feed them a strict `voice.md` profile, they revert right back to generic AI sludge—phrases like *"let's dive in"* and *"game-changer"*. You still need human taste to kill the fluff, verify the numbers, and actually hit publish. The skills write. You upload.

---

### [6:15 - 7:00] Payoff & Close
**[ON SCREEN: GitHub repository link and terminal command `git clone ...` pinned in description]**

**Spoken:**
All 11 skills and the 6 standalone Python scripts are 100% free, MIT licensed, with no API keys or signups required. The GitHub link and setup instructions are in the description below.

Clone the repo, run the hook scorer on your next video, and see what it scores. 

---

## Production Metadata
- **Estimated Runtime:** ~6.5 minutes (~900 words spoken at 145 wpm).
- **Winning Formula:** The Warning (High Address + High Stakes).
- **Required Assets:** VS Code terminal recording, screen recording of `title.py` and `hookscore.py` execution, raw `.srt` cut list demonstration.

---
**Ship it, or change it?**
