# Open-Meteo retrieval tool will be implemented here.
# No API key is normally required for the public endpoint.
import requests
from guardrails.validation import wrap_untrusted_context

def fetch_weather_data(city: str = "Chennai") -> dict:
    """Retrieves current weather metrics from the Open-Meteo REST API."""
    try:
        # Default coordinates for Chennai (13.0827° N, 80.2707° E)
        url = "https://api.open-meteo.com/v1/forecast?latitude=13.0827&longitude=80.2707&current_weather=true"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json().get("current_weather", {})
            metrics = f"City: {city} | Temperature: {data.get('temperature')}°C | Windspeed: {data.get('windspeed')} km/h | WeatherCode: {data.get('weathercode')}"
            return {
                "evidence": wrap_untrusted_context(metrics),
                "source": "Open-Meteo REST API"
            }
        return {
            "evidence": wrap_untrusted_context("Open-Meteo API unavailable."),
            "source": "Open-Meteo API"
        }
    except Exception as e:
        return {
            "evidence": wrap_untrusted_context(f"Weather lookup error: {str(e)}"),
            "source": "Open-Meteo API Error"
        }