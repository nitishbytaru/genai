import httpx
from datetime import datetime
from app.schemas import WeatherRequest

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
CURRENT_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}

def get_weather(location: str) -> dict :
    """Fetch current weather conditions for a city."""

    location = location.strip()

    if not location or len(location) > 100:
        return {"error":"Please Provide a valid location"}

    try:
        with httpx.Client(timeout=15.0) as client:
            # 1. Convert city name into co ordinates
            geo_response = client.get(
                GEOCODING_URL,
                params={
                    "name":location,
                    "count":1,
                    "language":"en",
                    "format":"json",
                },
            )
            geo_response.raise_for_status()

            places = geo_response.json().get("results",[])

            if not places:
                return {"error":f"No location found for '{location}'."}
            
            place = places[0]

            # 2. Fetch current conditions only
            weather_response = client.get(
                CURRENT_WEATHER_URL,
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "apparent_temperature,"
                        "wind_speed_10m,"
                        "weather_code"
                    ),
                    "timezone": "auto",
                    "forecast_days": 1,
                },
            )
            weather_response.raise_for_status()

            data = weather_response.json()
            current = data["current"]

            # 3. Validating the result with Pydentic
            result = WeatherRequest(
                location=place["name"],
                country=place.get("country"),
                temperature_c=current["temperature_2m"],
                feels_like_c=current["apparent_temperature"],
                humidity_percent=current["relative_humidity_2m"],
                wind_speed_kmh=current["wind_speed_10m"],
                condition=WEATHER_CODES.get(
                    current["weather_code"],
                    "Unknown conditions",
                ),
                timezone=data["timezone"],
                observed_at=datetime.fromisoformat(
                    current["time"]
                    ).strftime("%d %b %Y, %I:%M %p")
            )

            return result.model_dump()
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        return {
            "error":"Unable to fetch current weather right now"
        }