from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    provider = models.ForeignKey(
        Provider, related_name="service_areas", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    geojson = models.JSONField()

    def __str__(self):
        return self.name
