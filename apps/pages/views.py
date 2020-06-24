# apps/pages/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .forms import TripCreateForm
from .models import Trip


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
