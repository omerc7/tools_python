import argparse

from .weather import get_weather_city


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get current weather for a city")
    parser.add_argument("city", help="Name of the city to get weather for")

    # Parse command-line arguments
    args = parser.parse_args()

    # Get coordinates for the given city
    city_name = args.city
    get_weather_city(city_name)
