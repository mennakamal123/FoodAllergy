from typing import Iterable, Optional
from django.db import models
from users.models import User
from database.models import Allergy

class Product(models.Model):
    arabicName = models.CharField(max_length=255)
    englishName = models.CharField(max_length=255)
    arabicDescription = models.TextField()
    englishDescription = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    allergies = models.ManyToManyField(Allergy, related_name='products')

    def __str__(self):
        return f"{self.arabicName} - {self.englishName}"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
   
    def save(self,*args, **kwargs):
        try:
            self.get_price
        except:
            pass
        return super().save(*args, **kwargs)
    

    @property
    def get_price(self):
        price = sum(item.price for item in self.items.all())
        if price != self.total_price:
            self.total_price = price
            self.save(update_fields=["total_price"])
        return self.total_price
    
    def _str_(self) -> str:
        return self.user.email
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField(default=0.0)
    
    def save(self,*args, **kwargs):
        self.get_price
        return super().save(*args, **kwargs)

    
    @property
    def get_price(self):
        price = int(self.product.price) * int(self.quantity)
        if price != self.price:
            if not self.price == 0.0:
                self.price = price                 
                self.save(update_fields=["price"])
            self.price = price
        return self.price
    def _str_(self) -> str:
        return self.cart.user.email

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length= 50)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=20,null=True)
    total_price = models.FloatField(default=0)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField(default=0.0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')


