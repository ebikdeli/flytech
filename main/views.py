from django.shortcuts import render, HttpResponse
from .models import Dflight
from fly.models import Ticket
from fly.filters import TicketFilter


def index(request):
    tf = TicketFilter(request.GET, Ticket.objects.all())
    return render(request, 'index.html', {'filter': tf})
    """
    flight = Dflight.objects.all().last()
    for f in Dflight.objects.all().filter(country__icontains='iran'):
        print(f.icao)
    return HttpResponse(flight.country + '  ' + str(flight.id))
    """