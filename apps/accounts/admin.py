# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.pages.models import EmergencyContact
from .forms import CustomCreateForm, CustomChangeForm
from .models import CustomAccount


# Create custom admin accounts
class CustomAdminAccount(UserAdmin):
    """Custom admin account fields"""
    add_form = CustomCreateForm
    form = CustomChangeForm
    list_display = ['email', 'username', 'emergency_email']
    model = CustomAccount


# Register custom user accounts and custom admins
admin.site.register(CustomAccount, CustomAdminAccount)

# Register emergency contact model
admin.site.register(EmergencyContact)
