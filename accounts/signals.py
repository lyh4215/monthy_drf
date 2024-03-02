from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User

@receiver(post_save, sender=User)
def set_username_from_email(sender, instance, created, **kwargs):
    if created and not instance.username:
        instance.username = instance.email
        instance.save()
