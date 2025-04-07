from django.contrib import admin
from .models import ContactGroup, Contact, User


@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'contact_group', 'owner')
    search_fields = ('name', 'phone_number', 'email')
    list_filter = ('contact_group',)

admin.site.register(User)