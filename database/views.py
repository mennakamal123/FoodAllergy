from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Allergy, Category, Food, FoodAllergy, MiniFoodAllergy
from .permissions import FoodAllergyPermission, CategoryPermission, AllergyPermission, FoodPermission, MiniFoodAllergyPermission
from .serializers import (
    AllergySerializer,
    CategorySerializer,
    FoodAllergySerializer,
    FoodSerializer, 
    MiniFoodAllergySerializer,
    AllergySerializer_
)
from cart.serializers import ProductSerializer
# Create your views here.

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [FoodPermission]


class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer
    # permission_classes = [AllergyPermission]

    @action(detail=True, methods=['GET'])
    def products(self, request, pk=None):
        allergy = self.get_object()
        products = allergy.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request, pk=None):
        allergy = Allergy.objects.get(id=pk)
        serializers = AllergySerializer_(allergy)
        return Response(serializers.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

   

class FoodAllegryViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['GET'])
    def allergy(self, request, pk=None):


        mini_food = MiniFoodAllergy.objects.get(id=pk)
        allergy = FoodAllergy.objects.get(id=mini_food.foodallergy.id)


        serializer = FoodAllergySerializer(allergy)
        return Response(serializer.data)

class MiniFoodAllegryViewSet(viewsets.ModelViewSet):
    queryset = MiniFoodAllergy.objects.all()
    serializer_class = MiniFoodAllergySerializer
    permission_classes = [MiniFoodAllergyPermission]


    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    