# apps/pages/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import TripCreateForm, EmergencyContactForm
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

    def get_queryset(self):
        return Trip.objects.filter(trip_owner=self.request.user)


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


class EmergencyContactCreateView(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    template_name = 'add_emergency_ontact.html'
    form_class = EmergencyContactForm
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.isntance.user = self.request.user
        return super().form_valid(form)
