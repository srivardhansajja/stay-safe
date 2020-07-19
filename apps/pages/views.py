# apps/pages/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .forms import TripCreateForm, TripUpdateForm
from .forms import EmergencyContactForm, EmergencyContactUpdateForm
from .models import Trip, EmergencyContact, TripStatusList_
from django.db.models import F
from django.shortcuts import render, redirect,get_object_or_404


#  Render the homepage
class HomePageView(TemplateView):
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
                trip_start__lte=(now + timedelta(days=7))
            ).order_by('trip_start'),

            # Awaiting Response
            'awaiting_response': Trip.objects.filter(
                trip_owner=self.request.user,
                response_sent=False,
                trip_end__lt=now,
                trip_end__gt=(now - timedelta(hours=1))
            ).order_by('trip_start'),

            # Past
            'past': Trip.objects.filter(
                trip_owner=self.request.user,
                trip_end__lt=now,
                response_sent=True,
            ).order_by('trip_start')
        }

        # Update trip status for each query
        for key, val in queryset.items():
            trips_set = queryset[key]
            if key == 'in_progress':
                trips_set.update(
                    trip_status=TripStatusList_.IP.value
                )
            if key == 'upcoming':
                trips_set.update(
                    trip_status=TripStatusList_.YTS.value
                )
            
            if key == 'awaiting_response':
                trips_set.update(
                    trip_status=TripStatusList_.AR.value
                )

            if key == 'past':
                trips_set.update(
                    trip_status=TripStatusList_.CP.value
                )

        return queryset


# Render the page to Create Trips
class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trip_create.html'
    form_class = TripCreateForm
    success_url = reverse_lazy('trip_list')
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

def mark_complete(request, pk):
    if 'markcompletebtn' in request.POST:
        trip_ = Trip.objects.filter(pk=pk)[0]
        trip_.response_sent = True
        trip_.save()
        return redirect('trip_list')
    return HttpResponse('Error! Please try again')

def emergency_mode(request):
    if 'emergencybtn' in request.POST:
        return redirect('home')
    return HttpResponse('Error! Please try again')

class EmergencyContactCreateView(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    template_name = 'emergencycontact_add.html'
    form_class = EmergencyContactForm
    success_url = reverse_lazy('emergencycontact_view')
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
            return HttpResponseRedirect(reverse('emergencycontact_add'))

        if self.contact_duplicate(request.POST.get('email')):
            messages.error(request, "dup", extra_tags='duplicate_contact')
            return HttpResponseRedirect(reverse('emergencycontact_add'))

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EmergencyContactPageView(LoginRequiredMixin, ListView):
    model = EmergencyContact
    template_name = 'emergencycontact_view.html'
    fields = '__all__'
    login_url = '/accounts/login/'
    context_object_name = 'emergency_contacts'

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)


class EmergencyContactUpdateView(LoginRequiredMixin, UpdateView):
    model = EmergencyContact
    form_class = EmergencyContactUpdateForm
    template_name = 'emergencycontact_update.html'
    success_url = reverse_lazy('emergencycontact_view')


class EmergencyContactDeleteView(LoginRequiredMixin, DeleteView):
    model = EmergencyContact
    template_name = 'emergencycontact_delete.html'
    success_url = reverse_lazy('emergencycontact_view')
