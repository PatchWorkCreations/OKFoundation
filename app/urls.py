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
    path('update_account_settings', update_account_settings, name='update_account_settings'),
    path('update_user', update_user, name='update_user'),
    path('fetch_user_details/<int:pk>/', fetch_user_details, name='fetch_user_details'),
    path('update_user_detail/<int:pk>/', update_user_detail, name='update_user_detail'),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('eventinyourcity', eventinyourcity, name='eventinyourcity'),
    path('volunteer', volunteer, name='volunteer'),
    path('engagement', engagement, name='engagement'),
    path('fun', fun, name='fun'),
]
