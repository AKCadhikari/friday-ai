# 🔴 F.R.I.D.A.Y. Enhanced Edition v2.0
### *Your Personal Tony Stark AI Voice Assistant*

---

## What's New vs Original

| Feature | Original | Enhanced v2.0 |
|---|---|---|
| Web search | ✅ | ✅ |
| World news | ✅ | ✅ + Tech news category |
| System info | ✅ | ✅ + Battery + Processes |
| **Weather** | ❌ | ✅ Any city, no API key needed |
| **Wikipedia lookup** | ❌ | ✅ Instant research |
| **Math calculator** | ❌ | ✅ Full expression engine |
| **Unit conversion** | ❌ | ✅ km, kg, °C, feet, gallons |
| **Reminders** | ❌ | ✅ Session-based reminders |
| **Iron Man quotes** | ❌ | ✅ Random Stark quotes |
| **Jokes** | ❌ | ✅ Tech/science humor |
| **Suit diagnostic** | ❌ | ✅ Simulated HUD report |
| Configurable name | ❌ | ✅ Set your own BOSS_NAME |

---

## Step-by-Step Setup Guide

### STEP 1 — Prerequisites

Install these first:

**Python 3.11+**
```bash
# Check your version
python --version
# Should say Python 3.11.x or higher
```

**Install `uv` (fast Python package manager)**
```bash
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### STEP 2 — Clone & Install

```bash
# 1. Get the project
git clone https://github.com/AKCadhikari/friday-ai.git
cd friday-ai

# 2. Install all dependencies (creates a .venv automatically)
uv sync
```

---

### STEP 3 — Get Your API Keys

You need these accounts. All have free tiers:

#### 🔑 LiveKit (REQUIRED — for voice room)
1. Go to **https://cloud.livekit.io** → Sign up free
2. Create a new project
3. Copy your `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`

#### 🔑 Google Gemini (REQUIRED — the AI brain)
1. Go to **https://aistudio.google.com/app/apikey**
2. Click "Create API Key" → free tier is generous
3. Copy your `GOOGLE_API_KEY`

#### 🔑 OpenAI (REQUIRED — for the Friday voice)
1. Go to **https://platform.openai.com/api-keys**
2. Create a new API key
3. Copy your `OPENAI_API_KEY`
> The "nova" voice sounds closest to Friday from the MCU

#### 🔑 Sarvam (REQUIRED — for speech-to-text)
1. Go to **https://www.sarvam.ai** → Sign up
2. Get your `SARVAM_API_KEY` from the dashboard

#### 🔑 NewsAPI (OPTIONAL — for news headlines)
1. Go to **https://newsapi.org** → Free account
2. Copy your `NEWSAPI_KEY`
> Without this, news tools will tell you to add the key. Everything else still works.

---

### STEP 4 — Configure Your .env File

```bash
# Copy the example file
cp .env.example .env

# Open it in any text editor
nano .env       # Linux/Mac
notepad .env    # Windows
```

Fill in your keys:
```
LIVEKIT_URL=wss://your-project-xxxxx.livekit.cloud
LIVEKIT_API_KEY=APIxxxxxxxxxx
LIVEKIT_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx

GOOGLE_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxx
SARVAM_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
NEWSAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # optional

STT_PROVIDER=sarvam
LLM_PROVIDER=gemini
TTS_PROVIDER=openai

ASSISTANT_NAME=Friday
BOSS_NAME=Boss    # Change this to your name!
```

---

### STEP 5 — Run F.R.I.D.A.Y.

You need **two terminals open at the same time**:

**Terminal 1 — Start the MCP Tool Server:**
```bash
uv run friday
# You should see: 🔴 F.R.I.D.A.Y. MCP Server starting on 127.0.0.1:8000
```

**Terminal 2 — Start the Voice Agent:**
```bash
uv run friday_voice
# You should see: ✅ F.R.I.D.A.Y. is live and listening
```

---

### STEP 6 — Talk to F.R.I.D.A.Y.

1. Open **https://agents-playground.livekit.io** in your browser
2. Enter your LiveKit credentials (same URL, API key, secret from your .env)
3. Click **Connect**
4. **Start talking!** Friday will respond with her voice.

---

## What You Can Say to F.R.I.D.A.Y.

| Say this... | Friday will... |
|---|---|
| "Friday, what's the weather in Colombo?" | Get live weather |
| "What's the latest tech news?" | Read top tech headlines |
| "Run a suit diagnostic" | Simulate Iron Man HUD |
| "What's 144 squared divided by pi?" | Calculate it instantly |
| "Convert 100 km to miles" | Unit conversion |
| "Set a reminder for my meeting in 30 minutes" | Save a session reminder |
| "Look up quantum computing on Wikipedia" | Research summary |
| "Tell me a joke" | Tech/science humor |
| "Give me a Tony Stark quote" | Iron Man inspiration |
| "What's my battery status?" | System power check |
| "Run system diagnostics" | Full hardware report |
| "Search the web for SpaceX latest news" | Web search |

---

## Troubleshooting

**"Connection refused" on port 8000**
→ Make sure Terminal 1 (MCP server) is running first before Terminal 2.

**"Invalid API key" errors**
→ Double-check your `.env` file — no extra spaces around the `=` sign.

**No audio / can't hear Friday**
→ Check your browser microphone permissions. Use Chrome for best results.

**WSL users (Windows Subsystem for Linux)**
→ The MCP URL auto-resolves — but if issues occur, change `MCP_HOST` in `.env` to your WSL host IP (run `ip route | grep default` to find it).

**"Module not found" errors**
→ Make sure you ran `uv sync` inside the project folder.

---

## Adding More Tools

To add your own tools, create a function in `friday/tools/utils.py`:

```python
def my_new_tool(input: str) -> str:
    """Describe what this tool does — Friday will know when to use it."""
    return f"Result: {input}"
```

Then register it in `server.py`:
```python
from friday.tools.utils import my_new_tool
mcp.tool()(my_new_tool)
```

Restart both processes and Friday can now use your new tool!

---

*F.R.I.D.A.Y. Enhanced Edition — Built for people who want to feel like Tony Stark* 🔴
