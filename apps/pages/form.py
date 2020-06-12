# apps/pages/form.py
from django import forms
from django.forms import ModelForm
from .models import Trip


# Access the built-in DateInput widget
class DateInput(forms.DateInput):
    input_type = 'date'


# Form used to create trips
class TripCreateForm(ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        widgets = {
            'trip_start': DateInput(),
            'trip_end': DateInput(),
        }
