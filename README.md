# Smallest AI × Pipecat — Voice Demo

A fully interruptible real-time voice assistant running on [Pipecat](https://github.com/pipecat-ai/pipecat), powered entirely by Smallest AI for both speech-to-text and text-to-speech.

**Stack:**
- **STT**: Smallest AI Pulse (WebSocket, real-time)
- **LLM**: OpenAI GPT-4o
- **TTS**: Smallest AI Lightning v3.1 (`sophia` voice, WebSocket streaming)
- **Transport**: Daily WebRTC (in-browser, no app install needed)

---

## Prerequisites

- Python **3.10 or 3.11** (3.9 and below will not work — some dependencies require 3.10+)
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

> **Important:** All subsequent commands must be run from inside the `pipecat-demo-app` directory. If you run them from a different folder, the `.env` file and `requirements.txt` won't be found.

### 2. Check your Python version

```bash
python3 --version
```

If the output shows Python 3.9 or below, install a newer version first:

```bash
brew install python@3.11
```

### 3. Create a virtual environment

Use `python3.11` (or `python3.10`) explicitly to ensure the correct version is used:

```bash
python3.11 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

You can confirm the venv is active when you see `(venv)` at the start of your terminal prompt.

### 4. Upgrade pip and install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> This installs Pipecat from the open PR branch that adds native Smallest AI support.
> Once [PR #4014](https://github.com/pipecat-ai/pipecat/pull/4014) merges, the install
> will simplify to `pip install pipecat-ai[smallest,daily,openai,silero]`.

### 5. Add your API keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
SMALLEST_API_KEY=...
OPENAI_API_KEY=...
DAILY_API_KEY=...
```

**Where to find each key:**
- **Smallest AI** — [https://smallest.ai](https://smallest.ai) → Dashboard → API Keys
- **OpenAI** — [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Daily** — [https://dashboard.daily.co/developers](https://dashboard.daily.co/developers) → copy the **API Key** field

> **Note:** Do not commit your `.env` file or share your API keys publicly.

---

## Run

Make sure your virtual environment is active (`(venv)` in your prompt) and you are inside the `pipecat-demo-app` directory, then run:

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

## Experimenting with voices and languages

You can pass flags when starting the bot to change the voice or language — no code changes needed.

```bash
python bot.py --voice sophia --language en
python bot.py --language hi                  # Hindi
python bot.py --language de                  # German
python bot.py --voice sophia --language fr   # French with sophia voice
```

### Available flags

| Flag | Default | Description |
|------|---------|-------------|
| `--voice` | `sophia` | TTS voice ID |
| `--language` | `en` | Language code for both STT and TTS |

### Supported languages

| Code | Language |
|------|----------|
| `en` | English |
| `hi` | Hindi |
| `de` | German |
| `fr` | French |
| `es` | Spanish |
| `it` | Italian |
| `pt` | Portuguese |
| `ru` | Russian |
| `ar` | Arabic |
| `ta` | Tamil |
| `te` | Telugu |
| `bn` | Bengali |
| `gu` | Gujarati |
| `mr` | Marathi |
| `nl` | Dutch |
| `pl` | Polish |

> STT and TTS use the same `--language` value. Not all languages are available for both — if a language works for STT but not TTS (or vice versa), the service will fall back to its default.

---

## Notes

- The `sophia` voice is used by default. See [Smallest AI voices](https://smallest.ai) for alternatives.
- The STT service is in active development as part of the Pipecat integration. For best results, use English (`language=en`) and speak clearly.
