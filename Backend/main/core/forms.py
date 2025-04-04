from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput

User = get_user_model()

class StaffAddForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-input w-full', 'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-input w-full', 'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Enter Username'}),
            'role': forms.Select(attrs={'class': 'form-select w-full'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        if User.objects.filter(username=cleaned_data.get('username')).exists():
              raise forms.ValidationError("A user with this username already exists.")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
