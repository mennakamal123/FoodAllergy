# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
# from dj_rest_auth.registration.views import RegisterView, SocialLoginView
# from dj_rest_auth.social_serializers import TwitterLoginSerializer
# from rest_framework import  viewsets
# from rest_framework.response import Response
# from .serializers import (
#     CustomPatientRegistrationSerializer,
#     DoctorCustomRegistrationSerializer,
#     DetailedTokenSerializer,
#     UserProfileSerializer,
# )
# from rest_framework import generics
# from .models import User, Doctor
# from .serializers import LicenseSerializer
# from rest_framework.generics import UpdateAPIView
# from rest_framework.permissions import IsAuthenticated
# # Create your views here.

#     # Create your views here.

# # ovveride LoginView dj_rest_auth login view to add data to Response body
# from dj_rest_auth.views import LoginView

# class CustomLoginView(LoginView):
#     def get_response_serializer(self):
#         return DetailedTokenSerializer

# class DoctorRegistrationView(RegisterView, viewsets.GenericViewSet):
#     serializer_class = DoctorCustomRegistrationSerializer


# class PatientRegistrationView(RegisterView, viewsets.GenericViewSet):
#     serializer_class = CustomPatientRegistrationSerializer

# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserProfileSerializer
#     http_method_names= ['get']
    
#     def retrieve(self, request, pk=None):
#         user = User.objects.get(id=pk)
#         serializer = self.serializer_class(user)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         user = request.user
#         serializer = self.serializer_class(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)


# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter

# class TwitterLogin(SocialLoginView):
#     serializer_class = TwitterLoginSerializer
#     adapter_class = TwitterOAuthAdapter


# class GitHubLogin(SocialLoginView):
#     adapter_class = GitHubOAuth2Adapter
#     callback_url = "CALLBACK_URL_YOU_SET_ON_GITHUB"
#     client_class = OAuth2Client

# class LicenseView(generics.GenericAPIView):
#     serializer_class = LicenseSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user=request.user
#         data=request.data
#         ser = LicenseSerializer(data=data)
#         if ser.is_valid():
#             user.is_doctor=True
#             user.save()            
#             doctor,_=Doctor.objects.get_or_create(doctor=user)
#             doctor.license_pic = request.data['license_pic']
#             doctor.face_pic = request.data['face_pic']
#             doctor.save()
#             ser_ = LicenseSerializer(doctor)
#             return Response(ser_.data)
#         else:
#             return Response(ser.errors)

# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
# from dj_rest_auth.registration.views import RegisterView, SocialLoginView
# from dj_rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import  viewsets
# from rest_framework.response import Response
# from .serializers import (
#     CustomPatientRegistrationSerializer,
#     DoctorCustomRegistrationSerializer,
#     DetailedTokenSerializer,
#     UserProfileSerializer,
# )
# from rest_framework import generics
# from .models import User, Doctor
# from .serializers import LicenseSerializer
# from rest_framework.generics import UpdateAPIView
# from rest_framework.permissions import IsAuthenticated
# Create your views here.

    # Create your views here.

# ovveride LoginView dj_rest_auth login view to add data to Response body
# from dj_rest_auth.views import LoginView

# class CustomLoginView(LoginView):
#     def get_response_serializer(self):
#         return DetailedTokenSerializer

# class DoctorRegistrationView(RegisterView, viewsets.GenericViewSet):
#     serializer_class = DoctorCustomRegistrationSerializer


# class PatientRegistrationView(RegisterView, viewsets.GenericViewSet):
#     serializer_class = CustomPatientRegistrationSerializer




# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter

# class TwitterLogin(SocialLoginView):
#     serializer_class = TwitterLoginSerializer
#     adapter_class = TwitterOAuthAdapter


