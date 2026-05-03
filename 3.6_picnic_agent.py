from datetime import date, datetime, timedelta
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen
import json

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()


WEATHER_CODE_DESCRIPTIONS = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


def _request_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    query = urlencode(params)
    with urlopen(f"{url}?{query}", timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def _resolve_date(day: str | None) -> str:
    if not day or day.lower() == "today":
        return date.today().isoformat()
    if day.lower() == "tomorrow":
        return (date.today() + timedelta(days=1)).isoformat()
    try:
        return datetime.strptime(day, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return date.today().isoformat()


def _geocode(location: str) -> dict[str, Any]:
    data = _request_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {"name": location, "count": 1, "language": "en", "format": "json"},
    )
    results = data.get("results") or []
    if not results:
        raise ValueError(f"Could not find weather coordinates for {location!r}.")
    return results[0]


def _weather_for(location: str, day: str | None) -> dict[str, Any]:
    resolved_day = _resolve_date(day)
    place = _geocode(location)
    forecast = _request_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                    "wind_speed_10m_max",
                ]
            ),
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
            "start_date": resolved_day,
            "end_date": resolved_day,
        },
    )
    daily = forecast["daily"]
    weather_code = daily["weather_code"][0]
    return {
        "location": ", ".join(
            part
            for part in [
                place.get("name"),
                place.get("admin1"),
                place.get("country"),
            ]
            if part
        ),
        "date": daily["time"][0],
        "condition": WEATHER_CODE_DESCRIPTIONS.get(weather_code, f"code {weather_code}"),
        "high_f": daily["temperature_2m_max"][0],
        "low_f": daily["temperature_2m_min"][0],
        "precipitation_probability": daily["precipitation_probability_max"][0],
        "wind_mph": daily["wind_speed_10m_max"][0],
    }


def _outdoor_score(weather: dict[str, Any]) -> tuple[int, list[str]]:
    score = 100
    reasons = []

    precip = weather["precipitation_probability"]
    high = weather["high_f"]
    low = weather["low_f"]
    wind = weather["wind_mph"]
    condition = weather["condition"]

    if precip >= 60:
        score -= 45
        reasons.append("rain is fairly likely")
    elif precip >= 35:
        score -= 25
        reasons.append("there is a meaningful chance of rain")
    elif precip >= 20:
        score -= 10
        reasons.append("there is a small chance of rain")

    if high >= 92:
        score -= 30
        reasons.append("the afternoon may be very hot")
    elif high >= 85:
        score -= 15
        reasons.append("it may feel warm in direct sun")

    if low <= 45:
        score -= 25
        reasons.append("cool temperatures could make sitting outside uncomfortable")
    elif low <= 55:
        score -= 10
        reasons.append("layers may be useful")

    if wind >= 25:
        score -= 25
        reasons.append("winds may make blankets and food hard to manage")
    elif wind >= 15:
        score -= 10
        reasons.append("it may be breezy")

    if "thunderstorm" in condition or "heavy" in condition:
        score -= 35
        reasons.append(f"the forecast includes {condition}")

    return max(0, min(score, 100)), reasons


@tool
def get_weather_forecast(location: str, day: str = "today") -> str:
    """Get the weather forecast for a location and day. The day may be today, tomorrow, or YYYY-MM-DD."""
    try:
        weather = _weather_for(location, day)
    except Exception as exc:
        return f"I could not fetch the forecast: {exc}"

    return (
        f"Forecast for {weather['location']} on {weather['date']}: "
        f"{weather['condition']}, high {weather['high_f']}F, low {weather['low_f']}F, "
        f"{weather['precipitation_probability']}% chance of precipitation, "
        f"max wind {weather['wind_mph']} mph."
    )


@tool
def plan_picnic_trip(
    location: str,
    day: str = "today",
    group_size: int = 2,
    preferences: str = "",
) -> str:
    """Create an indoor or outdoor picnic recommendation using the weather forecast."""
    try:
        weather = _weather_for(location, day)
    except Exception as exc:
        return f"I could not make a picnic plan because the forecast failed: {exc}"

    score, reasons = _outdoor_score(weather)
    go_outdoors = score >= 65
    venue_type = "outdoor picnic" if go_outdoors else "indoor picnic"
    reason_text = "; ".join(reasons) if reasons else "the weather looks comfortable"

    if go_outdoors:
        venue_ideas = [
            "a shaded park lawn with tables nearby",
            "a botanical garden or lakeside green space",
            "a quiet trailhead with a short scenic walk before eating",
        ]
        packing = [
            "blanket",
            "water",
            "sunscreen",
            "napkins",
            "trash bag",
            "simple finger foods",
        ]
    else:
        venue_ideas = [
            "a covered pavilion",
            "a museum cafe or conservatory with seating",
            "a cozy living-room floor picnic near a window",
        ]
        packing = [
            "easy snacks",
            "thermos drinks",
            "board game or cards",
            "portable speaker",
            "reusable plates",
        ]

    return (
        f"Recommended plan: {venue_type} for {group_size} people in {weather['location']} "
        f"on {weather['date']}.\n"
        f"Weather: {weather['condition']}, high {weather['high_f']}F, low {weather['low_f']}F, "
        f"{weather['precipitation_probability']}% precipitation chance, wind up to {weather['wind_mph']} mph.\n"
        f"Why: outdoor score {score}/100 because {reason_text}.\n"
        f"Venue ideas: {', '.join(venue_ideas)}.\n"
        f"Packing list: {', '.join(packing)}.\n"
        f"Preferences to account for: {preferences or 'none provided'}."
    )


PICNIC_SYSTEM_PROMPT = """
You are a weather-aware picnic planner. Help the user decide whether an outdoor
or indoor picnic is better, explain the weather tradeoffs plainly, and produce a
practical itinerary with timing, location style, food ideas, packing list, and a
backup plan. Always call the weather or picnic planning tool when the user asks
about a real location or date. If the user does not provide a location, ask for it.
"""


agent = create_agent(
    "groq:llama-3.3-70b-versatile",
    tools=[get_weather_forecast, plan_picnic_trip],
    system_prompt=PICNIC_SYSTEM_PROMPT,
)
