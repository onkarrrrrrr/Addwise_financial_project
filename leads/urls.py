from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('disclaimer/', views.disclaimer_view, name='disclaimer'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('disclosure/', views.disclosure_view, name='disclosure'),
    path('code-of-conduct/', views.code_of_conduct_view, name='code_of_conduct'),
    path('calculators/', views.calculators_view, name='calculators'),
    path('careers/', views.career_view, name='career'),
    path(
        'applications/login/',
        auth_views.LoginView.as_view(template_name='leads/applications_login.html'),
        name='applications_login',
    ),
    # Role management routes
    path('roles/', views.roles_list, name='roles_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/<int:pk>/', views.role_detail, name='role_detail'),
    path('roles/<int:pk>/edit/', views.role_edit, name='role_edit'),
    path('roles/<int:pk>/delete/', views.role_delete, name='role_delete'),
    # Applications management routes
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/delete/', views.application_delete, name='application_delete'),
    path('applications/delete-by-role/', views.applications_delete_by_role, name='applications_delete_by_role'),
    path('applications/delete-all/', views.applications_delete_all, name='applications_delete_all'),
    # Appointment routes
    path('appointment/', views.appointment, name='appointment'), 
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    # Investor portal proxy routes
    path('investor-portal/', views.investor_portal_proxy, name='investor_portal_proxy_root'),
    path('investor-portal/<path:path>', views.investor_portal_proxy, name='investor_portal_proxy'),
]