import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nimbus.settings")
django.setup()
import datetime
import json
from typing import Any, Dict, List, Tuple

import pandas as pd
import requests
from rich import print

from weather.models import City, WeatherDay


def fetch_weather_data(
    longitude: float, latitude: float, timerange: Tuple[datetime.date, datetime.date]
) -> Dict[str, Any]:
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": timerange[0],
        "end_date": timerange[1],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
        ],
    }
    response = requests.get(base_url, params=params).json()

    return response


def populate_database(data: Dict[str, Any]) -> List[Dict[str, str]] | None:
    x = 0
    errors = []
    for city, weather in data.items():
        try:
            print(f"Storing data for {city} - {x}/{len(data)}")
            city = City.objects.get_or_create(name=city, country=weather["country"])
            weather_objects = [
                WeatherDay(
                    city=city[0],
                    date=weather["daily"]["time"][i],
                    temperature_max=weather["daily"]["temperature_2m_max"][i],
                    temperature_min=weather["daily"]["temperature_2m_min"][i],
                    weather_code=weather["daily"]["weather_code"][i],
                )
                for i in range(len(weather["daily"]["time"]))
            ]
            WeatherDay.objects.bulk_create(weather_objects)
            x += 1
        except Exception as e:
            print("Failed to store data for city", city)
            errors.append({"city": city, "error": str(e)})
    return errors if len(errors) != 0 else None


if __name__ == "__main__":
    timerange = (datetime.date(2024, 1, 1), datetime.date(2024, 12, 31))

    # collect city coordinates for mapping
    data = pd.read_csv("weather/data/city_mapping.csv", delimiter=",")[
        ["Capital City", "Country", "Latitude", "Longitude"]
    ].astype(str)
    data = data[:100]  # limited to 100 cities

    # fetch data from weather api for designated timerange and store locally
    if not os.path.exists(
        f"weather/data/weather_data_{timerange[0]}_{timerange[1]}.json"
    ):
        print("Fetching weather data...")
        time.sleep(1)
        total = len(data["Capital City"])
        fetched_data = {}
        for i, row in enumerate(
            zip(
                data["Capital City"],
                data["Country"],
                data["Latitude"],
                data["Longitude"],
            ),
            start=1,
        ):
            city, country, lat, lon = row
            print(f"Fetching {city} ({i}/{total})...")
            fetched_data[city] = {
                **fetch_weather_data(lat, lon, timerange),
                "country": country,
            }

        with open(
            f"weather/data/weather_data_{timerange[0]}_{timerange[1]}.json", "w"
        ) as outfile:
            json.dump(fetched_data, outfile)

    with open(
        f"weather/data/weather_data_{timerange[0]}_{timerange[1]}.json", "r"
    ) as f:
        fetched_data = json.load(f)

    # populate SQL database with data
    storage_errors = populate_database(fetched_data)
    if storage_errors:
        print("Errors detected during storage of data:")
        for case in storage_errors:
            print(case["city"], case["error"])
