from django.contrib import admin
from django.urls import path, include
from .views import CheckImei, CheckBalance, GetServices
urlpatterns = [
    path('check-imei/', CheckImei.as_view()),
    path('balance/', CheckBalance.as_view()),
    path('services/', GetServices.as_view()),
]
