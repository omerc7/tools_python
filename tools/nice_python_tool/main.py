import argparse

import requests
import pydantic

from .weather import get_weather_city


class WeatherOutput(pydantic.BaseModel):
    temperature: float
    windspeed: float
    winddirection: float


def get_coordinates(city_name):
    # Use Nominatim API to get latitude and longitude for the city
    geocode_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    response = requests.get(geocode_url, params=params)
    data = response.json()

    if data:
        latitude = data[0]["lat"]
        longitude = data[0]["lon"]
        return float(latitude), float(longitude)
    else:
        raise Exception("Location not found")


def get_weather(latitude, longitude):
    # Use Open-Meteo API to get current weather data
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current_weather": True}
    response = requests.get(weather_url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract and display weather data
    current_weather = data.get("current_weather", {})
    print(current_weather)
    return WeatherOutput(**current_weather)


def get_weather_city(city_name):
    latitude, longitude = get_coordinates(city_name)
    w_output = get_weather(latitude, longitude)
    print(f"Current Weather in {city_name}:")
    print(f"Temperature: {w_output.temperature}°C")
    print(f"Wind Speed: {w_output.windspeed} m/s")
    print(f"Wind Direction: {w_output.winddirection}°")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get current weather for a city")
    parser.add_argument("city", help="Name of the city to get weather for")

    # Parse command-line arguments
    args = parser.parse_args()

    # Get coordinates for the given city
    city_name = args.city
    get_weather_city(city_name)
