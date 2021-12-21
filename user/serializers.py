from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user:retreive')

    class Meta:
        model = get_user_model()
        exclude = ['background', 'is_active', 'is_staff',
                   'is_admin', 'slug', 'created',
                   'updated', 'user_permissions', 'groups']
        extra_kwargs = {'password': {'write_only': True}}
