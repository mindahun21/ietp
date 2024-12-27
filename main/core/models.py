from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from patients.models import Patient

# Create your models here.


class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'admin'),
        ('doctor', 'doctor'),
        ('nurse', 'nurse'),
    ]

    role = models.CharField(max_length=10, choices=ROLES, default='nurse')

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

    

class Case(models.Model):
    STATUS_CHOICES = [
        ('open', 'open'),
        ('closed', 'closed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='cases')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    initial_diagnosis = models.JSONField(blank=True, null=True)
    treatment_plan = models.JSONField(blank=True, null=True)
    closure_info = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def close_case(self):
        """
        Marks the case as closed, sets the end date, and optionally saves closure information.
        """
        self.status = 'closed'
        self.end_date = self.end_date or timezone.now().date()  # Use today's date if not set
        self.save()


    def __str__(self):
        return f"Case for: {self.patient.full_name} Status: {self.status}."

    class Meta:
        ordering = ['-start_date']

class MedicalHistory(models.Model): 
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_history')
    history = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Medical History for {self.patient.full_name}"
    
class Treatment(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='treatments')
    treatment_type = models.CharField(max_length=100)
    description = models.JSONField(blank=True, null=True)
    treatment_name = models.CharField(max_length=100)
    treatment_date = models.DateField(auto_now_add=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='treatments')
    def __str__(self):
        return f"Treatment for {self.case.patient.full_name}"
    
class LabResult(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=100)
    test_date = models.DateField()
    result = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Lab Result for {self.treatment.case.patient.full_name}"
    
class Immunization(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='immunizations')
    vaccine_name = models.CharField(max_length=100)
    vaccine_date = models.DateField()
    description = models.JSONField(blank=True, null=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='immunizations')

    

class CheckUp(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='checkups')
    nurse = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='checkups', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    bp = models.CharField(max_length=20,blank=True, null=True)
    pr  = models.CharField(max_length=20,blank=True, null=True)
    rr = models.CharField(max_length=20,blank=True, null=True)
    t= models.CharField(max_length=20,blank=True, null=True)
    input = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    