from django.db import models
from django.core.validators import RegexValidator


class ContactGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_regex = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message="Phone number must be a 10-digit Indian number starting with 6, 7, 8, or 9."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    email = models.EmailField(blank=True, null=True)
    contact_picture = models.ImageField(upload_to='contacts')
    contact_group = models.ForeignKey(ContactGroup, on_delete=models.CASCADE, related_name='contacts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
