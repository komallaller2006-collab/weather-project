"""
weather_engine.py - Weather Data Fetcher Engine module.
Handles network requests, geocoding resolution, Open-Meteo REST API data parsing,
and data modeling for current weather conditions and 7-day forecasts.
"""

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple
import config


@dataclass
class CurrentWeather:
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    pressure: float
    cloud_cover: int
    weather_code: int
    condition_text: str
    icon: str
    units: str
    timestamp: str


@dataclass
class ForecastDay:
    date_str: str
    day_name: str
    temp_max: float
    temp_min: float
    weather_code: int
    condition_text: str
    icon: str
    precipitation_prob: int


class WeatherService:
    """Service to fetch live weather data using Open-Meteo REST API."""

    def __init__(self):
        self.geo_url = config.OPEN_METEO_GEO_URL
        self.weather_url = config.OPEN_METEO_WEATHER_URL

    def _http_get(self, url: str) -> dict:
        """Executes HTTP GET request and returns JSON response."""
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AtmosphereWeatherApp/1.0 (Python Standard Library)"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = response.read().decode("utf-8")
                return json.loads(data)
            else:
                raise RuntimeError(f"HTTP Error {response.status}")

    def geocode_city(self, city_name: str) -> Tuple[float, float, str, str]:
        """Converts city name to (latitude, longitude, name, country)."""
        clean_city = city_name.strip()
        if not clean_city:
            raise ValueError("City name cannot be empty.")

        params = urllib.parse.urlencode({"name": clean_city, "count": 1, "language": "en", "format": "json"})
        full_url = f"{self.geo_url}?{params}"
        data = self._http_get(full_url)

        results = data.get("results")
        if not results:
            raise ValueError(f"City '{clean_city}' not found. Please verify the spelling.")

        first_match = results[0]
        lat = first_match["latitude"]
        lon = first_match["longitude"]
        name = first_match.get("name", clean_city)
        country = first_match.get("country", "")

        return lat, lon, name, country

    def fetch_weather(self, city_name: str, units: str = "metric") -> Tuple[CurrentWeather, List[ForecastDay]]:
        """
        Fetches current weather and 7-day forecast.
        units: 'metric' (°C, km/h) or 'imperial' (°F, mph)
        """
        lat, lon, formatted_name, country = self.geocode_city(city_name)

        temp_unit_param = "fahrenheit" if units == "imperial" else "celsius"
        wind_unit_param = "mph" if units == "imperial" else "kmh"

        params = urllib.parse.urlencode({
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,cloud_cover",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "temperature_unit": temp_unit_param,
            "wind_speed_unit": wind_unit_param,
            "timezone": "auto"
        })

        full_url = f"{self.weather_url}?{params}"
        raw_data = self._http_get(full_url)

        # Parse Current Weather
        curr = raw_data.get("current", {})
        wcode = curr.get("weather_code", 0)
        condition, icon = config.WMO_WEATHER_CODES.get(wcode, ("Unknown", "❓"))
        now_str = datetime.now().strftime("%I:%M %p, %a %b %d")

        current_weather = CurrentWeather(
            city=formatted_name,
            country=country,
            latitude=lat,
            longitude=lon,
            temperature=round(curr.get("temperature_2m", 0.0), 1),
            feels_like=round(curr.get("apparent_temperature", 0.0), 1),
            humidity=int(curr.get("relative_humidity_2m", 0)),
            wind_speed=round(curr.get("wind_speed_10m", 0.0), 1),
            pressure=round(curr.get("surface_pressure", 0.0), 1),
            cloud_cover=int(curr.get("cloud_cover", 0)),
            weather_code=wcode,
            condition_text=condition,
            icon=icon,
            units=units,
            timestamp=now_str
        )

        # Parse Daily Forecast
        daily = raw_data.get("daily", {})
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        wcodes = daily.get("weather_code", [])
        precip_probs = daily.get("precipitation_probability_max", [])

        forecast_list: List[ForecastDay] = []
        for i in range(min(len(dates), 7)):
            date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
            day_name = "Today" if i == 0 else date_obj.strftime("%a")
            d_wcode = wcodes[i] if i < len(wcodes) else 0
            d_cond, d_icon = config.WMO_WEATHER_CODES.get(d_wcode, ("Clear", "☀️"))

            forecast_list.append(ForecastDay(
                date_str=dates[i],
                day_name=day_name,
                temp_max=round(max_temps[i], 1) if i < len(max_temps) else 0.0,
                temp_min=round(min_temps[i], 1) if i < len(min_temps) else 0.0,
                weather_code=d_wcode,
                condition_text=d_cond,
                icon=d_icon,
                precipitation_prob=int(precip_probs[i]) if i < len(precip_probs) and precip_probs[i] is not None else 0
            ))

        return current_weather, forecast_list
