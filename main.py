
"""
main.py - Entry point for Atmosphere Weather Application.
Handles system configuration (High DPI scaling on Windows), CLI argument handling,
and launches the main Tkinter GUI loop.
"""
import argparse
import sys
import os
# Ensure local workspace directory is in Python path for clean module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import gui
def configure_high_dpi():
    """Configures Windows OS High DPI scaling for crisp text & UI rendering."""
    if sys.platform == "win32":
        try:
            import ctypes
            # Set DPI awareness (2 = Per Monitor DPI Aware, 1 = System DPI Aware)
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def parse_arguments():
    """Parses command-line arguments if launched from terminal."""
    parser = argparse.ArgumentParser(
        description="Atmosphere - Modern Weather Application"
    )
    parser.add_argument(
        "--city", "-c",
        type=str,
        default=config.DEFAULT_CITY,
        help="Initial city to display weather for (default: London)"
    )
    parser.add_argument(
        "--units", "-u",
        choices=["metric", "imperial"],
        default=config.DEFAULT_UNITS,
        help="Temperature unit: metric (°C) or imperial (°F)"
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    # Enable High DPI rendering for Windows
    configure_high_dpi()

    # Parse CLI flags
    args = parse_arguments()

    # Apply CLI overrides to config defaults
    if args.city:
        config.DEFAULT_CITY = args.city
    if args.units:
        config.DEFAULT_UNITS = args.units

    # Launch GUI
    print(f"Starting {config.APP_TITLE}...")
    app = gui.WeatherAppGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
