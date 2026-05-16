from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('about/', views.about_view, name='about'),
    # Yahan maine 'appointment_view' ko hata kar sirf 'appointment' kar diya hai 👇
    path('appointment/', views.appointment, name='appointment'), 
]