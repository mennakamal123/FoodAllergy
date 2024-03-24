from django.shortcuts import render
from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Rating, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializers, CartItemSerializer, OrderSerializers, RatingSer
from django_filters.rest_framework import DjangoFilterBackend
import random
from database.models import Allergy, MiniFoodAllergy
from rest_framework.permissions import IsAuthenticated
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    @action(detail=True, methods=['POST'], serializer_class=RatingSer, permission_classes = [IsAuthenticated])
    def rate(self, request, pk=None):
        user = request.user
        product = self.get_object()
        rating = request.data.get('rating')

        Rating.objects.update_or_create(user=user, product=product, defaults={'rating': rating})

        product.refresh_from_db()
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    @action(detail=False,methods=['GET'])
    def recommended(self,*args,**kwargs):
        pro = Product.objects.filter().values_list('id',flat=True)        
        random_product_id_list = random.sample(list(pro),min(len(pro),6))
        query_set = Product.objects.filter(id__in=random_product_id_list)
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data)

class AllergyProductViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['GET'])
    def allergy_products(self, request, pk=None):

        mini_food=MiniFoodAllergy.objects.get(id=pk)

        alg= Allergy.objects.get(id=mini_food.allergy.id)
        # alg= mini_food.allergy.get()

        products = alg.products.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self,request):
        user = request.user
        cart_ = Cart.objects.get(user=user)
        cart_.save()
        serializer = CartSerializers(cart_)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_ = Cart.objects.get(user=user)
        cart, created = CartItem.objects.get_or_create(cart=cart_, product=product, defaults={'quantity': quantity})
        if not created:
            cart.quantity += int(quantity)
            cart.save(update_fields=['quantity'])
        serializer = self.serializer_class(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], serializer_class= OrderSerializers)
    def complete(self,request):
        user=request.user
        data = request.data
        serializers = OrderSerializers(data=data)
        if not serializers.is_valid():
            return Response(serializers.errors)
        cart = Cart.objects.get(user=user)
        cart.save()
        cartItem= CartItem.objects.filter(cart=cart)
        
        order = Order.objects.create(
                user=request.user,
                total_price=cart.total_price,
                name = data['name'],
                address = data['address'],
                phone=data['phone']
                )
        for cartItem_ in cartItem:
            OrderItem.objects.create(
                product=cartItem_.product,
                quantity = cartItem_.quantity,
                price = cartItem_.price,
                order = order
                )
        serializers = OrderSerializers(order)
        return Response(serializers.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names=['get']
    def list(self,request):
        user = request.user
        order_ = Order.objects.filter(user=user).all()
        serializer = self.serializer_class(order_, many=True)
        return Response(serializer.data)
        
