from django import forms
from .models import Patient, Bed

class AddEditPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'full_name', 
            'address', 
            'email', 
            'phone_number', 
            'marital_status', 
            'gender', 
            'age', 
            'date_of_birth', 
            'emergency_contact', 
            'is_active'
        ]

    def clean_email(self):
      email = self.cleaned_data.get('email')
      if email:
          # Exclude the current instance from the duplicate check
          queryset = Patient.objects.filter(email=email)
          if self.instance.pk:
              queryset = queryset.exclude(pk=self.instance.pk)
          if queryset.exists():
              raise forms.ValidationError('A patient with this email already exists.')
      return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom widgets if necessary
        self.fields['full_name'].widget.attrs.update({'class': 'w-full'})
        self.fields['address'].widget.attrs.update({'class': 'w-full'})
        self.fields['email'].widget.attrs.update({'class': 'w-full'})
        self.fields['phone_number'].widget.attrs.update({'class': 'w-full'})
        self.fields['marital_status'].widget.attrs.update({'class': 'w-full'})
        self.fields['gender'].widget.attrs.update({'class': 'w-full'})
        self.fields['age'].widget.attrs.update({'class': 'w-full'})
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'w-full'})
        self.fields['emergency_contact'].widget.attrs.update({'type': 'json', 'hidden': True})
        self.fields['is_active']



from core.models import MedicalHistory
class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['history']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['history'].widget.attrs.update({'type':'json', 'class': 'w-full'})


from .models import Insurance
class InsuranceInfoForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['provider_name', 'policy_number', 'coverage_start_date', 'coverage_end_date', 'coverage_details']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider_name'].widget.attrs.update({'class': 'w-full'})
        self.fields['policy_number'].widget.attrs.update({'class': 'w-full'})
        self.fields['coverage_start_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'w-full'})
        self.fields['coverage_end_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'w-full'})
        self.fields['coverage_details'].widget = forms.Textarea(attrs={'class': 'w-full'})

    def clean_coverage_end_date(self):
      coverage_end_date = self.cleaned_data.get('coverage_end_date')
      coverage_start_date = self.cleaned_data.get('coverage_start_date')

      if coverage_end_date and coverage_start_date and coverage_end_date < coverage_start_date:
          raise forms.ValidationError('Coverage end date must be after coverage start date.')


from core.models import Case
class InitialDiagnosisForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['initial_diagnosis']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['initial_diagnosis'].widget.attrs.update({'type':'json', 'class': 'w-full'})


class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['treatment_plan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['treatment_plan'].widget.attrs.update({'type':'json', 'class': 'w-full'})


class ClosureInfoForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['closure_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['closure_info'].widget.attrs.update({'type':'json', 'class': 'w-full'})

        
class NotesForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].widget = forms.Textarea(attrs={'class': 'w-full'})

        
from core.models import CheckUp
from core.models import CustomUser

class CheckUpForm(forms.ModelForm):
    class Meta:
        model = CheckUp
        fields = ['nurse', 'bp', 'pr', 'rr', 't', 'input', 'output', 'additional_information']
        widgets = {
            'nurse': forms.Select(attrs={'class': 'form-control'}),
            'bp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blood Pressure'}),
            'pr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pulse Rate'}),
            'rr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Respiratory Rate'}),
            't': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Temperature'}),
            'input': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'output': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'additional_information': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter nurse field to only include users with role 'nurse'
        self.fields['nurse'].queryset = CustomUser.objects.filter(role='nurse')


from core.models import Treatment
class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['treatment_type', 'description','treatment_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['treatment_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'type':'json', 'class': 'form-control'})
        self.fields['treatment_name'].widget.attrs.update({'class': 'form-control'})




class AssignNursesForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['assigned_nurses']
        widgets = {
            'assigned_nurses': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit choices to nurses only
        self.fields['assigned_nurses'].queryset = CustomUser.objects.filter(role='nurse')



class AssignBedForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['bed']
        widgets = {
                'bed': forms.Select(attrs={'class': 'form-control w-full'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bed'].queryset = Bed.objects.filter(status='available')








