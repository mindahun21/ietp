# Generated by Django 5.1.4 on 2024-12-25 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_bed_asigned_to'),
        ('patients', '0005_alter_patient_assigned_nurses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bed',
            name='asigned_to',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bed', to='patients.patient'),
        ),
    ]