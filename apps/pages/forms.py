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
        ),
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

    # Validate form fields
    def clean(self):
        form_data = super().clean()
        trip_start = form_data.get('trip_start')
        trip_end = form_data.get('trip_end')

        # Raise an error if trip_start > trip_end
        if trip_start > trip_end:
            self.add_error(
                'trip_start',
                'Error: Start date must be before end date'
            )
            self.add_error(
                'trip_end',
                'Error: End date must be after start date.'
            )
            raise forms.ValidationError('invalid')
        return self.cleaned_data


# Form to add emergency contact information
class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
