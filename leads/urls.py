from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('careers/', views.career_view, name='career'),
    path(
        'applications/login/',
        auth_views.LoginView.as_view(template_name='leads/applications_login.html'),
        name='applications_login',
    ),
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/delete/', views.application_delete, name='application_delete'),
    path('applications/delete-by-role/', views.applications_delete_by_role, name='applications_delete_by_role'),
    path('applications/delete-all/', views.applications_delete_all, name='applications_delete_all'),
    # Yahan maine 'appointment_view' ko hata kar sirf 'appointment' kar diya hai 👇
    path('appointment/', views.appointment, name='appointment'), 
]