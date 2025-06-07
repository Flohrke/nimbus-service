import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from weather.models import City, WeatherDay
from weather.utils import (
    retrieve_average_temperature_for_city_over_time_period,
    retrieve_most_common_weather_for_city_over_time_period)


# Create your views here.
def index(request):
    cities = City.objects.all().values_list("name", flat=True)
    dates = set(WeatherDay.objects.all().values_list("date", flat=True))
    years = set([date.year for date in dates])
    return render(request, "weather_index.html", {"cities": cities, "years": years})


@require_GET
def get_average_temperature(request: HttpRequest) -> HttpResponse:
    city_name = request.GET.get("city")
    period_start = request.GET.get("start")
    period_end = request.GET.get("end")
    if not city_name:
        return JsonResponse({"error": "Missing city name"}, status=400)
    if not period_start or not period_end:
        return JsonResponse({"error": "Missing start or end date"}, status=400)

    try:
        start = datetime.datetime.strptime(period_start, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(period_end, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format. Use YYYY-MM-DD."}, status=400
        )

    if start > end:
        return JsonResponse(
            {"error": "Start date has to be before end date"}, status=400
        )

    average_temperature = retrieve_average_temperature_for_city_over_time_period(
        city_name, start, end
    )
    if not average_temperature:
        return JsonResponse({"error": "No data available"}, status=404)
    return JsonResponse({"city": city_name, "average_temperature": average_temperature})


@require_GET
def get_most_common_weather(
    request: HttpRequest,
) -> HttpResponse:
    city_name = request.GET.get("city")
    period_start = request.GET.get("start")
    period_end = request.GET.get("end")
    if not city_name:
        return JsonResponse({"error": "Missing city name"}, status=400)
    if not period_start or not period_end:
        return JsonResponse({"error": "Missing start or end date"}, status=400)

    try:
        start = datetime.datetime.strptime(period_start, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(period_end, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format. Use YYYY-MM-DD."}, status=400
        )

    average_temperature = retrieve_most_common_weather_for_city_over_time_period(
        city_name, start, end
    )
    if not average_temperature:
        return JsonResponse({"error": "No data available"}, status=404)
    return JsonResponse({"city": city_name, "most_common_weather": average_temperature})
