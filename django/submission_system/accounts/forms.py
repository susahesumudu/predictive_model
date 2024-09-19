from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

# User Registration Form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


# Profile Management Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_type', 'nic_passport_no', 'contact_address', 'permanent_address', 'mobile_no', 'home_no', 'gender']
        widgets = {
            'contact_address': forms.Textarea(attrs={'rows': 3}),
            'permanent_address': forms.Textarea(attrs={'rows': 3}),
        }




class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    # Add user_type field
    USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Lab Assistant', 'Lab Assistant'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


