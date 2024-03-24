from rest_framework import serializers
from .models import Product, CartItem,Cart, Rating,OrderItem, Order
from django.db import models
from django.db.models import Avg
from database.models import Allergy

class AllergySerializer_(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    allergies = AllergySerializer_(many=True, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"

    def get_products(self, obj):
        products = obj.products
        dataofproducts = {
            "image": products.image,
            "arabicDescription": products.arabicDescription,
            "englishDescription": products.englishDescription,
            "arabicName": products.arabicName,
            "englishName": products.englishName,
            "price": products.price,
        }
        return dataofproducts
    def get_rating(self, obj):
        return obj.ratings.aggregate(models.Avg('rating'))['rating__avg']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',read_only=True)
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    item = OrderItemSerializers(read_only=True, many=True)
    class Meta:
        model = Order
        fields = ['id','name','address','phone','item','total_price']
        extra_kwargs={"total_price":{"read_only":True}}

class RatingSer(serializers.Serializer):
    rating = serializers.IntegerField()