from pydantic import BaseModel, Field

class WeatherRequest(BaseModel):
    location: str
    country: str | None = None
    temperature_c: float
    feels_like_c: float
    humidity_percent: int
    wind_speed_kmh: float
    condition: str
    timezone: str
    observed_at: str