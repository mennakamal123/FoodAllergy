# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings

# """
# """

# def default_profile_pic():
#     return "profile_pics/default.jpg"

# class User(AbstractUser):
#     email = models.EmailField(_("email address"), unique=True)
    
#     is_doctor = models.BooleanField(default=False)
#     is_patient = models.BooleanField(default=False)
    
#     profile_pic = models.ImageField(
#         blank=True,
#         null=True,
#         upload_to="profile_pics",
#         default=default_profile_pic,
#     )
#     phone = models.CharField(
#         max_length=20,
#         blank=True,
#     )
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     def default_image_url(self):
#         return settings.MEDIA_URL + default_profile_pic()
    
#     def save(self, *args, **kwargs):
#         # Set the profile pic to the default image if it is not already set
#         if not self.profile_pic:
#             self.profile_pic = default_profile_pic()
#         super().save(*args, **kwargs)

# class Doctor(models.Model):
#     doctor = models.OneToOneField(
#         "User",
#         on_delete=models.CASCADE,
#     )

#     license_pic = models.ImageField(
#         null=True,
#         upload_to="license_pic",
#     )
#     face_pic = models.ImageField(
#         null=True,
#         upload_to="face_pic",
#     )

#     def __str__(self):
#         return self.doctor.username

# @receiver(post_save, sender=Doctor)
# def update_doctor_status(sender, instance, **kwargs):
#     if instance.license_pic:
#         instance.doctor.is_doctor = True
#     else:
#         instance.doctor.is_doctor = False
#     instance.doctor.save()


# class Patient(models.Model):
#     patient = models.OneToOneField(
#         "User",
#         on_delete=models.CASCADE,
#     )


#     def __str__(self):
#         return self.patient.username

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# """
# """

def default_profile_pic():
    return "profile_pics/default.jpg"

# class User(AbstractUser):
#     email = models.EmailField(_("email address"), unique=True)
    
#     is_doctor = models.BooleanField(default=False)
#     is_patient = models.BooleanField(default=False)
    
#     profile_pic = models.ImageField(
#         blank=True,
#         null=True,
#         upload_to="profile_pics",
#         default=default_profile_pic,
#     )
#     phone = models.CharField(
#         max_length=20,
#         blank=True,
#     )
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     def default_image_url(self):
#         return settings.MEDIA_URL + default_profile_pic()
    
#     def save(self, *args, **kwargs):
#         # Set the profile pic to the default image if it is not already set
#         if not self.profile_pic:
#             self.profile_pic = default_profile_pic()
#         super().save(*args, **kwargs)
from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django_session_jwt.middleware.session import SessionMiddleware, BaseSessionMiddleware
from django.contrib.sessions.models import Session
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')


        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user




class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    
    profile_pic = models.ImageField(
        blank=True,
        null=True,
        upload_to="profile_pics",
        default=default_profile_pic,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email



class Doctor(models.Model):
    doctor = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
    )

    license_pic = models.ImageField(
        null=True,
        upload_to="license_pic",
    )
    face_pic = models.ImageField(
        null=True,
        upload_to="face_pic",
    )

    def __str__(self):
        return self.doctor.username

@receiver(post_save, sender=Doctor)
def update_doctor_status(sender, instance, **kwargs):
    if instance.license_pic:
        instance.doctor.is_doctor = True
    else:
        instance.doctor.is_doctor = False
    instance.doctor.save()


class Patient(models.Model):
    patient = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return self.patient.username


