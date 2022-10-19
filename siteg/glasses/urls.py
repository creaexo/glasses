from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('person', person),
    path('login', login),
    path('signin', signin),
    path('basket', basket),
    path('product', product),
    path('status', status),
]