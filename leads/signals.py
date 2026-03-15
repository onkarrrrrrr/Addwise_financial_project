from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment

@receiver(post_save, sender=Appointment)
def send_appointment_emails(sender, instance, created, **kwargs):
    # 'created' True tabhi hoga jab pehli baar naya form/appointment save hoga
    if created:
        try:
            # ---------------------------------------------------------
            # 1. CLIENT KO MAIL (Jo customer form bharega usko jayega)
            # ---------------------------------------------------------
            client_subject = "Appointment Confirmed - Addwise Financials"
            client_message = (
                f"Namaste {instance.full_name},\n\n"
                f"Humne aapka {instance.service} ke liye request receive kar liya hai. "
                f"Hamari team jald hi aapse {instance.phone} par sampark karegi.\n\n"
                f"Thank You,\n"
                f"Team Addwise Financials"
            )
            
            send_mail(
                subject=client_subject,
                message=client_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email], # Customer ka email jo form me aaya
                fail_silently=False,
            )

            # ---------------------------------------------------------
            # 2. ADMIN KO MAIL (Aapko alert aayega ki nayi lead aayi hai)
            # ---------------------------------------------------------
            admin_subject = f"New Lead Alert: {instance.full_name}"
            admin_message = (
                f"Website par ek nayi lead aayi hai!\n\n"
                f"Name: {instance.full_name}\n"
                f"Phone: {instance.phone}\n"
                f"Email: {instance.email}\n"
                f"Service: {instance.service}\n\n"
                f"Please check the admin panel."
            )
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['satyampathrikar2007@gmail.com'], # <-- Admin ki email ID
                fail_silently=False,
            )
            
            print(f"Success: {instance.full_name} ke liye mail bhej diya gaya hai!")

        except Exception as e:
            # Agar koi error aati hai (jaise net band ho ya password galat ho), toh terminal me dikhegi
            print(f"Mail bhejne me error aayi: {e}")