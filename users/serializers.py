# from dj_rest_auth.registration.serializers import RegisterSerializer
# from dj_rest_auth.serializers import LoginSerializer
# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from django.conf import settings

# from .models import  Doctor, Patient

# class LoginSerializer(LoginSerializer):
#     username = None

# User = get_user_model()

# from dj_rest_auth.serializers import TokenSerializer

# class DetailedTokenSerializer(TokenSerializer):
#     status = serializers.SerializerMethodField()
#     message = serializers.SerializerMethodField()

#     id = serializers.IntegerField(source="user.id")
#     name = serializers.CharField(source="user.username")
#     email = serializers.CharField(source="user.email")
#     phone = serializers.CharField(source="user.phone")
#     image = serializers.SerializerMethodField()
#     is_doctor = serializers.BooleanField(source="user.is_doctor")
    
#     token = serializers.CharField(source="key")
    
#     class Meta(TokenSerializer.Meta):
#         fields = ["status", "message", "id", "name", "email","phone", "image", "is_doctor", "token"]
    
#     def get_status(self, obj):
#         return True if obj else False

#     def get_message(self, obj):
#         # return "تم تسجيل الدخول بنجاح" if obj else "خطأ في البريد الالكتروني او كلمة المرور"
#         return settings.LOGIN_SUCCESS_MESSAGE
    
#     def get_image(self, obj):
#         if obj.user.profile_pic:
#             return obj.user.profile_pic.url
#         else:
#             return obj.user.default_image_url()

# class DoctorCustomRegistrationSerializer(RegisterSerializer):
#     phone = serializers.CharField(required=True)

#     password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
#     password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
#     def get_cleaned_data(self):
#         data = super().get_cleaned_data()
#         print(data)
#         extra_data = {
#             "phone": self.validated_data.get("phone", ""),
#         }
#         data.update(extra_data)
#         return data

#     def save(self, request):
#         data = self.get_cleaned_data()
#         phone = data.get("phone")

#         user = super().save(request)
#         # user.is_doctor = True
#         user.phone = phone
#         user.save()
        
#         doctor = Doctor(doctor=user)

#         doctor.save()

#         return user


# class CustomPatientRegistrationSerializer(RegisterSerializer):
#     phone = serializers.CharField(required=True)

#     password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
#     password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

#     def get_cleaned_data(self):
#         data = super().get_cleaned_data()

#         extra_data = {
#             "phone": self.validated_data.get("phone", ""),
#         }
    
#         data.update(extra_data)
#         return data

#     def save(self, request):
#         data = self.get_cleaned_data()

#         phone = data.get("phone")
        
#         user = super().save(request)
#         user.is_patient = True
#         user.phone = phone
        
#         user.save()

#         patient = Patient(
#             patient=user,
#         )
#         patient.save()
#         return user

# class LicenseSerializer(serializers.ModelSerializer):
#     license_pic = serializers.ImageField(write_only=True)
#     face_pic = serializers.ImageField(write_only=True)
#     class Meta:
#         model = Doctor
#         fields = ('license_pic','face_pic')

# class LicenseSerializer_(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = ['license_pic']
# class UserProfileSerializer(serializers.ModelSerializer):
#     licen = LicenseSerializer_(read_only=True)
#     class Meta:
#         model = User
#         fields = ('id', 'username','email', 'profile_pic', 'phone','licen')

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import  Doctor, Patient
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import User
from django_session_jwt.middleware.session import SessionMiddleware
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from uuid import getnode as get_mac
from rest_framework import status
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password_again = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ["email", "username", "password",'password_again', "phone"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get('password','').strip()
        password_again = attrs.get('password_again','').strip()
        if password != password_again:
            raise serializers.ValidationError({"password":'Password not matching'})            
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            phone = validated_data['phone'],
            password= validated_data['password'],
            username=validated_data['username']
            )




