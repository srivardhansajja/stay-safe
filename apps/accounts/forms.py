# apps/accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomAccount


# Create custom account creation forms
class CustomCreateForm(UserCreationForm):
    """Account creation fields"""
    class Meta(UserCreationForm.Meta):
        model = CustomAccount
        fields = ('username', 'email', 'first_name', 'last_name')


# Create custom account change forms
class CustomChangeForm(UserChangeForm):
    """Admin access"""
    class Meta:
        model = CustomAccount
        fields = ('username', 'email', 'first_name', 'last_name')
