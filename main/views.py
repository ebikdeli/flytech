from django.shortcuts import render, HttpResponse
from .models import Dflight
from fly.models import Ticket
from fly.filters import TicketFilterSet


def index(request):
    flight = Dflight.objects.all().last()
    # for f in Dflight.objects.all().filter(country__icontains='iran'):
    #     print(f.icao)
    return HttpResponse('country: ' + flight.country + '  flight id: ' + str(flight.id) + '  flight icao number: ' + flight.icao)


def ticket_view(request):
    tf = TicketFilterSet(request.GET, Ticket.objects.all())
    return render(request, 'index.html', {'filter': tf})
