from django.contrib import admin
from .models import CustomUser,  Case, MedicalHistory, Treatment, LabResult, Immunization, CheckUp
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Case)
admin.site.register(MedicalHistory)
admin.site.register(Treatment)
admin.site.register(LabResult)
admin.site.register(Immunization)
admin.site.register(CheckUp)