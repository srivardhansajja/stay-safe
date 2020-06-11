# apps/pages/views.py
from django.views.generic import TemplateView


#  Render the homepage
class HomePageView(TemplateView):
    template_name = 'home.html'
