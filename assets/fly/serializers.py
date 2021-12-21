"""
IMPORTANT: Using 'HyperLinkedModelSerializers' with ViewSets needs to handled with care. The link
below can help us:
https://www.py4u.net/discuss/13413
"""
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from . import models
from .models import Airline


class LocationSerializer(CountryFieldMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = '__all__'


class AircraftSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='fly:aircraft-detail')

    class Meta:
        model = models.Aircraft
        fields = '__all__'


class AirlineSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="fly:airline-detail")

    class Meta:
        model = Airline
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    airline = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Airline.objects.all())

    class Meta:
        model = models.Flight
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    sub = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Ticket.objects.all())

    class Meta:
        model = models.Ticket
        fields = '__all__'
