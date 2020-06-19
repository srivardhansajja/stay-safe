# apps/pages/forms.py
from django import forms
from .models import Trip, EmergencyContact


# Form used to create trips
class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'trip_location',
            'trip_name',
            'trip_start',
            'trip_end',
        ]

    trip_start = forms.DateTimeField(
        required=True,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    trip_end = forms.DateTimeField(
        required=True,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )


# Form to add emergency contact information
class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
