from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'fly'

# router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()

router.register('location', views.LocationViewSet)
router.register('aircraft', views.AircraftViewSet)
router.register('airline', views.AirlineViewSet)
router.register('flight', views.FlightViewSet)
router.register('ticket', views.TicketViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/get/', views.api_get, name='api_get'),
    path('api/show/all', views.api_all, name='api_show_all'),
]
