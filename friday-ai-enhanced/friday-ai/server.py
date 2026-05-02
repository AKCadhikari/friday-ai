"""
server.py – F.R.I.D.A.Y. MCP Tool Server (Enhanced Edition)
Run with: uv run friday
"""
from fastmcp import FastMCP
from friday.config import MCP_HOST, MCP_PORT, BOSS_NAME

# ── Tool imports ────────────────────────────────────────────────────────────
from friday.tools.web import (
    search_web, fetch_url, get_world_news,
    get_tech_news, get_weather, lookup_wikipedia,
)
from friday.tools.system import (
    get_current_time, get_system_info,
    get_battery_status, get_running_processes,
)
from friday.tools.utils import (
    format_json, word_count, calculate,
    convert_units, set_reminder, list_reminders,
    countdown_timer, get_stark_quote, tell_joke,
    get_suit_status,
)

# ── Create MCP server ────────────────────────────────────────────────────────
mcp = FastMCP(
    name="friday-mcp",
    instructions=(
        f"You are F.R.I.D.A.Y., Tony Stark's AI assistant. "
        f"You call your user '{BOSS}'. "
        "Be concise, confident, and occasionally witty. "
        "You have access to web search, news, system info, weather, "
        "Wikipedia, math, unit conversion, reminders, and suit diagnostics."
    ),
)

# ── Register all tools ───────────────────────────────────────────────────────

# Web
mcp.tool()(search_web)
mcp.tool()(fetch_url)
mcp.tool()(get_world_news)
mcp.tool()(get_tech_news)
mcp.tool()(get_weather)
mcp.tool()(lookup_wikipedia)

# System
mcp.tool()(get_current_time)
mcp.tool()(get_system_info)
mcp.tool()(get_battery_status)
mcp.tool()(get_running_processes)

# Utilities
mcp.tool()(format_json)
mcp.tool()(word_count)
mcp.tool()(calculate)
mcp.tool()(convert_units)
mcp.tool()(set_reminder)
mcp.tool()(list_reminders)
mcp.tool()(countdown_timer)
mcp.tool()(get_stark_quote)
mcp.tool()(tell_joke)
mcp.tool()(get_suit_status)

# ── Resources ────────────────────────────────────────────────────────────────

@mcp.resource("friday://info")
def friday_info() -> str:
    return (
        "F.R.I.D.A.Y. Enhanced Edition v2.0\n"
        "Built on FastMCP + LiveKit Agents\n"
        "Tools: web search, news, weather, Wikipedia, system diagnostics, "
        "math, unit conversion, reminders, Iron Man suit status, jokes & quotes.\n"
        "Inspired by Tony Stark's AI assistant from the MCU."
    )

# ── Prompts ──────────────────────────────────────────────────────────────────

@mcp.prompt()
def summarize(text: str) -> str:
    return f"Summarize the following concisely for my Boss:\n\n{text}"

@mcp.prompt()
def explain_code(code: str) -> str:
    return f"Explain this code clearly in plain English:\n\n```\n{code}\n```"

@mcp.prompt()
def brainstorm(topic: str) -> str:
    return f"Brainstorm 5 creative ideas related to: {topic}"

# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    print(f"🔴 F.R.I.D.A.Y. MCP Server starting on {MCP_HOST}:{MCP_PORT} ...")
    mcp.run(transport="sse", host=MCP_HOST, port=MCP_PORT)

if __name__ == "__main__":
    main()
