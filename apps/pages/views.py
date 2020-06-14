# apps/pages/views.py
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .form import TripCreateForm
from .models import Trip


#  Render the homepage
class HomePageView(TemplateView):
    template_name = 'home.html'


# Render the page to View Trips
class TripPageView(ListView):
    model = Trip
    template_name = 'trip_view.html'
    fields = '__all__'

    def get_query_set(self):
        return self.Trip.objects.filter(user=self.request.user)


# Render the page to Create Trips
class TripCreateView(CreateView):
    model = Trip
    template_name = 'trip_create.html'
    form_class = TripCreateForm
    success_url = reverse_lazy('home')

    def get_query_set(self):
        return self.Trip.objects.filter(user=self.request.user)
