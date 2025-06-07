import datetime
from collections import Counter

from weather.models import City


def retrieve_average_temperature_for_city_over_time_period(
    city_name: str, start: datetime.date, end: datetime.date
) -> float | None:
    try:
        city = City.objects.get(name=city_name)
        # NOTE: since we apply a flexible range for filtering here we silently fail any non-available days.
        # This is more robust but also might result in differing average values depending on data availability.
        weather_data = city.weatherday_set.filter(date__gte=start, date__lte=end)
        daily_average_temperature = [
            w.average_temperature for w in weather_data if w.average_temperature
        ]
        return sum(daily_average_temperature) / len(daily_average_temperature)
    except Exception as e:
        print(e)
        return None


def retrieve_most_common_weather_for_city_over_time_period(
    city_name: str, start: datetime.date, end: datetime.date
) -> float | None:
    try:
        city = City.objects.get(name=city_name)
        weather_data = city.weatherday_set.filter(date__gte=start, date__lte=end)

        most_common_weather = Counter([w.most_frequent_weather for w in weather_data])
        return most_common_weather.most_common(1)[0][0]
    except Exception as e:
        print(e)
        return None
