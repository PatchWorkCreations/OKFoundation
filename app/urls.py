from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('login', login_user, name='login'),
    path('register', register_user, name='register'),
    path('lgout', logout_user, name='logout'),
    path('donate', donate_user, name='donate'),
]
