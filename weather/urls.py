from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="hello_world"),
    path(
        "average-temperature/",
        views.get_average_temperature,
        name="average_temperature",
    ),
    path(
        "most-common-weather/",
        views.get_most_common_weather,
        name="most_common_weather",
    ),
]
