# Smallest AI × Pipecat — Voice Demo

A fully interruptible real-time voice assistant running on [Pipecat](https://github.com/pipecat-ai/pipecat), powered entirely by Smallest AI for both speech-to-text and text-to-speech.

**Stack:**
- **STT**: Smallest AI Pulse (WebSocket, real-time)
- **LLM**: OpenAI GPT-4o
- **TTS**: Smallest AI Lightning v3.1 (`sophia` voice, WebSocket streaming)
- **Transport**: Daily WebRTC (in-browser, no app install needed)

---

## Prerequisites

- Python 3.10+
- A [Smallest AI](https://smallest.ai) API key
- An [OpenAI](https://platform.openai.com) API key
- A [Daily](https://dashboard.daily.co) API key (free tier works)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/harshitajain165/pipecat-demo-app.git
cd pipecat-demo-app
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> This installs Pipecat from the open PR branch that adds native Smallest AI support.
> Once [PR #4014](https://github.com/pipecat-ai/pipecat/pull/4014) merges, the install
> will simplify to `pip install pipecat-ai[smallest,daily,openai,silero]`.

### 4. Add your API keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
SMALLEST_API_KEY=...
OPENAI_API_KEY=...
DAILY_API_KEY=...
```

---

## Run

```bash
python bot.py
```

The bot will automatically create a Daily room and print a join URL:

```
============================================================
  Smallest AI x Pipecat — Voice Demo
============================================================

  Join URL:

    https://your-subdomain.daily.co/xxxxxxxx

  Open the URL above in your browser to talk to the bot.
  The bot uses Smallest AI for both STT and TTS.

  Press Ctrl+C to stop.
============================================================
```

Open the URL in any browser — no app or account needed. The bot will greet you and you can start talking. It's fully interruptible: speak while it's talking and it will stop immediately and respond to you.

---

## Notes

- The `sophia` voice is used by default. See [Smallest AI voices](https://smallest.ai) for alternatives.
- The STT service is in active development as part of the Pipecat integration. For best results, use English (`language=en`) and speak clearly.
- For questions or issues, open an issue in this repo or reach out on [Discord](https://discord.gg/Ub25S48hSf).
