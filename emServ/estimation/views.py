from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.contrib.auth import login

# Create your views here.

class EstimationView