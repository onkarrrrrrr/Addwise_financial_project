import json
import os
import time
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import CareerApplicationForm, RoleForm
from .models import Appointment, CareerApplication, Role

_GOOGLE_REVIEWS_CACHE = {"expires": 0, "data": None}
_GOOGLE_REVIEWS_TTL_SECONDS = 60 * 60


def _build_reviews_payload(payload):
    result = payload.get("result", {})
    rating = float(result.get("rating") or 0)
    rating_int = max(0, min(5, int(round(rating))))
    reviews = []
    for review in result.get("reviews", []):
        text = review.get("text", "")
        preview = text if len(text) <= 160 else f"{text[:157]}..."
        author = review.get("author_name", "Anonymous")
        review_rating = int(review.get("rating") or 0)
        reviews.append(
            {
                "author_name": author,
                "initial": author[:1].upper() if author else "A",
                "profile_photo_url": review.get("profile_photo_url"),
                "time": review.get("relative_time_description", ""),
                "rating_int": max(0, min(5, review_rating)),
                "preview": preview,
            }
        )
    return {
        "name": result.get("name", "Addwise Financials"),
        "address": result.get("formatted_address", ""),
        "rating": rating,
        "rating_int": rating_int,
        "user_ratings_total": int(result.get("user_ratings_total") or 0),
        "reviews": reviews,
        "star_range": [1, 2, 3, 4, 5],
    }


def _get_google_reviews():
    now = time.time()
    cached = _GOOGLE_REVIEWS_CACHE.get("data")
    if cached and now < _GOOGLE_REVIEWS_CACHE.get("expires", 0):
        return cached

    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    place_id = os.getenv("GOOGLE_PLACE_ID")
    if not api_key or not place_id:
        return None

    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,reviews,formatted_address",
        "reviews_sort": "most_relevant",
        "key": api_key,
    }
    url = "https://maps.googleapis.com/maps/api/place/details/json?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=6) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    if payload.get("status") != "OK":
        return None

    data = _build_reviews_payload(payload)
    _GOOGLE_REVIEWS_CACHE["data"] = data
    _GOOGLE_REVIEWS_CACHE["expires"] = now + _GOOGLE_REVIEWS_TTL_SECONDS
    return data


def _get_fallback_reviews():
    reviews = [
        {
            "author_name": "Harshad Deodhar",
            "initial": "H",
            "profile_photo_url": None,
            "time": "5 months ago",
            "rating_int": 5,
            "preview": "I had an excellent experience with this finance company. The team is knowledgeable, transparent, and very supportive throughout the process...",
        },
        {
            "author_name": "Digambar Deshpande",
            "initial": "D",
            "profile_photo_url": None,
            "time": "3 years ago",
            "rating_int": 5,
            "preview": "Got reference from friend, and still he helped me without any expectations. The 360 degree guidance was very helpful...",
        },
        {
            "author_name": "Deepak Pawar",
            "initial": "D",
            "profile_photo_url": None,
            "time": "5 years ago",
            "rating_int": 5,
            "preview": "Positive experience and clear guidance...",
        },
        {
            "author_name": "Nilesh Valand",
            "initial": "N",
            "profile_photo_url": None,
            "time": "6 months ago",
            "rating_int": 5,
            "preview": "We appreciate your support and trust...",
        },
        {
            "author_name": "Tanvi K",
            "initial": "T",
            "profile_photo_url": None,
            "time": "1 year ago",
            "rating_int": 5,
            "preview": "Thank you for your rating. If there is anything we can do to improve, please let us know...",
        },
    ]
    return {
        "name": "Addwise Financials",
        "address": "Ground Floor, Janaki Building, Bhandarkar Rd, near Kamala Nehru Park, opp. Bandhan Bank, Deccan Gymkhana, Pune, Maharashtra 411004, India",
        "rating": 5.0,
        "rating_int": 5,
        "user_ratings_total": 5,
        "reviews": reviews,
        "star_range": [1, 2, 3, 4, 5],
    }


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
    return render(request, 'leads/appointment.html', {'success': success})


@login_required(login_url='applications_login')
def appointments_list(request):
    status = request.GET.get('status', 'all')
    appointments = Appointment.objects.all().order_by('-created_at')
    if status != 'all':
        appointments = appointments.filter(status=status)
    status_counts = {
        'all': Appointment.objects.count(),
        Appointment.STATUS_NEW: Appointment.objects.filter(status=Appointment.STATUS_NEW).count(),
        Appointment.STATUS_COMPLETED: Appointment.objects.filter(status=Appointment.STATUS_COMPLETED).count(),
        Appointment.STATUS_CANCELED: Appointment.objects.filter(status=Appointment.STATUS_CANCELED).count(),
    }
    return render(request, 'leads/appointments_list.html', {'appointments': appointments, 'status': status, 'status_counts': status_counts})


