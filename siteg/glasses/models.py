from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

User = get_user_model()
#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Order

#6 Custumer


#0 Work

class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
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


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, auto_created=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = ' Категории'

    def __str__(self):
        return self.title


#2 Product

# 2.1 Glasses


class Glasses_manufacturer(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = '(1.1) Производители'

    def __str__(self):
        return self.title


class Glasses_frame_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип оправы'
        verbose_name_plural = '(1.2) Типы оправ'

    def __str__(self):
        return self.title


class Glasses_frame_material(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал оправы'
        verbose_name_plural = '(1.3) Материалы оправ'

    def __str__(self):
        return self.title


class Glasses_size(models.Model):
    size = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Размер очков'
        verbose_name_plural = '(1.4) Размеры очков'

    def __str__(self):
        return self.size


class Glasses_gender(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = '(1.5) Пол'

    def __str__(self):
        return self.title


class Glasses_form(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Форма оправы'
        verbose_name_plural = '(1.6) Форма оправ'

    def __str__(self):
        return self.title


class Glasses_linces_sph(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Сфера (Sph)')

    class Meta:
        verbose_name = 'Сфера (Sph)'
        verbose_name_plural = '(1.7.1) Сфера (Sph)'

    def __str__(self):
        return self.value


class Glasses_linces_cyl(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Цилиндр (Cyl)')

    class Meta:
        verbose_name = 'Цилиндр (Cyl)'
        verbose_name_plural = '(1.7.2) Цилиндр (Cyl)'

    def __str__(self):
        return self.value


class Glasses_linces_ax(models.Model):
    value = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ось (Ax)')

    class Meta:
        verbose_name = 'Ось (Ax)'
        verbose_name_plural = '(1.7.3) Ось (Ax)'

    def __str__(self):
        return self.value


class Glasses_linces_pd(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='РМЦ (PD)')

    class Meta:
        verbose_name = 'РМЦ (PD)'
        verbose_name_plural = '(1.7.4) РМЦ (PD)'

    def __str__(self):
        return self.value


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class Glasses(Product):
    glasses_size = models.ForeignKey('Glasses_size', on_delete=models.CASCADE, verbose_name="Размер очков")
    glasses_gender = models.ForeignKey('Glasses_gender', on_delete=models.CASCADE, verbose_name="Пол")
    manufacturer = models.ForeignKey('Glasses_manufacturer', on_delete=models.CASCADE, verbose_name="Производитель")
    frame_material = models.ForeignKey('Glasses_frame_material', on_delete=models.CASCADE, verbose_name="Материал оправы")
    frame_type = models.ForeignKey('Glasses_frame_type', on_delete=models.CASCADE, verbose_name="Тип оправы")
    glasses_form = models.ForeignKey('Glasses_form', on_delete=models.CASCADE, verbose_name="Форма очков")
    Lenses_height = models.IntegerField(verbose_name="Высота линзы")
    Lenses_width = models.IntegerField(verbose_name="Ширина линзы")
    Lenses_length = models.IntegerField(verbose_name="Длина линзы")
    Lenses_bridge = models.IntegerField(verbose_name="Высота линзы")

    class Meta:
        verbose_name = '[1.0] Очки'
        verbose_name_plural = '(1.0) Очки'

    def __str__(self):
        return "{} : {}".format(self.category, self.title)

# 2.2 Lenses


class Lenses_manufacturer(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Производитель линз'
        verbose_name_plural = '(2.1) Производители линз'


    def __str__(self):
        return self.title


class Lenses_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип линз'
        verbose_name_plural = '(2.2) Типы линз'

    def __str__(self):
        return self.title




class Lenses_material(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал линз'
        verbose_name_plural = '(2.3) Материалы линз'


    def __str__(self):
        return self.title


class Lenses_Sph(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Сфера (Sph)')

    class Meta:
        verbose_name = 'Сфера линз'
        verbose_name_plural = '(2.4.1) Сферы линз'


    def __str__(self):
        return self.value


class Lenses_rad(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Радиус (Вс)')

    class Meta:
        verbose_name = 'Радиус линз'
        verbose_name_plural = '(2.4.2) Радиусы линз'


    def __str__(self):
        return self.value


class Lenses(Product):
    meaning = models.BooleanField(default=0)
    moisture = models.IntegerField(verbose_name="Влагосодержание", validators=[MaxValueValidator(100)])
    oxygen = models.IntegerField(verbose_name="Пропускание кислорода")
    diameter = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')
    class Meta:
        verbose_name = 'Линзы'
        verbose_name_plural = '(2.0) Линзы'


    def __str__(self):
        return self.title


#3 CartProduct

class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Покупатель")
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="Корзина", related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = '(3.2) Продукты в корзине'

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)

#4 Cart

class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = '(3.1) Корзины'

    def __str__(self):
        return str(self.id)


#5 LikeProduct

class LikeProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Покупатель")
    like = models.ForeignKey('Like', on_delete=models.CASCADE, verbose_name="Нравится", related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Понравившийся продукт'
        verbose_name_plural = '(3.3) Понравившиеся продукты'

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
        verbose_name_plural = '(3.3) Понравившееся'


    def __str__(self):
        return str(self.id)

#5 Order

#6 Customer


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '(3.0) Пользователи'


    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

