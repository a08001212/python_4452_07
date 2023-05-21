import datetime

from django.shortcuts import render
import requests, json
from django.http import HttpResponse
from mysite.models import *
# Create your views here.
def index(request):
    return render(request, 'index.html', locals())