"""
agent_friday.py - F.R.I.D.A.Y. LiveKit Voice Agent (Enhanced Edition)
Run with: uv run friday_voice
"""
import logging
import os

from dotenv import load_dotenv
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.agents import cli, WorkerOptions
from livekit.agents import MCPServerHTTP

load_dotenv()

from friday.config import (
    STT_PROVIDER, LLM_PROVIDER, TTS_PROVIDER,
    BOSS_NAME, ASSISTANT_NAME, MCP_SSE_URL,
    OPENAI_API_KEY, GOOGLE_API_KEY, SARVAM_API_KEY,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Build STT ────────────────────────────────────────────────────────────────
def _build_stt():
    if STT_PROVIDER == "sarvam":
        from livekit.plugins.sarvam import STT
        return STT(api_key=SARVAM_API_KEY)
    elif STT_PROVIDER == "deepgram":
        from livekit.plugins.deepgram import STT
        return STT()
    else:
        from livekit.plugins.openai import STT
        return STT(api_key=OPENAI_API_KEY)


# ── Build LLM ────────────────────────────────────────────────────────────────
def _build_llm():
    if LLM_PROVIDER == "gemini":
        from livekit.plugins.google import LLM
        return LLM(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)
    else:
        from livekit.plugins.openai import LLM
        return LLM(model="gpt-4o", api_key=OPENAI_API_KEY)


# ── Build TTS ────────────────────────────────────────────────────────────────
def _build_tts():
    if TTS_PROVIDER == "openai":
        from livekit.plugins.openai import TTS
        # "nova" voice is closest to Friday's tone — calm, confident, female AI
        return TTS(voice="nova", api_key=OPENAI_API_KEY)
    elif TTS_PROVIDER == "sarvam":
        from livekit.plugins.sarvam import TTS
        return TTS(api_key=SARVAM_API_KEY)
    else:
        from livekit.plugins.openai import TTS
        return TTS(voice="nova", api_key=OPENAI_API_KEY)


# ── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""
You are F.R.I.D.A.Y. (Female Replacement Intelligent Digital Assistant Youth),
the AI assistant to Tony Stark — or in this case, {BOSS_NAME}.

## Personality
- Address the user as "{BOSS_NAME}" always.
- You are intelligent, calm, slightly witty, and laser-focused on being helpful.
- You speak like a real AI assistant — concise, smart, no fluff.
- Occasionally use phrases like "Understood, {BOSS_NAME}", "Right away", "On it."
- You can be playful when asked for jokes or quotes, but professional otherwise.

## Capabilities
You have access to these tools via MCP. Use them proactively:
- **search_web** – search the internet
- **get_world_news / get_tech_news** – latest headlines
- **get_weather** – real-time weather for any city
- **lookup_wikipedia** – factual research
- **get_current_time** – time in any timezone
- **get_system_info / get_battery_status / get_running_processes** – diagnostics
- **calculate** – math expressions (sqrt, sin, pi, etc.)
- **convert_units** – km↔miles, kg↔lbs, °C↔°F, etc.
- **set_reminder / list_reminders** – session reminders
- **get_stark_quote** – Iron Man inspiration
- **tell_joke** – humor when needed
- **get_suit_status** – simulate an Iron Man suit diagnostic

## Voice Rules
- Keep responses SHORT for voice — 1-3 sentences unless detail is requested.
- Never read out URLs or raw JSON.
- When summarizing news or weather, read it naturally like a human assistant.
- Start the session with: "F.R.I.D.A.Y. online. How can I help you, {BOSS_NAME}?"
"""


# ── Agent Definition ─────────────────────────────────────────────────────────
async def create_agent_session() -> tuple[AgentSession, Agent]:
    mcp_server = MCPServerHTTP(url=MCP_SSE_URL)

    session = AgentSession(
        stt=_build_stt(),
        llm=_build_llm(),
        tts=_build_tts(),
    )

    agent = Agent(
        instructions=SYSTEM_PROMPT,
        mcp_servers=[mcp_server],
    )

    return session, agent


async def entrypoint(ctx):
    logger.info(f"🔴 {ASSISTANT_NAME} voice agent connecting to room: {ctx.room.name}")
    session, agent = await create_agent_session()
    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(),
    )
    logger.info(f"✅ {ASSISTANT_NAME} is live and listening.")


# ── Entry Points ─────────────────────────────────────────────────────────────
def dev():
    """Dev mode — wraps the CLI so `uv run friday_voice` works."""
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint),
    )

if __name__ == "__main__":
    dev()
