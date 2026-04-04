from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sip/', views.sip_calculator, name='sip_calculator'),
    path('lumpsum/', views.lumpsum_calculator, name='lumpsum_calculator'),
    path('step-up-sip/', views.step_up_sip, name='step_up_sip'),
    path('stepup-vs-normal/', views.stepup_vs_normal_sip, name='stepup_vs_normal_sip'),
    path('cost-of-delay/', views.cost_of_delay, name='cost_of_delay'),
    path('swp/', views.swp_calculator, name='swp_calculator'),
    path('emi/', views.emi_calculator, name='emi_calculator'),
    path('inflation/', views.inflation_calculator, name='inflation_calculator'),
    path('fd/', views.fd_calculator, name='fd_calculator'),
    path('cagr/', views.cagr_calculator, name='cagr_calculator'),
    path('dream-goal/', views.dream_goal_calculator, name='dream_goal_calculator'),
    path('net-worth/', views.net_worth_calculator, name='net_worth_calculator'),
    path('life-cover/', views.life_cover_calculator, name='life_cover_calculator'),
    path('retirement/', views.retirement_calculator, name='retirement_calculator'),
    path('stp/', views.stp_calculator, name='stp_calculator'),
]