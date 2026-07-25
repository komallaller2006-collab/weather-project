"""
gui.py - Graphical User Interface for the Weather Application.
Built with Tkinter featuring a modern dark glassmorphic design system,
smooth async data fetching, unit switching, metric cards, and 7-day forecast.
"""

import threading
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional
import config
from weather_engine import WeatherService, CurrentWeather, ForecastDay  


class ModernCard(tk.Frame):
    """Custom styled card container frame with border and dark background."""

    def __init__(self, parent, bg=config.THEME["bg_card"], border_color=config.THEME["border"], **kwargs):
        super().__init__(parent, bg=border_color, padx=1, pady=1, **kwargs)
        self.inner = tk.Frame(self, bg=bg)
        self.inner.pack(fill="both", expand=True)


class WeatherAppGUI(tk.Tk):
    """Main Application Window for Atmosphere Weather App."""


    def __init__(self):
        super().__init__()

        self.title(config.APP_TITLE)
        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.minsize(850, 650)
        self.configure(bg=config.THEME["bg_dark"])

        # State Variables
        self.weather_service = WeatherService()
        self.current_city = config.DEFAULT_CITY
        self.current_units = config.DEFAULT_UNITS  # 'metric' or 'imperial'
        self.is_loading = False

        # Build Interface
        self._init_styles()
        self._build_ui()

        # Initial Load
        self.refresh_weather()

    def _init_styles(self):
        """Configure TTK widget styles."""
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Entry Style
        self.style.configure(
            "Custom.TEntry",
            fieldbackground=config.THEME["bg_card"],
            foreground=config.THEME["text_primary"],
            bordercolor=config.THEME["border"],
            lightcolor=config.THEME["accent_blue"],
            darkcolor=config.THEME["border"],
            padding=8
        )

    def _build_ui(self):
        """Constructs main layout sections."""
        # Container with padding
        self.main_container = tk.Frame(self, bg=config.THEME["bg_dark"], padx=25, pady=20)
        self.main_container.pack(fill="both", expand=True)

        self._build_header()
        self._build_current_weather_hero()
        self._build_metrics_grid()
        self._build_forecast_section()
        self._build_footer()

    def _build_header(self):
        """Header with app title, search entry, unit toggle, and refresh button."""
        header_frame = tk.Frame(self.main_container, bg=config.THEME["bg_dark"])
        header_frame.pack(fill="x", pady=(0, 20))

        # Title & Subtitle
        title_box = tk.Frame(header_frame, bg=config.THEME["bg_dark"])
        title_box.pack(side="left")

        app_label = tk.Label(
            title_box,
            text="⚡ ATMOSPHERE",
            font=("Segoe UI", 16, "bold"),
            fg=config.THEME["accent_blue"],
            bg=config.THEME["bg_dark"]
        )
        app_label.pack(anchor="w")

        # Search Bar Box
        search_box = tk.Frame(header_frame, bg=config.THEME["bg_dark"])
        search_box.pack(side="right")

        self.search_var = tk.StringVar(value=config.DEFAULT_CITY)
        self.search_entry = tk.Entry(
            search_box,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg=config.THEME["bg_card"],
            fg=config.THEME["text_primary"],
            insertbackground=config.THEME["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=config.THEME["border"],
            highlightcolor=config.THEME["accent_blue"],
            width=20
        )
        self.search_entry.pack(side="left", ipady=6, ipadx=10, padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        # Search Button
        self.search_btn = tk.Button(
            search_box,
            text="🔍 Search",
            font=("Segoe UI", 10, "bold"),
            bg=config.THEME["accent_blue"],
            fg="#0f172a",
            activebackground=config.THEME["accent_cyan"],
            activeforeground="#0f172a",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.on_search
        )
        self.search_btn.pack(side="left", padx=(0, 8))

        # Unit Switcher Button
        self.unit_btn = tk.Button(
            search_box,
            text="°C",
            font=("Segoe UI", 10, "bold"),
            bg=config.THEME["bg_card"],
            fg=config.THEME["accent_cyan"],
            activebackground=config.THEME["bg_card_hover"],
            activeforeground=config.THEME["text_primary"],
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground=config.THEME["border"],
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.toggle_units
        )
        self.unit_btn.pack(side="left")

    def _build_current_weather_hero(self):
        """Hero card presenting primary temperature and condition details."""
        card = ModernCard(self.main_container)
        card.pack(fill="x", pady=(0, 20))

        hero_frame = card.inner
        hero_frame.configure(padx=24, pady=20)

        # Left Column: Location & Main Temp
        left_col = tk.Frame(hero_frame, bg=config.THEME["bg_card"])
        left_col.pack(side="left", anchor="w")

        self.city_label = tk.Label(
            left_col,
            text="Loading...",
            font=("Segoe UI", 24, "bold"),
            fg=config.THEME["text_primary"],
            bg=config.THEME["bg_card"]
        )
        self.city_label.pack(anchor="w")

        self.condition_label = tk.Label(
            left_col,
            text="Fetching weather data...",
            font=("Segoe UI", 12),
            fg=config.THEME["text_secondary"],
            bg=config.THEME["bg_card"]
        )
        self.condition_label.pack(anchor="w", pady=(2, 10))

        temp_row = tk.Frame(left_col, bg=config.THEME["bg_card"])
        temp_row.pack(anchor="w")

        self.temp_label = tk.Label(
            temp_row,
            text="--°",
            font=("Segoe UI", 48, "bold"),
            fg=config.THEME["text_primary"],
            bg=config.THEME["bg_card"]
        )
        self.temp_label.pack(side="left")

        self.icon_label = tk.Label(
            temp_row,
            text="🌤️",
            font=("Segoe UI Emoji", 42),
            bg=config.THEME["bg_card"],
            fg=config.THEME["text_primary"]
        )
        self.icon_label.pack(side="left", padx=(15, 0))

        # Right Column: Sub-metrics (Feels Like, Last Updated)
        right_col = tk.Frame(hero_frame, bg=config.THEME["bg_card"])
        right_col.pack(side="right", anchor="e")

        self.feels_label = tk.Label(
            right_col,
            text="Feels like: --°",
            font=("Segoe UI", 13, "bold"),
            fg=config.THEME["accent_purple"],
            bg=config.THEME["bg_card"]
        )
        self.feels_label.pack(anchor="e")

        self.updated_label = tk.Label(
            right_col,
            text="Updated: --",
            font=("Segoe UI", 10),
            fg=config.THEME["text_muted"],
            bg=config.THEME["bg_card"]
        )
        self.updated_label.pack(anchor="e", pady=(6, 0))

    def _build_metrics_grid(self):
        """Grid of 4 key telemetry cards (Humidity, Wind, Pressure, Clouds)."""
        grid_frame = tk.Frame(self.main_container, bg=config.THEME["bg_dark"])
        grid_frame.pack(fill="x", pady=(0, 20))
        grid_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="metric_cols")

        self.metric_cards = {}
        metrics_def = [
            ("humidity", "💧 Humidity", "-- %"),
            ("wind", "💨 Wind Speed", "-- km/h"),
            ("pressure", "⏲️ Pressure", "-- hPa"),
            ("clouds", "☁️ Cloud Cover", "-- %"),
        ]

        for idx, (key, title, default_val) in enumerate(metrics_def):
            card = ModernCard(grid_frame)
            card.grid(row=0, column=idx, sticky="nsew", padx=4 if idx not in (0, 3) else 0)

            box = card.inner
            box.configure(padx=16, pady=14)

            title_lbl = tk.Label(
                box, text=title, font=("Segoe UI", 10), fg=config.THEME["text_secondary"], bg=config.THEME["bg_card"]
            )
            title_lbl.pack(anchor="w")

            val_lbl = tk.Label(
                box, text=default_val, font=("Segoe UI", 15, "bold"), fg=config.THEME["text_primary"], bg=config.THEME["bg_card"]
            )
            val_lbl.pack(anchor="w", pady=(4, 0))

            self.metric_cards[key] = val_lbl

    def _build_forecast_section(self):
        """Section header and horizontal row for 7-day forecast cards."""
        sec_title = tk.Label(
            self.main_container,
            text="7-DAY FORECAST",
            font=("Segoe UI", 11, "bold"),
            fg=config.THEME["text_secondary"],
            bg=config.THEME["bg_dark"]
        )
        sec_title.pack(anchor="w", pady=(0, 10))

        self.forecast_row = tk.Frame(self.main_container, bg=config.THEME["bg_dark"])
        self.forecast_row.pack(fill="x")
        self.forecast_row.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="fore_cols")

        self.forecast_widgets = []
        for i in range(7):
            card = ModernCard(self.forecast_row)
            card.grid(row=0, column=i, sticky="nsew", padx=3)

            box = card.inner
            box.configure(padx=8, pady=12)

            day_lbl = tk.Label(box, text="--", font=("Segoe UI", 10, "bold"), fg=config.THEME["accent_blue"], bg=config.THEME["bg_card"])
            day_lbl.pack()

            icon_lbl = tk.Label(box, text="☀️", font=("Segoe UI Emoji", 20), bg=config.THEME["bg_card"])
            icon_lbl.pack(pady=4)

            cond_lbl = tk.Label(box, text="--", font=("Segoe UI", 8), fg=config.THEME["text_muted"], bg=config.THEME["bg_card"])
            cond_lbl.pack()

            temp_lbl = tk.Label(box, text="--° / --°", font=("Segoe UI", 9, "bold"), fg=config.THEME["text_primary"], bg=config.THEME["bg_card"])
            temp_lbl.pack(pady=(4, 0))

            self.forecast_widgets.append({
                "day": day_lbl,
                "icon": icon_lbl,
                "cond": cond_lbl,
                "temp": temp_lbl
            })

    def _build_footer(self):
        """Footer status bar."""
        self.status_bar = tk.Label(
            self.main_container,
            text="Powered by Open-Meteo REST API • Real-time Data",
            font=("Segoe UI", 9),
            fg=config.THEME["text_muted"],
            bg=config.THEME["bg_dark"]
        )
        self.status_bar.pack(side="bottom", pady=(15, 0))

    def on_search(self):
        """Triggered when user submits city search."""
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a valid city name.")
            return

        self.current_city = query
        self.refresh_weather()

    def toggle_units(self):
        """Switches between metric (°C) and imperial (°F)."""
        if self.current_units == "metric":
            self.current_units = "imperial"
            self.unit_btn.config(text="°F")
        else:
            self.current_units = "metric"
            self.unit_btn.config(text="°C")

        self.refresh_weather()

    def refresh_weather(self):
        """Starts asynchronous thread to fetch weather data without freezing GUI."""
        if self.is_loading:
            return

        self.is_loading = True
        self.status_bar.config(text=f"Fetching latest weather for '{self.current_city}'...", fg=config.THEME["accent_cyan"])
        self.search_btn.config(state="disabled")

        threading.Thread(target=self._async_fetch, daemon=True).start()

    def _async_fetch(self):
        """Worker thread logic."""
        try:
            current, forecast = self.weather_service.fetch_weather(
                self.current_city, units=self.current_units
            )
            # Schedule UI update on main thread
            self.after(0, self._update_ui, current, forecast, None)
        except Exception as err:
            self.after(0, self._update_ui, None, None, str(err))

    def _update_ui(self, current: Optional[CurrentWeather], forecast: Optional[list[ForecastDay]], error_msg: Optional[str]):
        """Main thread callback to update visual elements."""
        self.is_loading = False
        self.search_btn.config(state="normal")

        if error_msg:
            self.status_bar.config(text=f"Error: {error_msg}", fg=config.THEME["danger"])
            messagebox.showerror("Weather Error", error_msg)
            return

        unit_symbol = "°C" if current.units == "metric" else "°F"
        speed_symbol = "km/h" if current.units == "metric" else "mph"

        # Update Hero Section
        country_str = f", {current.country}" if current.country else ""
        self.city_label.config(text=f"{current.city}{country_str}")
        self.condition_label.config(text=f"{current.condition_text}")
        self.temp_label.config(text=f"{current.temperature}{unit_symbol}")
        self.icon_label.config(text=current.icon)
        self.feels_label.config(text=f"Feels like: {current.feels_like}{unit_symbol}")
        self.updated_label.config(text=f"Updated: {current.timestamp}")

        # Update Metrics Grid
        self.metric_cards["humidity"].config(text=f"{current.humidity} %")
        self.metric_cards["wind"].config(text=f"{current.wind_speed} {speed_symbol}")
        self.metric_cards["pressure"].config(text=f"{current.pressure} hPa")
        self.metric_cards["clouds"].config(text=f"{current.cloud_cover} %")

        # Update Forecast
        if forecast:
            for idx, fday in enumerate(forecast[:7]):
                w = self.forecast_widgets[idx]
                w["day"].config(text=fday.day_name)
                w["icon"].config(text=fday.icon)
                w["cond"].config(text=fday.condition_text[:10])
                w["temp"].config(text=f"{fday.temp_max}° / {fday.temp_min}°")

        self.status_bar.config(
            text=f"Live weather data for {current.city} updated successfully.",
            fg=config.THEME["success"]
        )


if __name__ == "__main__":
    app = WeatherAppGUI()
    app.mainloop()