@login_required(login_url='applications_login')
def appointment_detail(request, pk):
    appointment_obj = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        # Handle marking completed and adding a note or deleting
        if 'save_note' in request.POST:
            note = request.POST.get('note', '')
            appointment_obj.note = note
            if request.POST.get('mark') == 'completed':
                appointment_obj.status = Appointment.STATUS_COMPLETED
                appointment_obj.reviewed_at = timezone.now()
            appointment_obj.save(update_fields=['note', 'status', 'reviewed_at'])
            return redirect('appointment_detail', pk=appointment_obj.pk)
        elif 'delete' in request.POST:
            appointment_obj.delete()
            return redirect('appointments_list')
    return render(request, 'leads/appointment_detail.html', {'appointment': appointment_obj})


@login_required(login_url='applications_login')
def appointment_delete(request, pk):
    appointment_obj = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment_obj.delete()
        return redirect('appointments_list')
    return redirect('appointment_detail', pk=pk)

def home_view(request):
    reviews_data = _get_google_reviews() or _get_fallback_reviews()
    place_id = os.getenv("GOOGLE_PLACE_ID")
    review_url = (
        f"https://search.google.com/local/writereview?placeid={place_id}"
        if place_id
        else "https://www.google.com/maps"
    )
    reviews_data["review_url"] = review_url
    return render(request, 'leads/home.html', {"reviews_data": reviews_data})

def services_view(request):
    return render(request, 'leads/services.html')

def about_view(request):
    return render(request, 'leads/about.html')


def contact_view(request):
    return render(request, 'leads/contact.html')


def calculators_view(request):
    """Display calculators page with embedded external site"""
    return render(request, 'leads/calculators.html')


def career_view(request):
    submitted = request.GET.get('submitted') == '1'
    role_id = request.GET.get('role', '')
    active_roles = Role.objects.filter(is_active=True).order_by('name')
    
    # Process responsibilities to split by newlines
    for role in active_roles:
        if role.responsibilities:
            role.responsibilities_list = [r.strip() for r in role.responsibilities.split('\n') if r.strip()]
        else:
            role.responsibilities_list = []
    
    if request.method == 'POST':
        form = CareerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            _send_career_submission_emails(application)
            return redirect(f"{reverse('career')}?submitted=1")
    else:
        initial_data = {}
        if role_id:
            try:
                initial_data['role'] = int(role_id)
            except (ValueError, TypeError):
                pass
        form = CareerApplicationForm(initial=initial_data)
    
    return render(
        request,
        'leads/career.html',
        {
            'form': form,
            'submitted': submitted,
            'active_roles': active_roles,
        },
    )


@login_required(login_url='applications_login')
def applications_list(request):
    from itertools import groupby
    status = request.GET.get('status', 'all')
    applications = CareerApplication.objects.all().select_related('role').order_by('role__name', '-created_at')
    if status != 'all':
        applications = applications.filter(status=status)
    status_counts = {
        'all': CareerApplication.objects.count(),
        CareerApplication.STATUS_NEW: CareerApplication.objects.filter(
            status=CareerApplication.STATUS_NEW
        ).count(),
        CareerApplication.STATUS_HOLD: CareerApplication.objects.filter(
            status=CareerApplication.STATUS_HOLD
        ).count(),
        CareerApplication.STATUS_ACCEPTED: CareerApplication.objects.filter(
            status=CareerApplication.STATUS_ACCEPTED
        ).count(),
        CareerApplication.STATUS_REJECTED: CareerApplication.objects.filter(
            status=CareerApplication.STATUS_REJECTED
        ).count(),
    }
    # Group applications by role
    grouped_applications = {}
    for role, group in groupby(applications, key=lambda x: x.role):
        grouped_applications[role] = list(group)
    
    return render(
        request,
        'leads/applications_list.html',
        {
            'grouped_applications': grouped_applications,
            'status': status,
            'status_counts': status_counts,
        },
    )


@login_required(login_url='applications_login')
def applications_delete_by_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        applications = CareerApplication.objects.filter(role=role)
        for application in applications:
            if application.resume:
                application.resume.delete(save=False)
        applications.delete()
    return redirect('applications_list')


@login_required(login_url='applications_login')
def applications_delete_all(request):
    if request.method == 'POST':
        applications = CareerApplication.objects.all()
        for application in applications:
            if application.resume:
                application.resume.delete(save=False)
        applications.delete()
    return redirect('applications_list')


