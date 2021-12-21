from django.db import models


class Dflight(models.Model):
    icao = models.CharField(max_length=10, blank=True, null=True)
    callsign = models.CharField(max_length=8, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'dflight'
