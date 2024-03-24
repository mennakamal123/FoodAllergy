from rest_framework import serializers
from database.serializers import CategorySerializer

class PredictSerializer(serializers.Serializer):
    image = serializers.ImageField()
    category = CategorySerializer(read_only=True)