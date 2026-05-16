from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('about/', views.about_view, name='about'),
    path('appointment/', views.appointment_view, name='appointment'), # Tumhara form page
]