# class GitHubLogin(SocialLoginView):
#     adapter_class = GitHubOAuth2Adapter
#     callback_url = "CALLBACK_URL_YOU_SET_ON_GITHUB"
#     client_class = OAuth2Client
from rest_framework.permissions import IsAuthenticated
from logging import exception
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.authentication import TokenAuthentication
from django.template.loader import render_to_string
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework.authtoken.models import Token
import json
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from uuid import getnode as get_mac
import uuid
from rest_framework.decorators import action
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names= ['get', 'put']
    
    def retrieve(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    @action(
        detail=False, methods=['GET'],
        serializer_class=statusSerializers,
        permission_classes=[IsAuthenticated],)
    def status(self,request):
        user = request.user
        serializers = statusSerializers(user)
        return Response(serializers.data)

# Create your views here.

class RegisterView_as_doctor(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else :
            return Response(
                {
                    "status": False,
                    "message": "هذا الايميل موجود من قبل ",
                },
                status=status.HTTP_200_OK,
            )
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('auth:verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        context = {"name": user.username, "url":str(absurl)}
        rendered = render_to_string("verify.html", context)            
        data = {
            "body": rendered,
            "to": [user.email],
            "subject": "Code for verify",
        }
        create,_ = Doctor.objects.get_or_create(doctor=user)
        Util.send_email_without_file(**data, html=True)
        return Response(
                {
                    "status": True,
                    "message": "لقد تم انشاء ايميل وارسلنا رسالة تفعيل للايميل الخاص بك",
                },
                status=status.HTTP_200_OK,
            )

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else :
            return Response(
                {
                    "status": False,
                    "message": "هذا الايميل موجود من قبل ",
                },
                status=status.HTTP_200_OK,
            )
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('auth:verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        context = {"name": user.username, "url":str(absurl)}
        rendered = render_to_string("verify.html", context)            
        data = {
            "body": rendered,
            "to": [user.email],
            "subject": "Code for verify",
        }
        create,_ = Patient.objects.get_or_create(patient=user)
        Util.send_email_without_file(**data, html=True)
        return Response(
                {
                    "status": True,
                    "message": "لقد تم انشاء ايميل وارسلنا رسالة تفعيل للايميل الخاص بك",
                },
                status=status.HTTP_200_OK,
            )
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data, context={"request": request},)
        serializer.is_valid(raise_exception=True)
        if "Token" in serializer.data.keys():
            return Response(
                {
                    "status": True,
                    "message": "logged successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            r = serializer.data.get("email")
            return Response(
                {"status": False, "message": r, "data": {}}, status=status.HTTP_200_OK
            )


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse(
                "auth:restPassword", kwargs={"uidb64": uidb64, "token": token}
            )

            absurl = "http://" + current_site + relativeLink
            email_body = "Hello, \n Use link below to reset your password  \n" + absurl
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your passsword",
            }
            Util.send_email(data)
            return Response(
                {
                    "status": True,
                    "message": "We have sent you a link to reset your password",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": False, "message": "this email is not register"},
            status=status.HTTP_200_OK,
        )
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.save():
                return Response(
                    {"status": True, "message": "logout done"}, status=status.HTTP_200_OK
                )
            return Response(
                {"status": False, "message": "invalid token"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": False, "message": "invalid token"},
                status=status.HTTP_200_OK,
            )

class LicenseView(generics.GenericAPIView):
    serializer_class = LicenseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        data=request.data
        ser = LicenseSerializer(data=data)
        if ser.is_valid():
            user.is_doctor=True
            user.save()            
            doctor,_=Doctor.objects.get_or_create(doctor=user)
            doctor.license_pic = request.data['license_pic']
            doctor.face_pic = request.data['face_pic']
            doctor.save()
            ser_ = LicenseSerializer(doctor)
            return Response(ser_.data)
        else:
            return Response(ser.errors)
        
        
class RestPassword(APIView):
    def get(self, request, uidb64, token):
        return render(request, "pages/forgot-password.html")

    def post(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            password = request.data["password"]
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                context = {"message": "لقد انتهى مدة اللينك اطلب واحد اخر"}

                return render(request, "pages/ok.html", context)
            if len(password) <= 10:
                context = {"message": "كلمة السر يجب ان تزيد عن 10 احرف"}

                return render(request, "pages/forgot-password.html", context)
            user.set_password(password)
            user.is_verified = True
            user.save()
            context = {"message": " تم تغيير كلمة السر بنجاح"}
            return render(request, "pages/ok.html", context)
        except:
            context = {"message": "انتهى اللينك اطلب اخر"}

            return render(request, "pages/ok.html", context)
def test(request):
    try:
        token = request.GET.get("token", "")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            context = {"message": "Email has been activated successfully"}
            return render(request, "pages/ok.html", context=context)
        except jwt.ExpiredSignatureError as identifier:
            context = {"message": "Invalid link"}
            return render(request, "pages/ok.html", context=context)
    except:
        context = {"message": "you should have a link"}
        return render(request, "pages/ok.html", context=context)