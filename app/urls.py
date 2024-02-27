from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('login', login_user, name='login'),
    # path('register', register_user, name='register'),
    path('logout', logout_user, name='logout'),
    path('donate', donate_user, name='donate'),
    path('johnstown2024', johnstown_2024_page, name='johnstown_2024'),
    path('registration', registration_page, name='registration'),
    path('dashboard', dashboard, name='dashboard'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('eventinyourcity', eventinyourcity, name='eventinyourcity'),
    path('volunteer', volunteer, name='volunteer'),
    path('engagement', engagement, name='engagement'),
]
