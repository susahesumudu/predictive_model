from django import forms
from .models import StudentProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'date_of_birth', 'address', 'phone_number', 'email', 'course', 'start_date', 'end_date', 'profile_picture']




class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=255)
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  # Add start_date field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
