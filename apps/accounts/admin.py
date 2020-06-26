# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomCreateForm, CustomChangeForm
from .models import CustomAccount


# Create custom admin accounts
class CustomAdminAccount(UserAdmin):
    """Custom admin account fields"""
    add_form = CustomCreateForm
    form = CustomChangeForm
    list_display = ['email', 'username']
    model = CustomAccount


# Register custom user accounts and custom admins
admin.site.register(CustomAccount, CustomAdminAccount)
