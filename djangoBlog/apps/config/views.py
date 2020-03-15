from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView, ListView
# Create your views here.


def links(request):
    return HttpResponse('links:Anything is OK!')

