# apps/pages/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .forms import TripCreateForm, TripUpdateForm, EmergencyContactForm
from .models import Trip, EmergencyContact


#  Render the homepage
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


# Render the page to View Trips
class TripPageView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trip_view.html'
    fields = '__all__'
    login_url = '/accounts/login/'
    context_object_name = 'trips'

    # Trip querysets for each trip status
    def get_queryset(self):
        now = timezone.now()
        queryset = {
            # All
            'all': Trip.objects.filter(
                trip_owner=self.request.user
            ).order_by('trip_start'),
            # In Progress
            'in_progress': Trip.objects.filter(
                trip_owner=self.request.user,
                trip_start__lte=now,
                trip_end__gt=now
            ).order_by('trip_start'),
            # Upcoming
            'upcoming': Trip.objects.filter(
                trip_owner=self.request.user,
                trip_start__gt=now,
                trip_end__lte=(now + timedelta(7))
            ).order_by('trip_start'),
            # Past
            'past': Trip.objects.filter(
                trip_owner=self.request.user,
                trip_end__lt=now
            ).order_by('trip_start')
        }
        # Update trip status for each query
        for key, val in queryset.items():
            trips_set = queryset[key]
            if key == 'in_progress':
                trips_set.update(trip_status="In progress")
            if key == 'upcoming':
                trips_set.update(trip_status="Yet to start")
            if key == 'past':
                trips_set.update(trip_status="Completed")
        return queryset


# Render the page to Create Trips
class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trip_create.html'
    form_class = TripCreateForm
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.trip_owner = self.request.user
        return super().form_valid(form)


class TripUpdateView(LoginRequiredMixin, UpdateView):
    model = Trip
    form_class = TripUpdateForm
    template_name = 'trip_update.html'
    success_url = reverse_lazy('trip_list')


class TripDeleteView(LoginRequiredMixin, DeleteView):
    model = Trip
    template_name = 'trip_delete.html'
    success_url = reverse_lazy('trip_list')


class EmergencyContactCreateView(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    template_name = 'add_emergency_contact.html'
    form_class = EmergencyContactForm
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'

    # Return the number of emergency contacts associated with the user
    def contact_count(self):
        return EmergencyContact.objects.filter(user=self.request.user).count()

    # Return true if 'post_email' is a duplicate email for the user
    def contact_duplicate(self, post_email):
        return EmergencyContact.objects.filter(
                user=self.request.user, email=post_email).exists()

    # Re-direct with an error if contact emails max out or have duplicates
    def post(self, request, *args, **kwargs):
        if self.contact_count() >= 5:
            messages.error(request, "max", extra_tags='max_contacts')
            return HttpResponseRedirect(reverse('add_emergency_contact'))

        if self.contact_duplicate(request.POST.get('email')):
            messages.error(request, "dup", extra_tags='duplicate_contact')
            return HttpResponseRedirect(reverse('add_emergency_contact'))

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
