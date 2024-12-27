from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

class RegisteredUser(models.Model):
    email = models.EmailField(unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email  


class Airdrops(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    link = models.URLField()
    cost = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('ongoing', 'Ongoing Airdrops'),
            ('upcoming', 'Upcoming Airdrops'),
            ('ended', 'Ended Airdrops')
        ],
        default='ongoing'
    )
    reward_date = models.DateField()
    airdrop_confidentiality = models.CharField(
        max_length=20,
        choices=[
            ('confirmed', 'Confirmed'),
            ('not-confirmed', 'Not Confirmed')
        ],
        default='confirmed'
    )
    fund_raised = models.FloatField()
    backers = models.CharField(max_length=255)
    website = models.URLField()
    social_medias = models.JSONField()
    eligibility_checker = models.URLField()
    claim_airdrop = models.URLField()
    image = models.ImageField(upload_to='airdrops/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Step(models.Model):
    airdrop = models.ForeignKey(Airdrops, related_name='steps', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='steps/')

    def __str__(self):
        return f"Step for {self.airdrop.name}"
    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
@receiver(post_save, sender=BlogPost)
def send_new_blog_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New Blog Post: {instance.title}"
        plain_message = f"New blog post published: {instance.title}. Visit https://mastercrypto.org/blog/{instance.id} to read more."
        html_message = (
            f"<html><body>"
            f"<h1>New Blog Post: {instance.title}</h1>"
            f"<p>{instance.excerpt}</p>"
            f"<p>{instance.content[:100]}...</p>"
            f"<p><a href='https://mastercrypto.org/blog/{instance.id}' "
            f"style='padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;'>Read Full Blog</a></p>"
            f"<p>Best regards,<br>MasterCrypto Team</p>"
            f"</body></html>"
        )
        recipient_list = [user.email for user in RegisteredUser.objects.all()]

        if recipient_list:
            send_mail(
                subject=subject,
                message=plain_message,  # Plain text version
                from_email='Master Crypto <abelbk06@gmail.com>',
                recipient_list=recipient_list,
                fail_silently=False,
                html_message=html_message  # HTML content
            )
