# This is for django-rest framework
import django_filters as f
from django_filters import rest_framework as filter
from . import models


class FlightFilterSet(filter.FilterSet):
    date = f.RangeFilter()
    class Meta:
        model = models.Flight
        fields = '__all__'

class TicketFilterSet(filter.FilterSet):

    class Meta:
        model = models.Ticket
        exclude = ['seat_number', 'total_price', 'sub']
