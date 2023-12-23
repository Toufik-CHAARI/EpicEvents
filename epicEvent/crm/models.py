from django.db import models
from authentication.models import CustomUser
from django.conf import settings

# Create your models here.
class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=255)
    creation_date = models.DateField()
    last_update = models.DateField()
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='clients')
    def __str__(self):
        return self.full_name

    
class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='contracts')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateField()
    is_signed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
        
    
   


class Event(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='events')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    support_contact = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='supported_events')
    location = models.CharField(max_length=255)
    attendees = models.IntegerField()
    notes = models.TextField()
    def __str__(self):
        return self.location


