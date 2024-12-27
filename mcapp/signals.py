from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Airdrops, RegisteredUser

@receiver(post_save, sender=Airdrops)
def send_airdrop_notification(sender, instance, created, **kwargs):
    if created:
        # Get all registered users
        users = RegisteredUser.objects.all()

        # Compose the email content
        subject = f"New Airdrop: {instance.name}"
        
        # HTML message with styling and a button
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #1a73e8;">New Airdrop: {instance.name}</h2>
                <p style="font-size: 16px;">Hello,</p>
                <p style="font-size: 16px;">We are excited to announce a new airdrop for you!</p>
                <p style="font-size: 16px;"><strong>Description:</strong> {instance.description}</p>
                <p style="font-size: 16px;"><strong>Start Date:</strong> {instance.date}</p>
                <p style="font-size: 16px;">Don't miss out on the opportunity. Click below to get more details:</p>
                
                <!-- Button with a link to the airdrop -->
                <a href="{instance.link}" style="background-color: #1a73e8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 18px; display: inline-block; margin-top: 20px;">
                    Claim Your Airdrop
                </a>
                
                <p style="font-size: 16px; margin-top: 30px;">Best regards,</p>
                <p style="font-size: 16px;">Master Crypto</p>
            </body>
        </html>
        """

        # Set the sender's name to "Master Crypto"
        from_email = 'Master Crypto <abelbk06@gmail.com>'

        # Send the email to each registered user
        for user in users:
            send_mail(
                subject,
                message='This is an HTML email. If you can see this, your email client does not support HTML emails.',
                from_email=from_email,
                recipient_list=[user.email],
                html_message=html_message  # Pass the HTML message here
            )
