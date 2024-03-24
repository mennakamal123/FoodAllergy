from django.db.models.signals import post_save, pre_delete
from users.models import User
from .models import Cart
def create_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

post_save.connect(create_profile, sender=User)