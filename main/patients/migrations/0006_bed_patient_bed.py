# Generated by Django 5.1.4 on 2024-12-25 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_alter_patient_assigned_nurses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, editable=False, max_length=100, unique=True)),
                ('room_number', models.IntegerField()),
                ('bed_number', models.IntegerField()),
                ('status', models.CharField(choices=[('available', 'available'), ('occupied', 'occupied'), ('maintenance', 'maintenance')], default='available', max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='bed',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient', to='patients.bed'),
        ),
    ]