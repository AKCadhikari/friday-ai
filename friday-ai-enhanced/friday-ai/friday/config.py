"""
friday/config.py – Environment variable loading & app-wide settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY    = os.getenv("GOOGLE_API_KEY", "")
SARVAM_API_KEY    = os.getenv("SARVAM_API_KEY", "")
DEEPGRAM_API_KEY  = os.getenv("DEEPGRAM_API_KEY", "")
NEWSAPI_KEY       = os.getenv("NEWSAPI_KEY", "")

# --- LiveKit ---
LIVEKIT_URL        = os.getenv("LIVEKIT_URL", "")
LIVEKIT_API_KEY    = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")

# --- Provider Selection ---
STT_PROVIDER = os.getenv("STT_PROVIDER", "sarvam")   # sarvam | deepgram | groq
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")   # gemini | openai
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "openai")   # openai | sarvam

# --- Personality ---
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Friday")
BOSS_NAME      = os.getenv("BOSS_NAME", "Boss")

# --- MCP Server ---
MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
MCP_SSE_URL = f"http://{MCP_HOST}:{MCP_PORT}/sse"
