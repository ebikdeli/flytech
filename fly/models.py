from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class Location(models.Model):
    """Source and Destination locations include country, city and airport"""
    country = CountryField(verbose_name=_('country'), max_length=50, blank=True, null=True)
    state = models.CharField(verbose_name=_('state, province or municipality'), max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name=_('city'), max_length=255, blank=True, null=True)
    airport = models.CharField(verbose_name=_('airport'), max_length=500, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)


class Aircraft(models.Model):
    """Aircraft specifications"""
    name = models.CharField(verbose_name=_('name'), max_length=255)
    maker = models.CharField(verbose_name=_('maker'), max_length=100, blank=True, null=True)
    model = models.CharField(verbose_name=_('aircraft model'), max_length=100, blank=True, null=True)
    year = models.DateField(verbose_name=_('year produced'), blank=True, null=True)
    seats = models.PositiveIntegerField(verbose_name=_('number of seats'), blank=True, null=True)
    price = models.DecimalField(verbose_name=_('aircraft price (m$)'), max_digits=12, decimal_places=2, blank=True, null=True)


class Airline(models.Model):
    """This class define airlines related fields"""
    name = models.CharField(verbose_name=_('name'), max_length=255)
    established = models.CharField(verbose_name=_('established'), max_length=255, blank=True, null=True)
    fleet_size = models.PositiveIntegerField(verbose_name=_('fleet size'), blank=True, null=True)


class Flight(models.Model):
    """This class contains flight specifications"""
    sub = models.ForeignKey('self', verbose_name=_('sub flight'), on_delete=models.CASCADE, related_name='sub_flight', blank=True, null=True)
    name = models.CharField(verbose_name=_('flight name'), default='Unknown', max_length=255)
    source = models.ForeignKey('Location', verbose_name=_('source location'), on_delete=models.SET_NULL, related_name='flight_source', blank=True, null=True)
    destination = models.ForeignKey('Location', verbose_name=_('destination location'), on_delete=models.SET_NULL, related_name='flight_destination', blank=True, null=True)
    airline = models.ForeignKey('Airline', verbose_name=_('airline'), on_delete=models.SET_NULL, related_name='flight_airline', blank=True, null=True)
    aircraft = models.ForeignKey('Aircraft', verbose_name=_('aircraft'), on_delete=models.SET_NULL, related_name='flight_aircraft', blank=True, null=True)
    start = models.DateTimeField(verbose_name=_('start time (est)'), blank=True, null=True)
    reach = models.DateTimeField(verbose_name=_('reach date (est)'), blank=True, null=True)
    distance = models.PositiveIntegerField(verbose_name=_('distance (KM)'), blank=True, null=True)
    passengers = models.PositiveIntegerField(verbose_name=_('passengers numbers'), blank=True, null=True)


class Ticket(models.Model):
    """This class contains ticket specs"""
    sub = models.ForeignKey('self', verbose_name=_('sub ticket'), on_delete=models.CASCADE, related_name='sub_ticket', blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), verbose_name=_('ticket owner'), on_delete=models.CASCADE, related_name='ticket_owner')
    source = models.ForeignKey('Location', verbose_name=_('source location'), on_delete=models.SET_NULL, related_name='ticket_source', blank=True, null=True)
    destination = models.ForeignKey('Location', verbose_name=_('destination location'), on_delete=models.SET_NULL, related_name='ticket_destination', blank=True, null=True)
    flight = models.ForeignKey('Flight', verbose_name=_('flight'), on_delete=models.CASCADE, related_name='ticket_flight')
    price = models.DecimalField(verbose_name=_('ticket price'), max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(verbose_name=_('ticket price after discounts'), max_digits=10, decimal_places=2, blank=True, null=True)
    seat_number = models.PositiveIntegerField(verbose_name=_('seat number'), blank=True, null=True)
