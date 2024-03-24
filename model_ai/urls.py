from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.PredictAPIView.as_view(), name='predictc'),
    # path('predict/', views.predict, name='predict'),
]
