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
    """
    This serializer uses nested relations. To have good readable and writeable nested serializer field, We have defined another write_only
    field named "<field_data>" to receive data for the respected field from the client.
    """
    # airline = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Airline.objects.all())
    airline = AirlineSerializer(many=False, read_only=True)
    airline_data = serializers.PrimaryKeyRelatedField(queryset=models.Airline.objects.all(), many=False, write_only=True)
    aircraft = AircraftSerializer(many=False, read_only=True)
    aircraft_data = serializers.PrimaryKeyRelatedField(queryset=models.Aircraft.objects.all(), many=False, write_only=True)

    class Meta:
        model = models.Flight
        fields = '__all__'
    

    def create(self, validated_data):
        # 'validated_data' is a dictionary consists of the data sent from client to serializer
        airline_data = validated_data.pop('airline_data')
        validated_data.update({'airline': airline_data})
        aircraft_data = validated_data.pop('aircraft_data')
        validated_data.update({'aircraft': aircraft_data})
        f = models.Flight(**validated_data)
        flight = models.Flight.objects.create(**validated_data)
        return flight

    def update(self, instance, validated_data):
        airline_data = validated_data.pop('airline_data')
        aircraft_data = validated_data.pop('aircraft_data')
        instance.airline = airline_data
        instance.aircraft = aircraft_data
        instance.save()
        return instance


class TicketSerializer(serializers.ModelSerializer):
    sub = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Ticket.objects.all())

    class Meta:
        model = models.Ticket
        fields = '__all__'
