# apps/pages/views.py
from django.views.generic import TemplateView, ListView
from . models import Trip


#  Render the homepage
class HomePageView(TemplateView):
    template_name = 'home.html'


class TripPageView(ListView):
    model = Trip
    template_name = 'trip_page.html'
    fields = '__all__'

    def get_query_set(self):
        return self.Trip.objects.filter(user=self.request.user)
