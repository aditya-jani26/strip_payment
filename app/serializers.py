from rest_framework import serializers
from .models import *
# from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        
    def __init__(self, instance=None, data=..., **kwargs):
        try:
            data = data.copy()
            data['password'] = make_password(data['password'])
        except:
            pass
        super().__init__(instance, data, **kwargs)
        