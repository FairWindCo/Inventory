from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from info.models import Server


class ServerHealth(ListView):
    model = Server
