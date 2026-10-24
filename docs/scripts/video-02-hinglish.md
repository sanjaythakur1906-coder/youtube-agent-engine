# Video 2 Script (Hinglish): "Maine DeepSeek R1 Local Run Kiya 7 Din"

## Metadata
- **Voice:** Aman (Male Indian English / Conversational Tech)
- **Winning Hook:** "ChatGPT ko 20 dollar dene se pehle, ye dekh lo ki local AI 7 din me kahan fail hua."
- **Packaging:** Title `I Ran DeepSeek R1 Locally for 7 Days` | Thumb `ZERO CLOUD?`

---

## Spoken Hinglish Script with On-Screen Beats

### [0:00 - 0:15] The Hook
**[ON SCREEN: Terminal window running `ollama run deepseek-r1:14b` with thermal monitor showing 98°C and memory usage spiking at 15.8GB]**

**Spoken:**
ChatGPT ko 20 dollar dene se pehle, ye dekh lo ki local AI 7 din me kahan fail hua.

---

### [0:15 - 0:45] The Turn
**[ON SCREEN: Split view: Left showing Ollama local terminal with 0ms cloud latency; Right showing cloud cancellation screen]**

**Spoken:**
Har jagah log bol rahe hain ki local AI aate hi cloud subscriptions band ho jayengi. Zero API cost, poori data privacy, aur zero internet requirement. Maine DeepSeek R1 ko poore 7 din apne local machine par real coding tasks ke liye use kiya. Aaj main aapko practical benchmark dikhaunga ki ye kahan best hai aur kahan aapka laptop crash ho jayega.

---

### [0:45 - 2:00] Beat 1: The Hardware Reality (7B vs 14B vs 32B)
**[ON SCREEN: Terminal running `btop` showing RAM memory pressure and token-per-second benchmarks]**

**Spoken:**
Pehle hardware ka sach jaan lo. Aapko 5 lakh ka Nvidia GPU nahi chahiye, lekin 8GB RAM wale laptop par reasoning models chalana bhool jao.

7B model 35 tokens per second deta hai, lekin complex bugs me hallucinate karta hai. 14B model sabse solid sweet spot hai: 22 tokens per second deta hai aur 12GB RAM ke andar fit ho jaata hai.

Agar aap bina 32GB RAM ke 32B model run karoge, toh machine swap memory me phas jayegi aur speed 2 tokens per second par gir jayegi. Itna slow ki haath se code likhna tez hoga.

---

### [2:00 - 3:30] Beat 2: Live Code Generation Benchmark
**[ON SCREEN: Side-by-side terminal comparison: DeepSeek R1 local reasoning stream vs Claude 3.5 Sonnet on circular imports bug]**

**Spoken:**
Ab actual code quality dekhte hain. Humne isko ek real production bug diya: circular import par crash hone wala recursive AST parser.

Terminal me iska `<think>` reasoning block dekho. Isne code likhne se pehle 18 seconds tak call stack evaluate kiya. Aur visited set use karke cycle detection perfectly implement kiya.

Single-file coding aur debugging me isne GPT-4o ko match kar diya, wo bhi bina kisi cloud call ke.

---

### [3:30 - 4:45] Beat 3: The Catch (Where Local AI Fails)
**[ON SCREEN: Screen recording showing VS Code with 40-file repository context failing due to 8k context window limit and battery draining 30% in 45 mins]**

**Spoken:**
Ab aate hain us sach par jo koi nahi batata.

Pehla issue hai context window. Jaise hi aapka codebase 8,000 tokens se bada hota hai, model purani files bhoolne lagta hai.

Doosra issue hai battery aur heating. Battery par 14B model run karne se 2 ghante me laptop 100% se 20% par aa gaya aur fans full speed par chalu ho gaye. Agar desk par plugged-in ho toh ye tool game-saver hai, lekin badhe codebases ke liye cloud models ko fully replace nahi kar sakta.

---

### [4:45 - 5:30] Payoff & Setup Guide
**[ON SCREEN: Clean terminal showing 3 commands: `brew install ollama`, `ollama run deepseek-r1:14b`, and setup config file]**

**Spoken:**
Agar aapko apne laptop par ye test karna hai, toh description me setup commands pinned hain. Bas teen commands me offline setup ho jaata hai.

Isko apne machine par run karke dekho aur comment me batao ki aapko kitni token speed mili.
