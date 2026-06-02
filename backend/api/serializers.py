from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class StockPredictionSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=20)
