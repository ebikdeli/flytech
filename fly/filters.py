# This is for django-rest framework
from django_filters import rest_framework as filters
from . import models


class TicketFilter(filters.FilterSet):

    class Meta:
        model = models.Ticket
        exclude = ['seat_number', 'total_price', 'sub']




"""
# This is for regular django view
import django_filters
from . import models


class TicketFilter(django_filters.FilterSet):
    # Filters for ticket model field

    class Meta:
        model = models.Ticket
        exclude = ['seat_number', 'total_price', 'sub']
"""
