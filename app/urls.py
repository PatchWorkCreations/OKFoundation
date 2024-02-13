from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='homepage'),
    path('register', views.RegisterUser, name='register'),
    path('donate', views.DonateUser, name='donate'),
]
