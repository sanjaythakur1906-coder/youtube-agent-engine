# Channel Strategy & Workflow: The Solo AI Builder

## 1. Channel Identity
- **Niche:** Practical AI Agents, Local LLM Tooling, Real-World Automation.
- **Positioning:** "The antidote to AI hype." Real code, real terminal, real failures.
- **Audience:** Tech builders, developers, engineering students, indie hackers.
- **Voice Profile:** Defined in [docs/voice.md](file:///Users/devbox/Projects/youtube-agent-skill/docs/voice.md).

## 2. Content Engine Workflow
For every video:
1. **Hook Scoring (`skills/yt-script/hookscore.py`):**
   - Test 5 hook variants before recording. Must exceed 75 threshold.
2. **Packaging Validation (`skills/yt-package/title.py`):**
   - Title and Thumbnail tested as single unit.
   - Enforce distinct wording between Title and Thumbnail.
   - Title under 60 chars (desktop) and punchy in first 40 chars (mobile).
3. **Script Beats (`skills/yt-script`):**
   - Hook (0-15s) -> Proof/Tension (15-45s) -> Core Build / Experiment (45s-7m) -> The Catch / Honest Verdict (7m-9m).
4. **Edit Decision List (`skills/yt-edit/deadair.py`):**
   - Process audio transcript to eliminate filler words, long pauses, and dead takes.

## 3. Video 1: Validated Package & Hook

### Title & Thumbnail Linter Result
* **Title:** `11 AI Agents Ran My Entire Channel` (34 chars)
* **Thumbnail Text:** `ZERO HUMANS?`
* **Score:** **100/100** (`skills/yt-package/title.py`)
  - No mobile cutoff issues.
  - Carries concrete number (11).
  - Title and thumbnail have 0 repeated words.

### Hook Score Result
* **Hook:** `"Before you let 11 AI agents run your channel, look at what broke in 7 days."`
* **Score:** **74 / 100 - STRONG** (`skills/yt-script/hookscore.py`)
  - Formula: The Warning
  - Specificity: 79/100
  - Address (Speaks directly to "you"): 96/100
  - Stakes: 88/100
  - Brevity: 100/100

### Full Production Script
* Spoken lines and visual cues: [docs/scripts/video-01-script.md](file:///Users/devbox/Projects/youtube-agent-skill/docs/scripts/video-01-script.md)
* Estimated Runtime: ~6.5 minutes.
* Status: **SHIPPED / READY TO RECORD**

### SEO, Description & Timestamps
* Full description, tags, and chapter markers: [docs/scripts/video-01-seo.md](file:///Users/devbox/Projects/youtube-agent-skill/docs/scripts/video-01-seo.md)

---

## 4. Video 2: Validated Package & Hook

### Title & Thumbnail Linter Result
* **Title:** `I Ran DeepSeek R1 Locally for 7 Days` (36 chars)
* **Thumbnail Text:** `ZERO CLOUD?`
* **Score:** **100/100** (`skills/yt-package/title.py`)
  - No mobile cutoff issues.
  - Carries concrete figures (1, 7).
  - Title and thumbnail have 0 repeated words.

### Hook Score Result
* **Hook:** `"Before you pay 20 dollars for ChatGPT, look at what broke running local AI for 7 days."`
* **Score:** **73 / 100 - STRONG** (`skills/yt-script/hookscore.py`)
  - Formula: I Tried It
  - Specificity: 90/100
  - Address: 76/100
  - Stakes: 88/100
  - Brevity: 100/100

### Production Scripts & SEO
* English Script: [docs/scripts/video-02-script.md](file:///Users/devbox/Projects/youtube-agent-skill/docs/scripts/video-02-script.md)
* Hinglish Script (Aman voice): [docs/scripts/video-02-hinglish.md](file:///Users/devbox/Projects/youtube-agent-skill/docs/scripts/video-02-hinglish.md)
* SEO Metadata & Timestamps: [docs/scripts/video-02-seo.md](file:///Users/devbox/Projects/youtube-agent-skill/docs/scripts/video-02-seo.md)

