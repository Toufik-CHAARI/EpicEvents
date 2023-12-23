from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('commercial', 'Commercial'),
        ('support', 'Support'),
        ('management', 'Management'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    def __str__(self):
        return self.username
