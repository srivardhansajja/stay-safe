# apps/accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomAccount


# Create custom account creation forms
class CustomCreateForm(UserCreationForm):
    """TODO: Set custom fields"""
    model = CustomAccount
    pass


# Create custom account change forms
class CustomChangeForm(UserChangeForm):
    """TODO: Set custom fields"""
    model = CustomAccount
    pass
