# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from django.conf import settings
# from django.conf.urls.static import static

# from .views import (DoctorRegistrationView,
#                     FacebookLogin, PatientRegistrationView, TwitterLogin, CustomLoginView,UserProfileViewSet,LicenseView)


# from dj_rest_auth.views import (
#     PasswordResetConfirmView,
#     PasswordResetView,
# )
# urlpatterns = [
#     path("auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
#     path("auth/twitter/", TwitterLogin.as_view(), name="twitter_login"),
# ]

# # app_name = "users"

# router = DefaultRouter()

# router.register(
#     "registration/doctor",
#     DoctorRegistrationView,
#     basename="register-doctor",
# )
# router.register(
#     "registration/patient",
#     PatientRegistrationView,
#     basename="register-patient",
# )
# router.register('user-profile', UserProfileViewSet, basename='user-profile')
# urlpatterns += [
#      path("", include(router.urls)),
#     path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
#     path(
#         "password/reset/confirm/<uidb64>/<token>/",
#         PasswordResetConfirmView.as_view(),
#         name="password_reset_confirm",
#     ),
#     path("loggin/", CustomLoginView.as_view(), name="login"),
#     path('lic/', LicenseView.as_view())

# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# from .views import (DoctorRegistrationView,
                    # FacebookLogin, PatientRegistrationView, TwitterLogin, CustomLoginView,UserProfileViewSet,LicenseView)


# from dj_rest_auth.views import (
    # PasswordResetConfirmView,
    # PasswordResetView,
# )
# urlpatterns = [
#     path("auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
#     path("auth/twitter/", TwitterLogin.as_view(), name="twitter_login"),
# ]

# app_name = "users"

# router = DefaultRouter()

# router.register(
#     "registration/doctor",
#     DoctorRegistrationView,
#     basename="register-doctor",
# )
# router.register(
#     "registration/patient",
#     PatientRegistrationView,
#     basename="register-patient",
# )
# router.register('user-profile', UserProfileViewSet, basename='user-profile')
# urlpatterns += [
#      path("", include(router.urls)),
#     path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
#     path(
#         "password/reset/confirm/<uidb64>/<token>/",
#         PasswordResetConfirmView.as_view(),
#         name="password_reset_confirm",
#     ),
#     path("loggin/", CustomLoginView.as_view(), name="login"),
#     path('lic/', LicenseView.as_view())

# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()

app_name = "auth"
router.register('user-profile', UserProfileViewSet, basename='user-profile')
urlpatterns= [
    path("", include(router.urls)),
    path('registerDoctor/', RegisterView_as_doctor.as_view(), name ="registerDoctor"),
    path('registerPatient/', RegisterView.as_view(), name ="registerPatient"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('lic/', LicenseView.as_view()),
    path('verify/',test, name='verify'),
    path("restPassword/<str:uidb64>/<str:token>/",  RestPassword.as_view() , name="restPassword"),
    
]