from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import *
from django.views.generic import DetailView, View
from .mixins import *
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context

class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'glasses/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context
class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        quantity = request.GET.get("quantity")
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, qty=int(quantity), object_id=product.id
        )
        print(f"quantity = {quantity}")
        if created:
            self.cart.products.add(cart_product)
        self.cart.save()
        messages.add_message(request, messages.INFO, "Товар добавленв корзину")
        return HttpResponseRedirect('/cart/')

class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        #recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')

class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        qty = int(request.POST.get('quantity'))
        cart_product.qty = qty
        cart_product.save()
        self.cart.save()
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        print(request.POST)
        return HttpResponseRedirect('/cart/')
class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        products_g = LatestProducts.objects.get_products_for_main_page('glasses')
        products_l = LatestProducts.objects.get_products_for_main_page('lenses')
        products_s = LatestProducts.objects.get_products_for_main_page('stock')
        context = {
            'products_g': products_g,
            'products_l': products_l,
            'products_s': products_s,
            'cart': self.cart,
        }
        return render(request, "glasses/base.html", context)


class CartView(CartMixin,View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart
        }
        return render(request, 'glasses/cart.html', context)
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