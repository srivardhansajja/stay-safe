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
    context_object_name = 'trips'

    # Trip querysets for each trip status
    def get_queryset(self):
        queryset = {
            # All
            'all': Trip.objects.filter(
                trip_owner=self.request.user
            ),
            # In Progress
            'in_progress': Trip.objects.filter(
                trip_owner=self.request.user,
                trip_start__gte=date.today(),
                trip_end__lte=date.today()
            ),
            # Upcoming
            'upcoming': Trip.objects.filter(
                trip_owner=self.request.user,
                trip_start__lte=(date.today() + timedelta(7))
            ),
            # Past
            'past': Trip.objects.filter(
                trip_owner=self.request.user,
                trip_end__lte=date.today()
            )
        }
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

        form.instance.trip_status = "Yet to start"
        # if datetime.now() > form.instance.trip_start:
        #     form.instance.trip_status = "In progress"
        # else:
        #     form.instance.trip_status = "Yet to start"
        return super().form_valid(form)
