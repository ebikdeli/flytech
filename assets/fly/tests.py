from django.test import TestCase
from django_countries import countries
from django.contrib.auth import get_user_model

from . import models

class TestSingleModels(TestCase):
    def test_location(self):
        """Test if location created properly"""
        loc = models.Location.objects.create(country='IR', state='Khoozestan', city='Dezfool')

        self.assertEqual(loc.city, 'Dezfool')
        # The following two lines are equal
        self.assertEqual(dict(countries)[loc.country], 'Iran')
        self.assertEqual(loc.country.name, 'Iran')
    
    def test_aircraft(self):
        """Test if aircaft created properly"""
        ac = models.Aircraft.objects.create(name='737 max 900', maker='boeing', seats=189, price=123, model='14/09/2020')

        self.assertEqual(ac.price, 123)

    def test_airline(self):
        """Test new airline object"""
        kish = models.Airline.objects.create(name='KishAirline', established='Iran, Kish island, 1992', fleet_size=23)

        self.assertEqual(kish.name, 'KishAirline')

    def test_flight(self):
        """Test if flight model works as expected"""
        source = models.Location.objects.create(country='IR', state='Khoozestan', city='Dezfool')
        destination = models.Location.objects.create(country='IR', state='Tehran', city='Tehran')
        airline = models.Airline.objects.create(name='KishAirline', established='Iran, Kish island, 1992', fleet_size=23)
        ac = models.Aircraft.objects.create(name='737 max 900', maker='boeing', seats=189, price=123, model='14/09/2020')
        s = '2021-12-06 19:10'
        r = '2021-12-06 20:00'
        d = 400
        passengers = 110
        flight = models.Flight.objects.create(
            source=source,
            destination=destination,
            airline=airline,
            aircraft=ac,
            start=s,
            reach=r,
            distance=d,
            passengers=passengers,
        )

        self.assertEqual(flight.destination.country.name, 'Iran')
        self.assertEqual(flight.aircraft.name, '737 max 900')
    
    def test_ticket(self):
        """Create and overwatch if ticket created properly"""
        owner = get_user_model().objects.create(username='ehsan', password='1234567')
        source = models.Location.objects.create(country='IR', state='Khoozestan', city='Dezfool')
        destination = models.Location.objects.create(country='IR', state='Tehran', city='Tehran')
        airline = models.Airline.objects.create(name='KishAirline', established='Iran, Kish island, 1992', fleet_size=23)
        ac = models.Aircraft.objects.create(name='737 max 900', maker='boeing', seats=189, price=123, model='14/09/2020')
        s = '2021-12-06 19:10'
        r = '2021-12-06 20:00'
        d = 400
        passengers = 110
        flight = models.Flight.objects.create(
            source=source,
            destination=destination,
            airline=airline,
            aircraft=ac,
            start=s,
            reach=r,
            distance=d,
            passengers=passengers,
        )
        ticket = models.Ticket.objects.create(
            owner=owner,
            source=source,
            destination=destination,
            flight=flight,
            price=200000,
            total_price=190000,
            seat_number=19
        )

        self.assertEqual(ticket.flight.aircraft.maker, 'boeing')
