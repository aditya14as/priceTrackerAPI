from rest_framework import serializers
from .models import Bitcoin


class FetchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        fields = '__all__'


class ListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        depth = 1
        fields = ('id', 'price', 'time')
