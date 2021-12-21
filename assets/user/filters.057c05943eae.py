from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model


class UserFilterAPI(filters.FilterSet):
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'phone', 'email',
                  'score', 'is_superuser']
