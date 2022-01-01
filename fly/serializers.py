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
    This serializer uses nested relations. Per rest_framework document to have a writeable nested serializer we should define
    'create' or/and 'update' methods explicity for the serializer
    """
    # airline = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Airline.objects.all())
    airline = AirlineSerializer(many=False, read_only=True)
    airline_write = serializers.PrimaryKeyRelatedField(queryset=models.Airline.objects.all(), many=False, write_only=True)
    aircraft = AircraftSerializer(many=False, read_only=True)

    class Meta:
        model = models.Flight
        fields = '__all__'
    

    def create(self, validated_data):
        airline_data = validated_data.pop('airline_write')
        print(airline_data)
        validated_data.update({'airline': airline_data})
        f = models.Flight(**validated_data)
        print(f, '  ', type(f), '   ', f.airline, '    ', f.airline.name, '   ', f.name)
        Farda az inja shoroo mishavad
        # flight = models.Flight.objects.create(**validated_data)
        # return flight
    """
    def update(self, instance, validated_data):
        airline_data = validated_data.pop('airline')
        flight = models.Flight.objects.create(**validated_data)
        for data in airline_data:
            models.Airline.objects.create(flight=flight, **data)
        return flight
    """


class TicketSerializer(serializers.ModelSerializer):
    sub = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Ticket.objects.all())

    class Meta:
        model = models.Ticket
        fields = '__all__'
