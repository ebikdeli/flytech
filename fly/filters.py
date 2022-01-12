# This is for django-rest framework
import django_filters as f
from django_filters import rest_framework as filter
from . import models


<<<<<<< HEAD
class FlightFilterSet(filter.FilterSet):
    date = f.RangeFilter()
=======
class LocationFilter(filters.FilterSet):
    """Filterset for Location model"""

    class Meta:
        model = models.Location
        fields = '__all__'

class TicketFilter(filters.FilterSet):

>>>>>>> f1bd08ca701840a1dd253a2ae0e5fface6131a5e
    class Meta:
        model = models.Flight
        fields = '__all__'

class TicketFilterSet(filter.FilterSet):

    class Meta:
        model = models.Ticket
        exclude = ['seat_number', 'total_price', 'sub']
