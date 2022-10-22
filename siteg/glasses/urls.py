from django.urls import path

from .views import *

urlpatterns = [
    path('', BaseView.as_view()),
    path('person', person),
    path('login', login),
    path('signin', signin),
    path('basket', basket),
    path('product', product),
    path('status', status),
    path('product/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
]