from django.shortcuts import render
from .models import Appointment


def appointment(request):
    success = False
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        service = request.POST.get('service', '')
        message = request.POST.get('message', '')

        Appointment.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            service=service,
            message=message,
        )
        success = True

def home_view(request):
    return render(request, 'leads/home.html')

def services_view(request):
    return render(request, 'leads/services.html')

def about_view(request):
    return render(request, 'leads/about.html')

    return render(request, 'leads/appointment.html', {'success': success})
