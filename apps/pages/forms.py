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

        labels = {
            'trip_name': 'Trip name/alias',
            'trip_location': 'Location',
        }

    trip_start = forms.DateTimeField(
        label='Start date',
        required=True,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    trip_end = forms.DateTimeField(
        label='End date',
        required=True,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )


# Form used to update trips
class TripUpdateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'trip_location',
            'trip_name',
            'trip_start',
            'trip_end',
        ]

        labels = {
            'trip_name': 'Trip name/alias',
            'trip_location': 'Location',
        }

    trip_start = forms.DateTimeField(
        label='Start date',
        required=True,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    trip_end = forms.DateTimeField(
        label='End date',
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
