from django.shortcuts import render

# Create your views here.
import datetime
from django.shortcuts import render, redirect
from .models import *


def index(request):
    return render(request, "glasses/index.html")


def person(request):
    return render(request, "glasses/person.html")

def login(request):
    return render(request, "glasses/login.html")

def signin(request):
    return render(request, "glasses/signin.html")


def basket(request):
    return render(request, "glasses/basket.html")


def product(request):
    return render(request, "glasses/product.html")

def status(request):
    return render(request, "glasses/status.html")