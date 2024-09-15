from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment, Video

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Comment Added',
            f'A new comment was added by {instance.user.email} on your post.',
            settings.DEFAULT_FROM_EMAIL,
            [instance.blog.author.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Video)
def log_video_creation(sender, instance, created, **kwargs):
    if created:
        print(f'New video added: {instance.name}')
