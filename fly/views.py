"""
IMPORTANT: If we use viewsets, we should use 'queryset' attribute even if we
override it with 'get_queryset' method.
"""
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filter

from . import models
from . import serializers
from . import filters


class LocationViewSet(viewsets.ModelViewSet):
    """Viewset for location"""
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()
    #filter_backends = (filter.DjangoFilterBackend)
    #sfilterset_class = filters.LocationFilter


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
    # filter_backends = (filter.DjangoFilterBackend)
    # filterset_class = filters.TicketFilter


    def get_queryset(self):
        """Override queryset method to filter client queries"""
        queryset = models.Ticket.objects.all()
        return queryset


@api_view(['GET'])
def api_all(request):
    """Show API for all models"""
    aircraft_query = models.Aircraft.objects.all()
    airline_query = models.Airline.objects.all()
    flight_query = models.Flight.objects.all()
    ticket_query = models.Ticket.objects.all()
    location_query = models.Location.objects.all()

    # 1- We should add 'many=True' for every serializer objects if there are more than one object returned by queryset.
    # 2- If we use 'HyperlinkedModelSerializer' we must send 'request' as a context element to the serializer.
    aircraft = serializers.AircraftSerializer(aircraft_query, many=True, context={'request': request})
    airline = serializers.AirlineSerializer(airline_query, many=True, context={'request': request})
    flight = serializers.FlightSerializer(flight_query, many=True, context={'request': request})
    ticket = serializers.TicketSerializer(ticket_query, many=True, context={'request': request})
    location = serializers.LocationSerializer(location_query, many=True, context={'request': request})

    # This is how we return more than one model serializer as json response.
    return Response({'aircrafts': aircraft.data, 'airlines': airline.data, 'flights': flight.data, 'tickets': ticket.data, 'locations': location.data})


@api_view(['GET'])
def api_get(request):
    """Return requested flights and tickets to the client"""
    if request.GET:
        flight_filter_dict = dict()
        ticket_filter_dict = dict()
        result_ticket_filter = None
        result_flight_filter = None
        # Get all filters and respected values for 'Flight' and 'Ticket'
        for filtr, value in request.GET.items():
            # These are for Flight
            if filtr == 'source':
                flight_source = Q(source__city=value)
                flight_filter_dict.update({'flight_source': flight_source})
            if filtr == 'destination':
                flight_destination = Q(destination__city=value)
                flight_filter_dict.update({'flight_destination': flight_destination})
            if filtr == 'aircraft':
                flight_aircraft = Q(aircraft__maker=value)
                flight_filter_dict.update({'flight_aircraft': flight_aircraft})
            # These are for Ticket
            if filtr == 'price':
                ticket_price = Q(price=value)
                ticket_filter_dict.update({'ticket_price': ticket_price})
        # Implement all filters to the 'Flight' query set
        if flight_filter_dict:
            i = 0
            for f in flight_filter_dict.values():
                if len(flight_filter_dict) > 1:
                    if i == 0:
                        result_flight_filter = f
                        i += 1
                        continue
                    result_flight_filter &= f
                else:
                    result_flight_filter = f
        # Implement all filters to the 'Ticket' query set
        if ticket_filter_dict:
            i = 0
            for f in ticket_filter_dict.values():
                if len(ticket_filter_dict) > 1:
                    if i == 0:
                        result_ticket_filter = f
                        i += 1
                        continue
                    result_ticket_filter &= f
                else:
                    result_ticket_filter = f
        # Force filters to models
        if result_flight_filter:
            flight_query = models.Flight.objects.filter(result_flight_filter)
        else:
            # Returns empty queryset
            flight_query = models.Flight.objects.none()
        flight_serializer = serializers.FlightSerializer(instance=flight_query, many=True, context={'request': request})
        if result_ticket_filter:
            ticket_query = models.Ticket.objects.filter(result_ticket_filter)
        else:
            ticket_query = models.Ticket.objects.none()
        ticket_serializer = serializers.TicketSerializer(instance=ticket_query, many=True, context={'request': request})
        # Finally send filterd response to the client
        return Response(data={'flights': flight_serializer.data, 'tickets': ticket_serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response(data={'error': 'No filter for flights or tickets'}, status=status.HTTP_200_OK)
