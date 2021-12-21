from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('list/', views.UserListCreateView.as_view(), name='list'),
    path('list/<user>/', views.UserListCreateView.as_view(), name='list_q'),
    path('retreive/<pk>/', views.UserRetreiveUpdateDedtroyView.as_view(), name='retreive'),
    path('create/', views.UserCreateUpdateView.as_view(), name='create'),
]
