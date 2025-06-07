from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country"], name="unique_city_country"
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.country}"


class WeatherDay(models.Model):
    from nimbus.constants import WEATHER_CODE_TO_DESCRIPTION

    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    temperature_max = models.FloatField(null=True)
    temperature_min = models.FloatField(null=True)
    weather_code = models.IntegerField(null=True, choices=WEATHER_CODE_TO_DESCRIPTION)

    @property
    def average_temperature(self) -> float | None:
        if self.temperature_max is None or self.temperature_min is None:
            return None
        return (self.temperature_min + self.temperature_max) / 2

    @property
    def most_frequent_weather(self) -> str:
        from nimbus.constants import WEATHER_CODE_TO_DESCRIPTION

        return WEATHER_CODE_TO_DESCRIPTION.get(
            self.weather_code, "unknown weather code"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["city", "date"], name="unique_city_date"),
            models.CheckConstraint(
                check=(
                    (
                        models.Q(temperature_max__isnull=True)
                        & models.Q(temperature_min__isnull=True)
                    )
                    | (
                        models.Q(temperature_max__isnull=False)
                        & models.Q(temperature_min__isnull=False)
                    )
                ),
                name="min_and_max_temperature_both_null_or_filled",
            ),
        ]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.city} on {self.date}"
