"""
friday/tools/utils.py – Utility tools (jokes, math, unit conversion, reminders, etc.)
"""
import json
import math
import random
import datetime


# ── Formatting ──────────────────────────────────────────────────────────────

def format_json(data: str) -> str:
    """Pretty-print a JSON string."""
    try:
        return json.dumps(json.loads(data), indent=2)
    except Exception as e:
        return f"Invalid JSON: {e}"


def word_count(text: str) -> str:
    """Count words, characters, and sentences in a block of text."""
    words = len(text.split())
    chars = len(text)
    sentences = text.count(".") + text.count("!") + text.count("?")
    return f"Words: {words} | Characters: {chars} | Sentences: {sentences}"


# ── Iron Man Personality ─────────────────────────────────────────────────────

STARK_QUOTES = [
    "Sometimes you gotta run before you can walk.",
    "Genius, billionaire, playboy, philanthropist.",
    "Part of the journey is the end.",
    "I am Iron Man.",
    "The truth is… I am Iron Man.",
    "I've successfully privatized world peace.",
    "No amount of money ever bought a second of time.",
    "We're the Avengers — not the Alternatives.",
    "Proof that Tony Stark has a heart.",
    "I can do this all day. Actually, I prefer not to.",
]

def get_stark_quote() -> str:
    """Return a random Tony Stark / Iron Man quote to inspire the Boss."""
    return f'"{random.choice(STARK_QUOTES)}" — Tony Stark'


def tell_joke() -> str:
    """Tell a clever tech or science joke, Stark-style."""
    try:
        import pyjokes
        return pyjokes.get_joke(category="all")
    except Exception:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?'",
            "Why don't scientists trust atoms? Because they make up everything.",
        ]
        return random.choice(jokes)


# ── Math & Science ───────────────────────────────────────────────────────────

def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Supports: +, -, *, /, **, sqrt(), sin(), cos(), tan(), log(), pi, e
    Example: calculate("sqrt(144) + pi * 2")
    """
    try:
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        allowed_names["abs"] = abs
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Calculation error: {e}"


def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert between common units.
    Supported: km/miles, kg/lbs, celsius/fahrenheit, meters/feet, liters/gallons
    """
    conversions = {
        ("km", "miles"):        lambda v: v * 0.621371,
        ("miles", "km"):        lambda v: v * 1.60934,
        ("kg", "lbs"):          lambda v: v * 2.20462,
        ("lbs", "kg"):          lambda v: v * 0.453592,
        ("celsius", "fahrenheit"): lambda v: v * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5/9,
        ("meters", "feet"):     lambda v: v * 3.28084,
        ("feet", "meters"):     lambda v: v * 0.3048,
        ("liters", "gallons"):  lambda v: v * 0.264172,
        ("gallons", "liters"):  lambda v: v * 3.78541,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {result:.4f} {to_unit}"
    return f"Conversion from '{from_unit}' to '{to_unit}' is not supported yet."


# ── Productivity ─────────────────────────────────────────────────────────────

_reminders: list[dict] = []

def set_reminder(task: str, minutes_from_now: int = 30) -> str:
    """Set a reminder for a task (stored in memory for this session)."""
    due = datetime.datetime.now() + datetime.timedelta(minutes=minutes_from_now)
    _reminders.append({"task": task, "due": due.strftime("%I:%M %p")})
    return f"Reminder set: '{task}' at {due.strftime('%I:%M %p')}. I'll let you know, Boss."


def list_reminders() -> str:
    """List all active reminders for this session."""
    if not _reminders:
        return "No reminders set, Boss. Your schedule is clear."
    return "\n".join([f"• {r['task']} — at {r['due']}" for r in _reminders])


def countdown_timer(seconds: int) -> str:
    """Tell how long a countdown of N seconds is in human terms."""
    h, rem = divmod(seconds, 3600)
    m, s   = divmod(rem, 60)
    parts  = []
    if h: parts.append(f"{h} hour{'s' if h>1 else ''}")
    if m: parts.append(f"{m} minute{'s' if m>1 else ''}")
    if s: parts.append(f"{s} second{'s' if s>1 else ''}")
    return f"Timer for {' '.join(parts)} acknowledged, Boss."


# ── Iron Man Suit Status (fun simulation) ───────────────────────────────────

SUIT_MODELS = ["Mark L", "Mark LXXXV", "Mark XLVII", "Rescue Armor"]

def get_suit_status() -> str:
    """Run a simulated Stark suit diagnostic — just for the Iron Man feel."""
    suit  = random.choice(SUIT_MODELS)
    power = random.randint(85, 100)
    arc   = random.randint(90, 100)
    repul = random.randint(95, 100)
    thrus = random.randint(88, 100)
    return (
        f"🔴 {suit} Diagnostic Report\n"
        f"  Arc Reactor: {arc}% output\n"
        f"  Repulsor Array: {repul}% charge\n"
        f"  Thruster efficiency: {thrus}%\n"
        f"  Overall suit power: {power}%\n"
        f"  Status: All systems nominal. Ready for deployment, Boss."
    )
