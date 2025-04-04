from django.contrib import admin
from .models import Patient, Insurance, Bed

# Register your models here.
admin.site.register(Patient)
admin.site.register(Insurance)
admin.site.register(Bed)


