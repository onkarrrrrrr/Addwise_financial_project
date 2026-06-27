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
    # Appointment (public form)
    path('appointment/', views.appointment, name='appointment'),

    # ─── Superadmin Login / Logout ─────────────────────────────────────────────
    path(
        'superadmin/login/',
        auth_views.LoginView.as_view(template_name='leads/applications_login.html'),
        name='applications_login',
    ),
    path('superadmin/logout/', views.superadmin_logout, name='superadmin_logout'),

    # ─── Superadmin Dashboard (root redirect) ──────────────────────────────────
    path('superadmin/', views.superadmin_redirect, name='superadmin_dashboard'),

    # ─── Appointment management ────────────────────────────────────────────────
    path('superadmin/appointments/', views.appointments_list, name='appointments_list'),
    path('superadmin/appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('superadmin/appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # ─── Career Applications ───────────────────────────────────────────────────
    path('superadmin/applications/', views.applications_list, name='applications_list'),
    path('superadmin/applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('superadmin/applications/<int:pk>/delete/', views.application_delete, name='application_delete'),
    path('superadmin/applications/delete-by-role/', views.applications_delete_by_role, name='applications_delete_by_role'),
    path('superadmin/applications/delete-all/', views.applications_delete_all, name='applications_delete_all'),

    # ─── Role management ───────────────────────────────────────────────────────
    path('superadmin/roles/', views.roles_list, name='roles_list'),
    path('superadmin/roles/create/', views.role_create, name='role_create'),
    path('superadmin/roles/<int:pk>/', views.role_detail, name='role_detail'),
    path('superadmin/roles/<int:pk>/edit/', views.role_edit, name='role_edit'),
    path('superadmin/roles/<int:pk>/delete/', views.role_delete, name='role_delete'),

    # Investor portal proxy routes
    path('investor-portal/', views.investor_portal_proxy, name='investor_portal_proxy_root'),
    path('investor-portal/<path:path>', views.investor_portal_proxy, name='investor_portal_proxy'),
]