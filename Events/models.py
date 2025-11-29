from django.db import models
from django.contrib.auth.models import AbstractUser

from Form import settings
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

    office = models.CharField(max_length=255, null=True, blank=True)

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
         return f"{self.first_name} {self.last_name} - {self.role}"

class Organization(models.Model):

        OrganizationName_Choices = [
        ('SSITE', 'SSITE'),
        ('UASAO', 'UASAO'),
        ('MCSA', 'MCSA'),
        ('JPIA', 'JPIA'),
        ('LTSP', 'LTSP'),
        ('BHS-PHS', 'BHS-PHS'),
        ('NSC', 'NSC'),
        ('JPPhA', 'JPPhA'),
        ('CRCYC', 'CRCYC'),
        ('CDW', 'CDW'),
        ('BATAS', 'BATAS'),
        ('CREATE', 'CREATE'),
        ('PICE', 'PICE'),
        ('AAA', 'AAA'),
        ('PIIE', 'PIIE'),
        ('BACC', 'BACC'),
        ('PSYCHSOC', 'PSYCHSOC'),
        ('LEAD', 'LEAD'),
        ('CHARMS', 'CHARMS'),
        ('ICpEP.se', 'ICpEP.se'),
        ('INA', 'INA'),
        ('UACSC', 'UACSC'),

    ]
        OrganizationName = models.CharField(max_length=255, choices= OrganizationName_Choices, null=True, blank=True, unique=True)
        def __str__(self):
            return self.OrganizationName

    

    
class FormRegistration(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE, # ⬅️ Changed from SET_NULL to CASCADE
        null=True, # Note: null=True is usually incompatible with CASCADE on a required field, 
                   # but kept here as it was in the previous code.
        blank=True,
        related_name='events'
    )

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