class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=2000, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    Token = serializers.CharField(
        max_length=200000, min_length=6, read_only=True
    )
    phone =serializers.CharField(read_only=True)
    profile_pic = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "username",
            "id",
            "Token",
            "is_doctor",
            "profile_pic",
            "phone",
            
        ]
        extra_kwargs = {"is_doctor":{"read_only":True}}

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)
        
        if not user:
            if not User.objects.filter(email=email).exists():
                return {
                    "email": "هذا الاميل غير موجود",
                    "username": "user.username",
                }
            return {
                "email": " كلمة السر خاطئة",
                "username": "user.username",
            }
        
        if not user.is_verified:
            token = RefreshToken.for_user(user)
            current_site = get_current_site(self.context["request"]).domain
            relativeLink = reverse("auth:verify")
            absurl = (
                "http://"+current_site + relativeLink +"?token="+ str(token)
            )
            context = {"name": user.username, "url": str(absurl)}
            rendered = render_to_string("verify.html", context)
            data = {
                "body": rendered,
                "to": [user.email],
                "subject": "Code for verify",
            }
            Util.send_email_without_file(**data, html=True)
            return {
                "email": "فعل اميلك من خلال الرسالة التي ارسلت الى اميلك",
                "username": "user.username",
                
            }
        tt, token = Token.objects.get_or_create(user=user)
        return {
            "email": user.email,
            "username": user.username,
            "Token": tt.key,
            "is_doctor":user.is_doctor,
            "id":user.id,
            "profile_pic":user.profile_pic,
            "phone":user.phone

        }

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ["email"]


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()
    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["token"].strip()
        return attrs

    def save(self, **kwargs):

        try:
            t = Token.objects.filter(key=self.token)
            if t.exists():
                t[0].delete()
                return True
        except :
            return False

# class LoginSerializer(LoginSerializer):
#     username = None

# User = get_user_model()

# from dj_rest_auth.serializers import TokenSerializer

# class DetailedTokenSerializer(TokenSerializer):
#     status = serializers.SerializerMethodField()
#     message = serializers.SerializerMethodField()

#     id = serializers.IntegerField(source="user.id")
#     name = serializers.CharField(source="user.username")
#     email = serializers.CharField(source="user.email")
#     phone = serializers.CharField(source="user.phone")
#     image = serializers.SerializerMethodField()
#     is_doctor = serializers.BooleanField(source="user.is_doctor")
    
#     token = serializers.CharField(source="key")
    
#     class Meta(TokenSerializer.Meta):
#         fields = ["status", "message", "id", "name", "email","phone", "image", "is_doctor", "token"]
    
#     def get_status(self, obj):
#         return True if obj else False

#     def get_message(self, obj):
#         # return "تم تسجيل الدخول بنجاح" if obj else "خطأ في البريد الالكتروني او كلمة المرور"
#         return settings.LOGIN_SUCCESS_MESSAGE
    
#     def get_image(self, obj):
#         if obj.user.profile_pic:
#             return obj.user.profile_pic.url
#         else:
#             return obj.user.default_image_url()

# class DoctorCustomRegistrationSerializer(RegisterSerializer):
#     phone = serializers.CharField(required=True)

#     password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
#     password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
#     def get_cleaned_data(self):
#         data = super().get_cleaned_data()
#         print(data)
#         extra_data = {
#             "phone": self.validated_data.get("phone", ""),
#         }
#         data.update(extra_data)
#         return data

#     def save(self, request):
#         data = self.get_cleaned_data()
#         phone = data.get("phone")

#         user = super().save(request)
#         # user.is_doctor = True
#         user.phone = phone
#         user.save()
        
#         doctor = Doctor(doctor=user)

#         doctor.save()

#         return user


# class CustomPatientRegistrationSerializer(RegisterSerializer):
#     phone = serializers.CharField(required=True)

#     password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
#     password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

#     def get_cleaned_data(self):
#         data = super().get_cleaned_data()

#         extra_data = {
#             "phone": self.validated_data.get("phone", ""),
#         }
    
#         data.update(extra_data)
#         return data

#     def save(self, request):
#         data = self.get_cleaned_data()

#         phone = data.get("phone")
        
#         user = super().save(request)
#         user.is_patient = True
#         user.phone = phone
        
#         user.save()

#         patient = Patient(
#             patient=user,
#         )
#         patient.save()
#         return user

class LicenseSerializer(serializers.ModelSerializer):
    license_pic = serializers.ImageField(write_only=True)
    face_pic = serializers.ImageField(write_only=True)
    class Meta:
        model = Doctor
        fields = ('license_pic','face_pic')

class LicenseSerializer_(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['license_pic']
class UserProfileSerializer(serializers.ModelSerializer):
    licen = LicenseSerializer_(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username','email', 'profile_pic', 'phone','licen')

class statusSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['is_doctor','is_patient']