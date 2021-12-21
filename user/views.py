from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework import permissions
from django_filters import rest_framework as filters

from .serializers import UserSerializer
from .filters import UserFilterAPI


class UserListCreateView(generics.ListCreateAPIView):
    """Create a new user or get all users list"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [filters.DjangoFilterBackend,]
    filterset_class = UserFilterAPI
    
    def get_queryset(self):
        """Override get_queryset default method (for future use)"""
        print(self.request.query_params)
        if self.request.user.is_superuser:
            queryset = get_user_model().objects.all()
        else:
            queryset = get_user_model().objects.filter(id=self.request.user.id)
        name = self.request.query_params.get('q')
        if name:
            return queryset.filter(username__contains=name)
        return queryset
        
        
class UserRetreiveUpdateDedtroyView(generics.RetrieveUpdateDestroyAPIView):
    """Delete or Updated or Retreive a user"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = get_user_model().objects.all()


class UserCreateUpdateView(generics.CreateAPIView):
    """Everyone can create user"""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = get_user_model().objects.all()
