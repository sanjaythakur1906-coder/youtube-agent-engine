# 🤖 GitHub Actions Daily Publishing Deployment (100% Free)

This guide walks you through automating your autonomous YouTube publishing engine using **GitHub Actions**.

### Why GitHub Actions?
- **100% Free**: 2,000 runner minutes/month (daily runs only use ~30 minutes/month).
- **No Credit Card Required**: Works out-of-the-box on your private GitHub repository.
- **Pre-installed FFmpeg**: Ubuntu-latest runner includes Python 3.11 and FFmpeg natively.
- **Automated Gating**: Generates video, sends review card to Telegram on your phone, waits for your 1-tap approval, and publishes directly to YouTube.

---

## Step 1: Add Secrets to GitHub

Open your GitHub repo in browser:
`https://github.com/sanjaythakur1906-coder/youtube-agent-engine/settings/secrets/actions`

Click **"New repository secret"** for each of the 3 secrets below:

### 1. Secret Name: `YOUTUBE_TOKEN_JSON`
- Value: The full JSON contents of your local `credentials/token.json` file:
```bash
cat credentials/token.json
```

### 2. Secret Name: `CLIENT_SECRETS_JSON`
- Value: The full JSON contents of your local `credentials/client_secrets.json` file:
```bash
cat credentials/client_secrets.json
```

### 3. Secret Name: `TELEGRAM_JSON`
- Value: The full JSON contents of your local `credentials/telegram.json` file:
```bash
cat credentials/telegram.json
```

---

## Step 2: Grant Workflow Write Permissions

GitHub Actions needs permission to commit updated video IDs to `output/history.json` so topics never repeat.

1. In your repo, go to **Settings &rarr; Actions &rarr; General**.
2. Scroll down to **"Workflow permissions"**.
3. Select **"Read and write permissions"**.
4. Check **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

---

## Step 3: Commit and Push the Workflow

Run the following commands in your local terminal:
```bash
git add .github/ docs/ tools/ requirements.txt
git commit -m "feat: add github actions autonomous publishing engine"
git push origin main
```

---

## Step 4: Test with 1-Click Trigger

1. Go to your repo on GitHub &rarr; click the **"Actions"** tab.
2. Under "All workflows", click **"Daily Autonomous YouTube Publishing Engine"**.
3. Click the **"Run workflow"** button on the right:
   - **Format**: Select `short` (Vertical 9:16) or `long` (1080p).
   - **Privacy**: Select `private`, `unlisted`, or `public`.
   - Click **Run workflow**.
4. Within 45-60 seconds, check your phone's Telegram:
   - Your bot `@my_notification_1906_bot` will send you the video and thumbnail with buttons:
     `[ ✅ Approve & Upload ]` `[ ❌ Reject ]`
5. Review and Take Action:
   - **Tap [ ✅ Approve & Upload ]**: Workflow uploads video directly to YouTube Studio and sends you live watch link!
   - **Tap [ ❌ Reject ]**: Bot asks what needs improvement:
     - `[ 🎣 Weak Hook / Script ]`
     - `[ 🎙️ Voice / Pacing ]`
     - `[ 🎨 Visuals / Code Snippets ]`
     - `[ ⏩ Dislike Topic Entirely ]`
     - `[ 💤 Done for Today ]`
   - **Choose Next Action**:
     - `[ 🛠️ Improve & Re-render Video ]`: Engine fixes the hook/voice/visuals based on your feedback and sends revised video in ~45s!
     - `[ 🔄 Pick Different Topic ]`: Archives rejected topic and generates a fresh topic from the bank.
     - `[ 💤 Done for Today ]`: Archives topic and finishes cleanly for today.

---

## Daily Schedule
The workflow runs automatically every day at **08:00 AM UTC** (**1:30 PM IST**). You can adjust the schedule in `.github/workflows/daily-publish.yml` under `cron`.
