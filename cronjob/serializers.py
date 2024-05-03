
from rest_framework import serializers
from app.models import *

# from rest_framework.authtoken.models import Token

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name', 'image')