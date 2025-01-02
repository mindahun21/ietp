from django.db import models
from django.conf import settings
import uuid



class Patient(models.Model):
    MARITAL_STATUS = [
        ('single', 'single'),
        ('married', 'married'),
        ('divorced', 'divorced'),
        ('widowed', 'widowed'),
    ] 
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]

    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, default='')
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True,null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, blank=True,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES) 
    age = models.IntegerField(blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True) 
    emergency_contact = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    assigned_nurses = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        limit_choices_to={'role': 'nurse'},  
        related_name='patients', 
        blank=True,
    )
    bed = models.OneToOneField('Bed', on_delete=models.SET_NULL, null=True, blank=True, related_name='patient')
    
    def __str__(self):
        return f"{self.full_name}"
    
class Bed(models.Model):
    STATUS =[
        ('available', 'available'),
        ('occupied', 'occupied'),
        ('maintenance', 'maintenance'),
    ]
    uuid = models.CharField(max_length=100, unique=True, editable=False, blank=True) 
    room_number = models.IntegerField()
    bed_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='available')

    def save(self, *args, **kwargs):
        if not self.uuid:  
            self.uuid = str(uuid.uuid4()) 
        super().save(*args, **kwargs)  

    def __str__(self):
            return f"Bed {self.bed_number} in Room {self.room_number}"

class Insurance(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="insurance")
    provider_name = models.CharField(max_length=100)  
    policy_number = models.CharField(max_length=100) 
    coverage_start_date = models.DateField() 
    coverage_end_date = models.DateField(null=True, blank=True)  
    coverage_details = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.provider_name} - {self.policy_number}"
    
class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()

    # TODO: add many tomay field with nurses