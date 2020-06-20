# apps/pages/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from datetime import date, timedelta
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

    def get_queryset(self):
        return Trip.objects.filter(trip_owner=self.request.user)


# Render the page to view upcoming trips
class UpcomingTripsView(TripPageView):
    template_name = 'upcoming_trips.html'
    delta = date.today() + timedelta(7)

    def getqueryset(self):
        return Trip.objects.filter(
            trip_owner=self.request.user,
            trip_start__lte=str(self.delta),
        )


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
