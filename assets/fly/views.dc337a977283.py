"""
IMPORTANT: If we use viewsets, we should use 'queryset' attribute even if we
override it with 'get_queryset' method.
"""
from django.shortcuts import render
from rest_framework import viewsets

from . import models
from . import serializers


class LocationViewSet(viewsets.ModelViewSet):
    """Viewset for location"""
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class AircraftViewSet(viewsets.ModelViewSet):
    """Viewset for Aircraft"""
    serializer_class = serializers.AircraftSerializer
    queryset = models.Aircraft.objects.all()


class AirlineViewSet(viewsets.ModelViewSet):
    """Viewset for Airline"""
    serializer_class = serializers.AirlineSerializer
    queryset = models.Airline.objects.all()


class FlightViewSet(viewsets.ModelViewSet):
    """Viewset for Flight"""
    serializer_class = serializers.FlightSerializer
    queryset = models.Flight.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    """Viewset for Ticket"""
    serializer_class = serializers.TicketSerializer
    queryset = models.Ticket.objects.all()

    def get_queryset(self):
        """Override queryset method to filter client queries"""
        queryset = models.Ticket.objects.all()
        return queryset
        