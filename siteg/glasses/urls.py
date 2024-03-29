from django.urls import path

from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='index'),
    path('person', person),
    path('login', LoginUser.as_view(), name="login"),
    path('signin', signin),
    path('basket', basket),
    path('product', product),
    path('status', status),
    path('product/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('add-to-favourites/<str:ct_model>/<str:slug>/', AddToFavourites.as_view(), name='add_to_favourites'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('remove-from-favorites/<str:ct_model>/<str:slug>/', DeleteFromCartFavorites.as_view(), name='delete_from_favorites'),
    path('change_qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('make-products-for-order/', MakeProductsForOrderView.as_view(), name='make_products_for_order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('none/', NoneView.as_view(), name='none'),
    path('search/', SearchView.as_view(), name='search'),
    path('make-order/', MakeOrderView.as_view(), name='make_order')
]