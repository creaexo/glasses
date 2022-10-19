from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
# *args - список
# **kwargs - словарь
User = get_user_model()
#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Order

#6 Custumer


#1 Category

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, auto_created=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


#2 Product

# 2.1 Glasses

class Glasses_size(models.Model):
    size = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Размер очков'
        verbose_name_plural = 'Размеры очков'

    def __str__(self):
        return self.size


class Glasses_gender(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.title


class Glasses_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип оправы'
        verbose_name_plural = 'Типы оправ'

    def __str__(self):
        return self.title


class Glasses_frame_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип оправы'
        verbose_name_plural = 'Типы оправ'

    def __str__(self):
        return self.title


class Glasses_frame_material(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал оправы'
        verbose_name_plural = 'Материалы оправ'

    def __str__(self):
        return self.title


class Glasses_manufacturer(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.title


class Glasses_form(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Форма оправы'
        verbose_name_plural = 'Форма оправ'

    def __str__(self):
        return self.title


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
    type = models.ForeignKey('Glasses_type', on_delete=models.CASCADE, verbose_name="Тип")
    manufacturer = models.ForeignKey('Glasses_manufacturer', on_delete=models.CASCADE, verbose_name="Производитель")
    frame_material = models.ForeignKey('Glasses_frame_material', on_delete=models.CASCADE, verbose_name="Материал оправы")
    frame_type = models.ForeignKey('Glasses_frame_type', on_delete=models.CASCADE, verbose_name="Тип оправы")
    glasses_form = models.ForeignKey('Glasses_form', on_delete=models.CASCADE, verbose_name="Форма очков")
    lince_height = models.IntegerField(verbose_name="Высота линзы")
    lince_width = models.IntegerField(verbose_name="Ширина линзы")
    lince_length = models.IntegerField(verbose_name="Длина линзы")
    lince_bridge = models.IntegerField(verbose_name="Высота линзы")

    class Meta:
        verbose_name = 'Очки'
        verbose_name_plural = 'Очки'

    def __str__(self):
        return "{} : {}".format(self.category, self.title)

# 2.2 Lince


class Lince_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип линз'
        verbose_name_plural = 'Типы линз'

    def __str__(self):
        return self.title


class Lince_manufacturer(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Производитель линз'
        verbose_name_plural = 'Производители линз'


    def __str__(self):
        return self.title


    def __str__(self):
        return self.meaning


class Lince_material(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал линз'
        verbose_name_plural = 'Материалы линз'


    def __str__(self):
        return self.title


class Lince(Product):
    meaning = models.BooleanField(default=0)
    moisture = models.IntegerField(verbose_name="Влагосодержание", validators=[MaxValueValidator(100)])
    oxygen = models.IntegerField(verbose_name="Пропускание кислорода")
    diameter = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='Цена')
    class Meta:
        verbose_name = 'Линзы'
        verbose_name_plural = 'Линзы'


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

    def __str__(self):
        return str(self.id)


#5 LikeProduct

class LikeProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Покупатель")
    like = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="Корзина", related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Продукт: {} (Понравившееся)".format(self.product.title)

#6 Like


class Like(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

#5 Order

#6 Customer


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)