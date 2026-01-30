from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

