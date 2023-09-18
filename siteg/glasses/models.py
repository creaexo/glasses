from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

# Create your models here.

User = get_user_model()
#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Order

#6 Custumer


#0 Work

def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:4]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()

#1 Category

class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Очки': 'glasses__count',
        'Аксессуары': 'accessories__count',
        'Средства по уходу': 'care_products__count',
        'Солнечные очки': 'sun_glasses__count',
        'Линзы': 'lenses__count'
    }
    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('glasses', 'lenses')
        qs = list(self.get_queryset().annotate(*models).values())


class Category(models.Model):
    slug = models.SlugField(max_length=100, auto_created=True)
    name = models.CharField(max_length=100, verbose_name='Название категории')

    objects = CategoryManager()
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = ' Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

#2 Product




class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image1 = models.ImageField(verbose_name='Изображение 1', blank=True)
    image2 = models.ImageField(verbose_name='Изображение 2', blank=True)
    image3 = models.ImageField(verbose_name='Изображение 3', blank=True)
    image4 = models.ImageField(verbose_name='Изображение 4', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

# class Stocks(Product):
#     new_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Новая цена')
#     manufacturer = models.ForeignKey('Other_manufacturer', on_delete=models.CASCADE, verbose_name="Производитель")
#     type = models.ForeignKey('Other_type', on_delete=models.CASCADE, verbose_name="Тип")
#
#     class Meta:
#         verbose_name = '[6.0] Акция'
#         verbose_name_plural = '(6.0) Акции'
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return get_product_url(self, 'product_detail')

#3 CartProduct

class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Покупатель")
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="Корзина", related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Пренадлежность к категориям')
    object_id = models.PositiveIntegerField(verbose_name='ID товара')
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество единиц товара')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    glist = models.TextField(verbose_name="Параметры", default='')
    in_order = models.BooleanField(verbose_name="В заказе", default=False)
    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


# class CartProduct(models.Model):
#     user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Покупатель")
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="Корзина", related_name='related_products')
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     qty = models.PositiveIntegerField(default=1)
#     final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
#     glist = models.TextField(verbose_name="Параметры", default='')
#     in_order = models.BooleanField(verbose_name="В заказе", default=False)
#     class Meta:
#         verbose_name = 'Продукт в корзине'
#         verbose_name_plural = 'Продукты в корзине'
#
#     def __str__(self):
#         return "Продукт: {} (для корзины)".format(self.content_object.title)
#
#     def save(self, *args, **kwargs):
#         self.final_price = self.qty * self.content_object.price
#         super().save(*args, **kwargs)



#4 Cart

class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart', verbose_name='Продукты')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Количество продуктов')
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False, verbose_name='Заказан')
    for_anonymous_user = models.BooleanField(default=False, verbose_name='От анонимного покупателя')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.id)


# class ProductInOrder(models.Model):
#     cart_product = models.ForeignKey('CartProduct', on_delete=models.CASCADE, verbose_name="Продукт в корзине", related_name='related_cart')
# class CartForOrder(models.Model):
#
#     owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
#     products = models.ManyToManyField(ProductInOrder, blank=True, related_name='cart_product')
#     total_products = models.PositiveIntegerField(default=0)
#     final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
#     in_order = models.BooleanField(default=False)
#     for_anonymous_user = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзины'
#
#     def __str__(self):
#         return str(self.id)



#5 LikeProduct

class LikeProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Покупатель")
    like = models.ForeignKey('Like', on_delete=models.CASCADE, verbose_name="Нравится", related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Понравившийся продукт'
        verbose_name_plural = 'Понравившиеся продукты'

    def __str__(self):
        return "Продукт: {} (Понравившееся)".format(self.product.title)

#6 Like


class Like(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(LikeProduct, blank=True, related_name='related_like')
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Понравившееся'
        verbose_name_plural = 'Понравившееся'


    def __str__(self):
        return str(self.id)

#5 Order

#6 Customer



class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')
    USERNAME_FIELD = "username"
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    # final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    products_information = models.TextField(verbose_name='Информация о товарах', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)


    class Meta:
        verbose_name = '    Заказ'
        verbose_name_plural = '         Заказы'