from django.contrib import admin

from . import models


admin.site.register([models.Location, models.Aircraft, models.Airline, models.Flight, models.Ticket])
