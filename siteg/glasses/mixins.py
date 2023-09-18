from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.db.models import Q
from .models import *
from product_lenses.models import *
from product_accessories.models import *
from product_care_products.models import *
from product_sun_glasses.models import *
from product_glasses.models import *

class CategoryDetailMixin(SingleObjectMixin):

    CATEGORY_SLUG2PRODUCT_MODEL = {
        'glasses': Glasses,
        'accessories': Accessories,
        'care_products': Care_Products,
        'sun_glasses': Sun_Glasses,
        'lenses': Lenses
    }

    def get_context_data(self, filter=False, *args, **kwargs):
        object = {'object': kwargs['object']}
        print(object['object'])
        page = 1
        if isinstance(self.get_object(), Category):

            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**object)
            filter = True
            count_of_items = 6
            if filter:
                dck = {}
                dck['criteria_sort_by'] = 'title'
                dck['criteria_page'] = 1
                dck['criteria_price_min'] = 0
                dck['criteria_price_max'] = 9999999
                dck['criteria_category'] = '0'
                dck['criteria_type'] = '0'
                dck.update(kwargs)
                print(kwargs)
                change_criteria_page = False
                if dck['criteria_page'] == "<<":
                    dck['criteria_page'] = 1
                elif dck['criteria_page'] == ">>":
                    change_criteria_page = True
                    dck['criteria_page'] = 1
                del dck['object']
                sort_by = dck['criteria_sort_by']
                del dck['criteria_sort_by']
                page = int(dck['criteria_page'])
                del dck['criteria_page']
                max_price = int(dck['criteria_price_max'])
                del dck['criteria_price_max']
                min_price = int(dck['criteria_price_min'])
                del dck['criteria_price_min']
                print('min_price - ' + str(min_price))
                print('max_price - ' + str(max_price))
                criteria_list = []
                dict_criteria = {}
                dict_criteria_manuf = {}
                selected_manuf = []
                criteria_category_none = 0
                criteria_type_none = 0
                if dck['criteria_category'] == '0':
                    criteria_category_none = 1
                    del dck['criteria_category']
                if dck['criteria_type'] == '0':
                    criteria_type_none = 1
                    del dck['criteria_type']
                # if criteria_category_none:
                #     del dck['criteria_category']
                # if criteria_type_none:
                #     del dck['criteria_type']
                for k, v in dck.items():
                    if 'criteria_manufacturer' not in k:
                        dict_criteria[k] = v
                    else:
                        selected_manuf.append(int(k[::-1][0]))
                        dict_criteria_manuf[k] = v
                print('dict_criteria - ' + str(dict_criteria))

                if dict_criteria_manuf == {}:
                    criteria_list.append(dict_criteria)
                else:
                    for k in dict_criteria_manuf:
                        dc = {}
                        dc.update(dict_criteria)
                        # print('dc - ', dc)
                        # print('dict_criteria - ', dict_criteria)
                        dc.update({f'{k}': f'yes'})
                        criteria_list.append(dc)
                        # print('criteria_list - ', criteria_list)


                # print(dict_criteria)
                # print(dict_criteria_manuf)
                criteria_filters = '[Q(**' + str(criteria_list)[1:].replace('}, ', '}) | Q(**')
                print(criteria_filters)

                if self.get_object().slug == 'lenses' or self.get_object().slug == 'care_products' or self.get_object().slug == 'accessories':
                    criteria_filters = criteria_filters.replace('}]', '})]').replace("': '", "': int('").replace('criteria_manufacturer_', "manufacturer_id': ").replace("': int('yes", "'").replace("''", "").replace("',", "'),").replace("'}", "')}").replace('criteria_category', 'category_id').replace('criteria_type', 'type_id')
                elif self.get_object().slug == 'glasses' or self.get_object().slug == 'sun_glasses':
                    criteria_filters = criteria_filters.replace('}]', '})]').replace("': '", "': int('").replace('criteria_manufacturer_', "manufacturer_id': ").replace("': int('yes", "'").replace("''", "").replace("',", "'),").replace("'}", "')}").replace('criteria_category', 'frame_type_id').replace('criteria_type', 'glasses_form_id')
                print(criteria_filters)
                print('criteria_filters - ' + criteria_filters)
                q = eval(criteria_filters)
                # print(type(q))
                products = model.objects
                products_count = products.filter(*q).filter(price__range=(min_price, max_price)).count()
                print('products_count - ' + str(products_count))
                context['category_products'] = products.filter(*q).filter(price__range=(min_price, max_price)).order_by(sort_by)[count_of_items*page-count_of_items:count_of_items*page]
                context['products_num'] = products.filter(*q).filter(price__range=(min_price, max_price)).order_by(sort_by)[count_of_items*page-count_of_items:count_of_items*page]
                context['selected_manuf'] = selected_manuf
                context['page'] = page
                context['min_price'] = min_price
                context['max_price'] = max_price
                if criteria_category_none:
                    dict_criteria['criteria_category'] = 0
                if criteria_type_none:
                    dict_criteria['criteria_type'] = 0
                context['criteria_category'] = int(dict_criteria['criteria_category'])
                context['criteria_type'] = int(dict_criteria['criteria_type'])
                dck['criteria_page'] = products_count/count_of_items
                context['last_page'] = products_count/count_of_items
                # print("context['last_page']" + str(context['last_page']))
                # print("context['last_page'] - 1" + str(context['last_page'] - 1 == 0))
                if context['last_page'] % 1 != 0:
                    context['last_page'] = (context['last_page'] + 1) // 1
                context['last_page'] = int(context['last_page'])
                if not context['category_products']:
                    context['last_page'] = 0
                print("context['category_products'] - " + str(not context['category_products']))
                print("context['last_page'] type - " + str(type(context['last_page'])))

            else:
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                context['category_products'] = model.objects.all()[:1]
            return context
        context = super().get_context_data(**object)
        # context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user,
                    # phone=request.user.phone,
                )
                cart = Cart.objects.create(owner=customer)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            #if not cart:
                # cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)



    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         customer = Customer.objects.filter(user=request.user).first()
    #         if not customer:
    #             customer = Customer.objects.create(
    #                 user=request.user,
    #                 # phone=request.user.phone,
    #             )
    #             cart = Cart.objects.create(owner=customer)
    #         cart = Cart.objects.filter(owner=customer, in_order=False).first()
    #         if not cart:
    #             cart = Cart.objects.create(owner=customer)
    #     else:
    #         cart = Cart.objects.filter(for_anonymous_user=True).first()
    #         #if not cart:
    #             # cart = Cart.objects.create(for_anonymous_user=True)
    #     self.cart = cart
    #
    #     ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
    #     content_type = ContentType.objects.get(model=ct_model)
    #     product = content_type.model_class().objects.get(slug=product_slug)
    #     self.ct_model = ct_model
    #     self.product_slug = product_slug
    #     self.content_type = content_type
    #     self.product = product
    #     try:
    #         check_product_in_cart = CartProduct.objects.get(
    #             user=self.cart.owner,
    #             cart=self.cart,
    #             content_type=content_type,
    #             object_id=product.id)
    #     except:
    #         check_product_in_cart = False
    #     self.check_product_in_cart = check_product_in_cart
    #     return super().dispatch(request, *args, **kwargs)


class LikeMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user,
                    # phone=request.user.phone,
                )
                like = Like.objects.create(owner=customer)
            like = Like.objects.filter(owner=customer, in_order=False).first()
            if not like:
                like = Like.objects.create(owner=customer)
        else:
            like = Like.objects.filter(for_anonymous_user=True).first()
            #if not like:
                # like = like.objects.create(for_anonymous_user=True)
        self.like = like
        return super().dispatch(request, *args, **kwargs)
