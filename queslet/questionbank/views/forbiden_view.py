
from django.shortcuts import render
from django.http import HttpResponse


def forbiden(request):
    
    return render(request, 'forbiden.html')