from django.shortcuts import render, HttpResponse

# Create your views here.


def links(request):
    return HttpResponse('links:Anything is OK!')