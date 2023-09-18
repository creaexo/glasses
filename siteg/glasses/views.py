from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.list import MultipleObjectMixin

from .models import *
from django.views.generic import DetailView, View
from .mixins import *
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import *
from .utils import recalc_cart
class ProductDetailView(CartMixin, LikeMixin, CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'glasses': Glasses,
        'accessories': Accessories,
        'care_products': Care_Products,
        'sun_glasses': Sun_Glasses,
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
        context['like'] = self.like
        return context

class CategoryDetailView(CartMixin, LikeMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    lenses_category = Lenses_category.objects.all()
    lenses_type = Lenses_type.objects.all()
    lenses_manufacturer = Lenses_manufacturer.objects.all()
    lenses_material = Lenses_material.objects.all()

    galasses_frame_type = Glasses_frame_type.objects.all()
    galasses_form = Glasses_form.objects.all()
    galasses_manufacturer = Glasses_manufacturer.objects.all()

    sun_galasses_frame_type = Sun_glasses_frame_type.objects.all()
    sun_galasses_form = Sun_glasses_form.objects.all()
    sun_galasses_manufacturer = Sun_glasses_manufacturer.objects.all()

    care_products_type = Care_Products_type.objects.all()
    care_products_manufacturer = Care_Products_manufacturer.objects.all()

    accessories_type = Accessories_type.objects.all()
    accessories_manufacturer = Accessories_manufacturer.objects.all()
    # lenses_sph = Category.objects.all()
    # lenses_rad = Category.objects.all()
    context_object_name = 'category'
    template_name = 'glasses/category_detail.html'
    slug_url_kwarg = 'slug'
    print('galasses_manufacturer - ' + str(Glasses_manufacturer.objects.all()))

    def get_context_data(self, **kwargs):
        url = self.request.get_full_path()[::-1]
        select_sort = ''
        if '?' in url:
            url_split = url.split("?")[0][::-1]
            url_list = url_split.split("&")
            print('url_list - ' + str(url_list))
            arr = {}
            # if '?' in url
            for i in url_list:
                s = i.split("=")
                if s[0] == 'criteria_sort_by':
                    select_sort = s[1]
                if 'criteria' in s[0] and s[1] != '':
                    kwargs.update({f'{s[0]}': f'{s[1]}'})

        print('models -  ', self.kwargs)
        print("self.kwargs['slug'] -", self.kwargs['slug'])
        # print(self.kwargs)
        context = super().get_context_data(filter=1, **kwargs)
        # context['url_split'] = url_split.replace(f"criteria_page={context['page']}&", '')
        context['select_sort'] = select_sort
        context['cart'] = self.cart
        context['like'] = self.like
        if self.kwargs['slug'] == 'lenses':
            context['lenses_category'] = self.lenses_category
            context['lenses_type'] = self.lenses_type
            context['lenses_manufacturer'] = self.lenses_manufacturer
            context['lenses_material'] = self.lenses_material
        elif self.kwargs['slug'] == 'glasses':
            context['galasses_frame_type'] = self.galasses_frame_type
            context['galasses_form'] = self.galasses_form
            context['galasses_manufacturer'] = self.galasses_manufacturer
        elif self.kwargs['slug'] == 'sun_glasses':
            context['sun_galasses_frame_type'] = self.sun_galasses_frame_type
            context['sun_galasses_form'] = self.sun_galasses_form
            context['sun_galasses_manufacturer'] = self.sun_galasses_manufacturer
        elif self.kwargs['slug'] == 'care_products':
            context['care_products_type'] = self.care_products_type
            context['care_products_manufacturer'] = self.care_products_manufacturer
        elif self.kwargs['slug'] == 'accessories':
            context['accessories_type'] = self.accessories_type
            context['accessories_manufacturer'] = self.accessories_manufacturer
        # context['lenses_sph'] = self.lenses_sph
        # context['lenses_rad'] = self.lenses_rad
        return context
class AddToCartView(CartMixin, LikeMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        quantity = request.GET.get("quantity")
        # right_sph = request.GET.get("right_sph")
        # right_cyl = request.GET.get("right_cyl")
        # right_ax = request.GET.get("right_ax")
        # left_sph = request.GET.get("left_sph")
        # left_cyl = request.GET.get("left_cyl")
        # left_ax = request.GET.get("left_ax")
        # pd1 = request.GET.get("pd1")
        # pd2 = request.GET.get("pd2")
        try:
            check_product_in_cart = CartProduct.objects.get(
                user=self.cart.owner,
                cart=self.cart,
                content_type=content_type,
                object_id=product.id)
        except:
            check_product_in_cart = False
            print(check_product_in_cart)
        if(check_product_in_cart):
            check_product_in_cart.qty += int(quantity)
            check_product_in_cart.save()
        else:
            cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner,
                cart=self.cart,
                content_type=content_type,
                qty=int(quantity),
                object_id=product.id,
                # glist=f"Правый глаз: sph={right_sph}, cyl={right_cyl}, ax={right_ax}; Левый глаз: sph={left_sph}, cyl={left_cyl}, ax={left_ax}; pd1={pd1}, pd2={pd2}"
            )
            if created:
                self.cart.products.add(cart_product)
                print(f"created = {created}")

        print(f"quantity = {quantity}")


        recalc_cart(self.cart)

        messages.add_message(request, messages.INFO, "Товар добавленв корзину")
        return HttpResponseRedirect('/cart/')
class AddToFavourites(LikeMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = LikeProduct.objects.get_or_create(
            user=self.like.owner,
            like=self.like,
            content_type=content_type,
            object_id=product.id,
        )
        if created:
            self.like.products.add(cart_product)

        messages.add_message(request, messages.INFO, "Товар добавлен в избранное")
        return HttpResponseRedirect('/favorites/')

class DeleteFromCartView(CartMixin, LikeMixin, View):
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
        messages.add_message(request, messages.INFO, "Товар успешно удалён")
        return HttpResponseRedirect('/cart/')
class DeleteFromCartFavorites(CartMixin, LikeMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        like_product = LikeProduct.objects.get(
            user=self.like.owner, like=self.like, content_type=content_type, object_id=product.id
        )
        self.like.products.remove(like_product)
        like_product.delete()
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/favorites/')

class ChangeQTYView(CartMixin, LikeMixin, View):

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
# class CategoryFilter(CartMixin, LikeMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
#         content_type = ContentType.objects.get(model=ct_model)
#         product = content_type.model_class().objects.get(slug=product_slug)
#         cart_product = CartProduct.objects.get(
#             user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
#         )
#         qty = int(request.POST.get('quantity'))
#         cart_product.qty = qty
#         cart_product.save()
#         recalc_cart(self.cart)
#         messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
#         print(request.POST)
#         return HttpResponseRedirect('/cart/')


class BaseView(CartMixin, LikeMixin, CategoryDetailMixin, View):

    def get(self, request, *args, **kwargs):
        products_g = LatestProducts.objects.get_products_for_main_page('glasses')
        products_l = LatestProducts.objects.get_products_for_main_page('lenses')
        products_s = LatestProducts.objects.get_products_for_main_page('stock')
        context = {
            'products_g': products_g,
            'products_l': products_l,
            'products_s': products_s,
            'cart': self.cart,
        'like': self.like,
        }
        return render(request, "glasses/base.html", context)


class CartView(CartMixin, LikeMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
            'like': self.like
        }
        return render(request, 'glasses/cart.html', context)

class FavoritesView(CartMixin, LikeMixin, View):

    def get(self, request):
        context = {
            'cart': self.cart,
            'like': self.like
        }
        return render(request, 'glasses/favorites.html', context)


class CheckoutView(CartMixin, LikeMixin, View):


    def get(self, request, *args, **kwargs):


        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        # products_order = request.POST
        context = {
            'cart': self.cart,
            'like': self.like,
            'categories': categories,
            'form': form,
        }
        return render(request, 'glasses/checkout.html', context, **kwargs)

class MakeProductsForOrderView(CartMixin, LikeMixin, View):

    def post(self, request, *args, **kwargs):
        arr = request.POST
        no_empty = False
        for product_slug, ct_model in arr.items():
            if product_slug != 'csrfmiddlewaretoken':
                print(product_slug)
                print(ct_model)
                if product_slug[:9] == '___all___':
                    content_type = ContentType.objects.get(model=ct_model)
                    product = content_type.model_class().objects.get(slug=product_slug[9:])
                    product_in_order = CartProduct.objects.get(
                        user=self.cart.owner,
                        cart=self.cart,
                        content_type=content_type,
                        object_id=product.id)
                    product_in_order.in_order = False
                    product_in_order.save()
                else:
                    no_empty = True
                    content_type = ContentType.objects.get(model=ct_model)
                    product = content_type.model_class().objects.get(slug=product_slug)
                    product_in_order = CartProduct.objects.get(
                        user=self.cart.owner,
                        cart=self.cart,
                        content_type=content_type,
                        object_id=product.id)
                    product_in_order.in_order = True
                    product_in_order.save()
        print(request.POST)
        if no_empty:
            return HttpResponseRedirect('/checkout/')
        else:
            messages.add_message(request, messages.INFO, 'Необходимо выбрать товары для оформления заказа')
            return HttpResponseRedirect('/cart/')



class MakeOrderView(CartMixin, LikeMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)

        # cart_product, created = CartProduct.objects.get_or_create(
        #     user=self.cart.owner,
        #     cart=self.cart,
        #     content_type=content_type,
        #     qty=int(quantity),
        #     object_id=product.id,
        #     # glist=f"Правый глаз: sph={right_sph}, cyl={right_cyl}, ax={right_ax}; Левый глаз: sph={left_sph}, cyl={left_cyl}, ax={left_ax}; pd1={pd1}, pd2={pd2}"
        # )
        if form.is_valid():
            arr = request.POST
            qty_slug = {}
            for product_slug, ct_model in arr.items():
                if product_slug[:18] == '___not_in_order___':
                    print(product_slug)
                    print(ct_model)
                    content_type = ContentType.objects.get(model=ct_model)
                    product = content_type.model_class().objects.get(slug=product_slug[18:])
                    product_in_order = CartProduct.objects.get(
                        user=self.cart.owner,
                        cart=self.cart,
                        content_type=content_type,
                        object_id=product.id
                    )
                    qty_slug[product_slug] = product_in_order.qty
                    product_in_order.delete()
            recalc_cart(self.cart)
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.products_information = form.cleaned_data['products_information']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)

            self.cart = Cart.objects.create(owner=customer)
            for product_slug, ct_model in arr.items():
                if product_slug[:18] == '___not_in_order___':
                    print(product_slug)
                    print(ct_model)
                    content_type = ContentType.objects.get(model=ct_model)
                    product = content_type.model_class().objects.get(slug=product_slug[18:])
                    cart_product, created = CartProduct.objects.get_or_create(
                        user=self.cart.owner,
                        cart=self.cart,
                        content_type=content_type,
                        qty=int(qty_slug[product_slug]),
                        object_id=product.id,
                        # glist=f"Правый глаз: sph={right_sph}, cyl={right_cyl}, ax={right_ax}; Левый глаз: sph={left_sph}, cyl={left_cyl}, ax={left_ax}; pd1={pd1}, pd2={pd2}"
                    )
                    if created:
                        self.cart.products.add(cart_product)
                        print(f"created = {created}")



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

class NoneView(CartMixin, LikeMixin, View):

    def get(self, request):
        context = {
            'cart': self.cart,
            'like': self.like
        }
        return render(request, 'glasses/none.html', context)
class SearchView(CartMixin, LikeMixin, View):

    def get(self, request):
        context = {
            'cart': self.cart,
            'like': self.like
        }
        return render(request, 'glasses/search.html', context)
def logout_user(request):
    logout(request)
    return redirect('login')
def none(request):
    return render(request, "glasses/none.html")

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