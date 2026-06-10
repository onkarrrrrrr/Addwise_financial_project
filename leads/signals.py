from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment

@receiver(post_save, sender=Appointment)
def send_appointment_emails(sender, instance, created, **kwargs):
    if created:
        try:
            # 1. CLIENT EMAIL (English)
            client_subject = "Appointment Confirmed - Addwise Financials"
            client_message = (
                f"Dear {instance.full_name},\n\n"
                f"We have successfully received your request for {instance.get_service_display()}. "
                f"Our team will contact you shortly on {instance.phone}.\n\n"
                f"Thank You,\n"
                f"Team Addwise Financials"
            )
            
            send_mail(
                subject=client_subject,
                message=client_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )

            # 2. ADMIN EMAIL (English)
            admin_subject = f"New Lead Alert: {instance.full_name}"
            admin_message = (
                f"A new lead has been generated on the website!\n\n"
                f"Name: {instance.full_name}\n"
                f"Phone: {instance.phone}\n"
                f"Email: {instance.email}\n"
                f"Service: {instance.get_service_display()}\n"
                f"Message: {instance.message}\n\n"
                f"Please log in to the admin panel for more details."
            )
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['connect@addwisefin.com'], 
                fail_silently=False,
            )
            
            print(f"Success: Email sent for {instance.full_name}")

        except Exception as e:
            print(f"Error sending mail: {e}")