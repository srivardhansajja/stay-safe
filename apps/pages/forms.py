# apps/pages/forms.py
from django import forms
from .models import Trip


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
