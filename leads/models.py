from django.db import models

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