import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


def career_resume_upload_path(instance, filename):
    safe_name = f"{uuid.uuid4().hex}_{filename}"
    role_folder = instance.role.lower().replace(' ', '_') if instance.role else 'general'
    return f"career/resumes/{role_folder}/{safe_name}"

class Appointment(models.Model):
    # Dropdown choices for services
    SERVICE_CHOICES = [
        ('HOME', 'Home Loan'),
        ('BIZ', 'Business Loan'),
        ('SIP', 'SIP/Investment'),
        ('LAP', 'Loan Against Property'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # Kab book kiya

    def __str__(self):
        return f"{self.full_name} - {self.service}"


class CareerApplication(models.Model):
    ROLE_WEALTH_ANALYST = 'Wealth Analyst'
    ROLE_RELATIONSHIP_MANAGER = 'Relationship Manager'
    ROLE_OPERATIONS_EXECUTIVE = 'Operations Executive'
    ROLE_CHOICES = [
        (ROLE_WEALTH_ANALYST, 'Wealth Analyst'),
        (ROLE_RELATIONSHIP_MANAGER, 'Relationship Manager'),
        (ROLE_OPERATIONS_EXECUTIVE, 'Operations Executive'),
        ('Other', 'Other'),
    ]
    
    STATUS_NEW = 'NEW'
    STATUS_HOLD = 'HOLD'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_HOLD, 'Hold'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    location = models.CharField(max_length=120)
    college = models.CharField(max_length=160)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=ROLE_WEALTH_ANALYST)
    resume = models.FileField(
        upload_to=career_resume_upload_path,
        validators=[FileExtensionValidator(['pdf'])],
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_NEW)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.status}"