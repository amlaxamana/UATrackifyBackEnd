from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('admin', 'Administrator'),
        ]
    )
    
    organization = models.CharField(max_length=255, null=True, blank=True)
    office = models.CharField(max_length=255, null=True, blank=True)

    
class FormRegistration(models.Model):
    STATUS_CHOICES = [
        ('C', 'Completed'),
        ('NS', 'Not Started'),
        ('IP', 'In Progress'),
    ]
    event_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    event_date = models.DateField(max_length=10)
    attach_document = models.FileField(upload_to='documents/')
    status_osa = models.CharField(max_length=3, choices=STATUS_CHOICES, default='NS')
    osa_note = models.CharField(max_length=200, blank=True, null=True)
    status_vpaa = models.CharField(max_length=3, choices=STATUS_CHOICES, default='NS')
    vpaa_note = models.CharField(max_length=200, blank=True, null=True)
    status_finance = models.CharField(max_length=3, choices=STATUS_CHOICES, default='NS')
    finance_note = models.CharField(max_length=200, blank=True, null=True)
    status_vpa = models.CharField(max_length=3, choices=STATUS_CHOICES, default='NS')
    vpa_note = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.CharField(max_length=300 , blank=True, null=True)
    
    def __str__(self):
        return f"{self.event_name} {self.contact_person}"