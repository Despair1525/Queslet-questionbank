from django.shortcuts import render,redirect
from django.http import HttpRequest
from ..models.models import Mcq
from django.core.paginator import Paginator

# Create your views here.

def manage(request):

    return render(request, 'manage.html',{})
