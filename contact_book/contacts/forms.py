from django import forms
from .models import Contact, User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Your password must contain at least 8 characters, including letters and numbers.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter.")
        return password


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


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
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
        label="Owner",
    )
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email',
                  'contact_picture', 'contact_group', 'owner']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Make contact_group field required
            self.fields['contact_group'].empty_label = None