@login_required(login_url='applications_login')
def application_detail(request, pk):
    application = get_object_or_404(CareerApplication, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        status_map = {
            'hold': CareerApplication.STATUS_HOLD,
            'accept': CareerApplication.STATUS_ACCEPTED,
            'reject': CareerApplication.STATUS_REJECTED,
        }
        if action in status_map:
            new_status = status_map[action]
            if application.status != new_status:
                application.status = new_status
                application.reviewed_at = timezone.now()
                application.save(update_fields=['status', 'reviewed_at', 'updated_at'])
                if new_status in [
                    CareerApplication.STATUS_ACCEPTED,
                    CareerApplication.STATUS_REJECTED,
                ]:
                    _send_career_decision_email(application)
            return redirect('application_detail', pk=application.pk)
    return render(
        request,
        'leads/application_detail.html',
        {'application': application},
    )


@login_required(login_url='applications_login')
def application_delete(request, pk):
    application = get_object_or_404(CareerApplication, pk=pk)
    if request.method == 'POST':
        # Delete the stored PDF file
        if application.resume:
            application.resume.delete(save=False)
        application.delete()
        return redirect('applications_list')
    return redirect('application_detail', pk=pk)


# ========== ROLE MANAGEMENT CRUD VIEWS ==========

@login_required(login_url='applications_login')
def roles_list(request):
    """List all roles with management options"""
    roles = Role.objects.all().order_by('-created_at')
    return render(request, 'leads/roles_list.html', {'roles': roles})


@login_required(login_url='applications_login')
def role_create(request):
    """Create a new role"""
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            return redirect('role_detail', pk=role.pk)
    else:
        form = RoleForm()
    return render(request, 'leads/role_form.html', {'form': form, 'action': 'Create'})


@login_required(login_url='applications_login')
def role_detail(request, pk):
    """View role details"""
    role = get_object_or_404(Role, pk=pk)
    applications_count = role.applications.count()
    return render(
        request,
        'leads/role_detail.html',
        {'role': role, 'applications_count': applications_count}
    )


@login_required(login_url='applications_login')
def role_edit(request, pk):
    """Edit an existing role"""
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role_detail', pk=role.pk)
    else:
        form = RoleForm(instance=role)
    return render(
        request,
        'leads/role_form.html',
        {'form': form, 'action': 'Edit', 'role': role}
    )


@login_required(login_url='applications_login')
def role_delete(request, pk):
    """Delete a role"""
    role = get_object_or_404(Role, pk=pk)
    applications_count = role.applications.count()
    
    if applications_count > 0:
        # Can't delete role with active applications
        return render(
            request,
            'leads/role_delete_error.html',
            {'role': role, 'applications_count': applications_count}
        )
    
    if request.method == 'POST':
        role.delete()
        return redirect('roles_list')
    
    return render(request, 'leads/role_confirm_delete.html', {'role': role})


def _send_career_submission_emails(application):
    applicant_subject = 'We received your application'
    applicant_message = (
        'Hi {name},\n\n'
        'Thank you for applying to Addwise Financials. We have received your application '
        'and our team will review it shortly.\n\n'
        'Regards,\n'
        'Addwise Financials'
    ).format(name=application.full_name)
    _send_mail(applicant_subject, applicant_message, [application.email])

    if settings.CAREERS_NOTIFICATION_EMAILS:
        team_subject = 'New career application received'
        team_message = (
            'A new career application was submitted.\n\n'
            'Name: {name}\n'
            'Email: {email}\n'
            'Location: {location}\n'
            'College: {college}\n\n'
            'Review: {review_url}\n'
        ).format(
            name=application.full_name,
            email=application.email,
            location=application.location,
            college=application.college,
            review_url=f"/applications/{application.pk}/",
        )
        _send_mail(team_subject, team_message, settings.CAREERS_NOTIFICATION_EMAILS)


def _send_career_decision_email(application):
    if application.status == CareerApplication.STATUS_ACCEPTED:
        subject = 'Your application status update'
        message = (
            'Hi {name},\n\n'
            'We are pleased to share that your application has been accepted. '
            'Our team will reach out to you with the next steps.\n\n'
            'Regards,\n'
            'Addwise Financials'
        ).format(name=application.full_name)
    else:
        subject = 'Your application status update'
        message = (
            'Hi {name},\n\n'
            'Thank you for applying to Addwise Financials. After review, we will not be '
            'moving forward at this time. We appreciate your interest and wish you the best.\n\n'
            'Regards,\n'
            'Addwise Financials'
        ).format(name=application.full_name)
    _send_mail(subject, message, [application.email])


def _send_mail(subject, message, recipients):
    if not recipients:
        return
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=True,
    )
