import django_filters
from .models import Patient
from django.forms import TextInput, Select, NumberInput, BooleanField

class PatientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name='full_name', 
        label='Search by Name', 
        lookup_expr='icontains',
        widget=TextInput(attrs={
            'class': ' w-full ',
            'placeholder':'Enter name'
        })
        )
    gender = django_filters.ChoiceFilter(
        choices=Patient.GENDER_CHOICES,
        widget=Select(attrs={
            'class': 'w-full'
        })
        )
    age = django_filters.NumberFilter(
        label='Exact age',
        widget=NumberInput(attrs={
          'class':'w-full',
        })
        )
    age_lt = django_filters.NumberFilter(
        field_name='age', 
        lookup_expr='lt',
        widget=NumberInput(attrs={
          'class':'w-full',
        })
      )
    age_gt = django_filters.NumberFilter(
        field_name='age', 
        lookup_expr='gt',
        widget=NumberInput(attrs={
          'class':'w-full',
        })
      )
    is_active = django_filters.BooleanFilter(
        field_name='is_active',
        label='Active Patients Only',
        widget=django_filters.widgets.BooleanWidget()
    )


    class Meta:
        model = Patient
        fields = ['search', 'gender', 'age', 'is_active']
