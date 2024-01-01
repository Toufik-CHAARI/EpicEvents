from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import sentry_sdk



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('commercial', 'Commercial'),
        ('support', 'Support'),
        ('management', 'Management'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    def __str__(self):
        return self.username

@receiver(post_save, sender=CustomUser)
@receiver(post_delete, sender=CustomUser)
def model_changes(sender, instance, **kwargs):
    if 'created' in kwargs:
        action = "created" if kwargs['created'] else "updated"
    else:
        action = "deleted"

    sentry_sdk.capture_message(f"{sender.__name__} {action}: {instance.id}")
