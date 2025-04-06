from django import forms
from .models import Contact
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
        label="Name",
        required=True
    )
    phone_number = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        label="Phone Number",
        required=True
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        label="Email",
        required=True
    )
    contact_picture = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        ),
        label="Image",
        required=True
    )
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email',
                  'contact_picture', 'contact_group']
