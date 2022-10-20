from django.shortcuts import render

# Create your views here.
import datetime
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import DetailView, View
class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'glasses': Glasses,
        'lenses': Lenses
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'glasses/product.html'
    slug_url_kwarg = 'slug'





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