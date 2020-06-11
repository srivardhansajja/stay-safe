# apps/accounts/views.py
from django.views import generic
from .forms import CustomCreateForm
from django.urls import reverse_lazy


class SignUp(generic.CreateView):
    form_class = CustomCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
