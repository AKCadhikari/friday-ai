"""
friday/tools/web.py – Web, news, and search tools
"""
import httpx
from friday.config import NEWSAPI_KEY


async def _get(url: str, **params) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()


async def search_web(query: str) -> str:
    """Search the web using DuckDuckGo Instant Answers for a query."""
    try:
        data = await _get(
            "https://api.duckduckgo.com/",
            q=query,
            format="json",
            no_redirect=1,
            no_html=1,
        )
        abstract = data.get("Abstract", "")
        related  = [r.get("Text", "") for r in data.get("RelatedTopics", [])[:3] if "Text" in r]
        if abstract:
            return f"{abstract}\n\nRelated: {'; '.join(related)}" if related else abstract
        if related:
            return "Related results:\n" + "\n".join(related)
        return f"No instant answer found for '{query}'. Try a more specific query."
    except Exception as e:
        return f"Web search error: {e}"


async def fetch_url(url: str) -> str:
    """Fetch plain text content from a URL."""
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            r = await client.get(url, headers={"User-Agent": "FridayAI/2.0"})
            r.raise_for_status()
            # strip HTML tags minimally
            import re
            text = re.sub(r"<[^>]+>", " ", r.text)
            text = re.sub(r"\s+", " ", text).strip()
            return text[:3000]
    except Exception as e:
        return f"Fetch error: {e}"


async def get_world_news(category: str = "general", country: str = "us") -> str:
    """
    Get top world headlines.
    category: general | technology | science | health | business | entertainment | sports
    country:  us | gb | in | au | ca
    """
    if not NEWSAPI_KEY:
        return "NewsAPI key not configured. Add NEWSAPI_KEY to your .env file (free at newsapi.org)."
    try:
        data = await _get(
            "https://newsapi.org/v2/top-headlines",
            apiKey=NEWSAPI_KEY,
            category=category,
            country=country,
            pageSize=5,
        )
        articles = data.get("articles", [])
        if not articles:
            return "No headlines found."
        lines = [f"{i+1}. {a['title']} — {a.get('source', {}).get('name', '')}"
                 for i, a in enumerate(articles)]
        return "\n".join(lines)
    except Exception as e:
        return f"News fetch error: {e}"


async def get_tech_news() -> str:
    """Get the latest technology news headlines — great for staying up to date, Boss."""
    return await get_world_news(category="technology")


async def get_weather(city: str) -> str:
    """Get current weather for a city using the Open-Meteo geocoding + weather API (no key needed)."""
    try:
        geo = await _get(
            "https://geocoding-api.open-meteo.com/v1/search",
            name=city, count=1, language="en", format="json"
        )
        results = geo.get("results")
        if not results:
            return f"City '{city}' not found."
        loc = results[0]
        lat, lon = loc["latitude"], loc["longitude"]
        weather = await _get(
            "https://api.open-meteo.com/v1/forecast",
            latitude=lat, longitude=lon,
            current="temperature_2m,windspeed_10m,weathercode",
            timezone="auto"
        )
        cur = weather["current"]
        code_map = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 51: "Light drizzle", 61: "Light rain", 71: "Light snow",
            80: "Rain showers", 95: "Thunderstorm"
        }
        wcode = cur.get("weathercode", 0)
        desc  = code_map.get(wcode, f"Code {wcode}")
        temp  = cur.get("temperature_2m")
        wind  = cur.get("windspeed_10m")
        return (f"Weather in {loc['name']}, {loc.get('country', '')}: "
                f"{desc}, {temp}°C, wind {wind} km/h")
    except Exception as e:
        return f"Weather error: {e}"


async def lookup_wikipedia(topic: str) -> str:
    """Look up a topic on Wikipedia and return a concise summary."""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json()
                return data.get("extract", "No summary available.")
            return f"Wikipedia page not found for '{topic}'."
    except Exception as e:
        return f"Wikipedia error: {e}"
