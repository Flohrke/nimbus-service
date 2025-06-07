import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nimbus.settings")
django.setup()
import datetime

from django.test import TestCase

from weather.models import City, WeatherDay
from weather.utils import (
    retrieve_average_temperature_for_city_over_time_period,
    retrieve_most_common_weather_for_city_over_time_period)


class WeatherRetrievalTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Berlin", country="Germany")
        self.other_city = City.objects.create(name="Munich", country="Germany")
        WeatherDay.objects.create(
            city=self.city,
            date=datetime.date(2023, 1, 1),
            temperature_min=0,
            temperature_max=10,
            weather_code=1,
        )
        WeatherDay.objects.create(
            city=self.city,
            date=datetime.date(2023, 1, 2),
            temperature_min=2,
            temperature_max=8,
            weather_code=2,
        )
        # WeatherDay with missing temperatures (should be skipped for average)
        WeatherDay.objects.create(
            city=self.city,
            date=datetime.date(2023, 1, 3),
            temperature_min=None,
            temperature_max=None,
            weather_code=1,
        )
        WeatherDay.objects.create(
            city=self.other_city,
            date=datetime.date(2023, 1, 1),
            temperature_min=5,
            temperature_max=15,
            weather_code=3,
        )

    def test_average_temperature_correct(self):
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 3)
        result = retrieve_average_temperature_for_city_over_time_period(
            "Berlin", start, end
        )
        # Only first two days have valid temperatures: (0+10)/2=5, (2+8)/2=5; avg = 5
        self.assertEqual(result, 5.0)

    def test_average_temperature_no_data(self):
        start = datetime.date(2022, 1, 1)
        end = datetime.date(2022, 1, 31)
        result = retrieve_average_temperature_for_city_over_time_period(
            "Berlin", start, end
        )
        self.assertIsNone(result)

    def test_average_temperature_city_not_found(self):
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 3)
        result = retrieve_average_temperature_for_city_over_time_period(
            "Paris", start, end
        )
        self.assertIsNone(result)

    def test_most_common_weather_correct(self):
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 3)
        result = retrieve_most_common_weather_for_city_over_time_period(
            "Berlin", start, end
        )
        # Weather codes: 1, 2, 1 -> most common is 1
        from nimbus.constants import WEATHER_CODE_TO_DESCRIPTION

        expected = WEATHER_CODE_TO_DESCRIPTION.get(1, "unknown weather code")
        self.assertEqual(result, expected)

    def test_most_common_weather_no_data(self):
        start = datetime.date(2022, 1, 1)
        end = datetime.date(2022, 1, 31)
        result = retrieve_most_common_weather_for_city_over_time_period(
            "Berlin", start, end
        )
        self.assertIsNone(result)

    def test_most_common_weather_city_not_found(self):
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 3)
        result = retrieve_most_common_weather_for_city_over_time_period(
            "Paris", start, end
        )
        self.assertIsNone(result)
