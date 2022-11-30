from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from .models import *
from django.views.generic import DetailView, View
from .mixins import *
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import *
from .utils import recalc_cart
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
        right_sph = request.GET.get("right_sph")
        right_cyl = request.GET.get("right_cyl")
        right_ax = request.GET.get("right_ax")
        left_sph = request.GET.get("left_sph")
        left_cyl = request.GET.get("left_cyl")
        left_ax = request.GET.get("left_ax")
        pd1 = request.GET.get("pd1")
        pd2 = request.GET.get("pd2")
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            qty=int(quantity),
            object_id=product.id,
            glist=f"Правый глаз: sph={right_sph}, cyl={right_cyl}, ax={right_ax}; Левый глаз: sph={left_sph}, cyl={left_cyl}, ax={left_ax}; pd1={pd1}, pd2={pd2}"
        )
        print(f"quantity = {quantity}")
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)

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
        recalc_cart(self.cart)
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
        recalc_cart(self.cart)
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


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'glasses/checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'glasses/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request)
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'glasses/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')

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