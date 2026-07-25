"""
config.py - Configuration settings for the Weather Application.
Includes UI constants, color palettes, API endpoints, and default preferences.
"""

import os

# Application Info
APP_TITLE = "Atmosphere - Modern Weather Dashboard"
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 720

# Default User Preferences
DEFAULT_CITY = "London"
DEFAULT_UNITS = "metric"  # 'metric' (°C, km/h) or 'imperial' (°F, mph)

# Weather API Configurations (Open-Meteo REST API - Free, no key required)
OPEN_METEO_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Optional OpenWeatherMap API configuration
OWM_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OWM_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Design System - Slate Dark Glassmorphism Theme Palette
THEME = {
    "bg_dark": "#0f172a",          # Deep slate background
    "bg_card": "#1e293b",          # Slate card background
    "bg_card_hover": "#334155",    # Lighter card hover state
    "accent_blue": "#38bdf8",      # Sky blue accent
    "accent_purple": "#818cf8",    # Indigo accent
    "accent_cyan": "#22d3ee",      # Cyan highlight
    "text_primary": "#f8fafc",     # Bright white
    "text_secondary": "#94a3b8",   # Soft slate gray
    "text_muted": "#64748b",       # Muted gray
    "border": "#334155",           # Subtle border
    "success": "#4ade80",          # Soft green
    "warning": "#fbbf24",          # Warm amber
    "danger": "#f87171",           # Soft red
}

# Weather WMO Code Mappings to Descriptions and Icons
WMO_WEATHER_CODES = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Depositing Rime Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌦️"),
    55: ("Dense Drizzle", "🌧️"),
    56: ("Light Freezing Drizzle", "🌧️❄️"),
    57: ("Dense Freezing Drizzle", "🌧️❄️"),
    61: ("Slight Rain", "🌧️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️🌧️"),
    66: ("Light Freezing Rain", "🌧️❄️"),
    67: ("Heavy Freezing Rain", "🌧️❄️"),
    71: ("Slight Snowfall", "🌨️"),
    73: ("Moderate Snowfall", "🌨️"),
    75: ("Heavy Snowfall", "❄️❄️"),
    77: ("Snow Grains", "❄️"),
    80: ("Slight Rain Showers", "🌦️"),
    81: ("Moderate Rain Showers", "🌧️"),
    82: ("Violent Rain Showers", "⛈️"),
    85: ("Slight Snow Showers", "🌨️"),
    86: ("Heavy Snow Showers", "❄️"),
    95: ("Thunderstorm", "🌩️"),
    96: ("Thunderstorm with Hail", "⛈️"),
    99: ("Heavy Thunderstorm", "⛈️❄️"),
}
