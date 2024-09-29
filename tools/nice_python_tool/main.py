import httpx


def get_weather():
    return httpx.get(
        "https://api.open-meteo.com/v1/forecast?latitude=32.0809&longitude=34.7806&hourly=temperature_2m"
    )


def main():
    response = get_weather()
    print(response.json())


if __name__ == "__main__":
    main()
