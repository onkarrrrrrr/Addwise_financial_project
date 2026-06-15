import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


def career_resume_upload_path(instance, filename):
    safe_name = f"{uuid.uuid4().hex}_{filename}"
    role_folder = instance.role.name.lower().replace(' ', '_') if instance.role else 'general'
    return f"career/resumes/{role_folder}/{safe_name}"


class Role(models.Model):
    """
    Represents a job role/position that the company is hiring for.
    Has a complete job description that is mandatory.
    """
    name = models.CharField(max_length=100, unique=True)
    job_description = models.TextField(help_text="Complete job description (mandatory)")
    requirements = models.TextField(blank=True, help_text="Technical and soft skills requirements")
    responsibilities = models.TextField(blank=True, help_text="Key responsibilities")
    benefits = models.TextField(blank=True, help_text="Benefits and perks")
    is_active = models.BooleanField(default=True, help_text="If unchecked, this role won't appear on careers page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Appointment(models.Model):
    # Dropdown choices for services
    SERVICE_CHOICES = [
        ('WEALTH', 'Goal based Wealth creation solutions'),
        ('TERM', 'Term Insurance'),
        ('HEALTH', 'Health Insurance'),
        ('LOANS', 'Loans & Credit Solutions'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField(blank=True)
    # Management fields
    STATUS_NEW = 'NEW'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CANCELED = 'CANCELED'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELED, 'Canceled'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_NEW)
    note = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # Kab book kiya

    def __str__(self):
        return f"{self.full_name} - {self.service}"


class CareerApplication(models.Model):
    
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
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='applications')
    resume = models.FileField(
        upload_to=career_resume_upload_path,
        validators=[FileExtensionValidator(['pdf'])],
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_NEW)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.status}"