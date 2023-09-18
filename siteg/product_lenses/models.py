from glasses.models import *

# Create your models here.
# 2.2 Lenses


class Lenses_manufacturer(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Производитель линз'
        verbose_name_plural = 'Производители линз'


    def __str__(self):
        return self.title


class Lenses_category(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категории линз'
        verbose_name_plural = 'Категории линз'

    def __str__(self):
        return self.title

class Lenses_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип линз'
        verbose_name_plural = 'Типы линз'

    def __str__(self):
        return self.title




class Lenses_material(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал линз'
        verbose_name_plural = 'Материалы линз'


    def __str__(self):
        return self.title


class Lenses_Sph(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Сфера (Sph)')

    class Meta:
        verbose_name = 'Сфера линз'
        verbose_name_plural = 'Сферы линз'


    def __str__(self):
        return self.value


class Lenses_rad(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Радиус (Вс)')

    class Meta:
        verbose_name = 'Радиус линз'
        verbose_name_plural = 'Радиусы линз'


    def __str__(self):
        return self.value


class Lenses(Product):
    manufacturer = models.ForeignKey('Lenses_manufacturer', on_delete=models.CASCADE, verbose_name="Производитель")
    material = models.ForeignKey('Lenses_material', on_delete=models.CASCADE, verbose_name="Материал")
    category_of_lenses = models.ForeignKey(Lenses_category, on_delete=models.CASCADE, verbose_name="Категория линз", default=0)
    type = models.ForeignKey('Lenses_type', on_delete=models.CASCADE, verbose_name="Тип")
    meaning = models.BooleanField(verbose_name="UVA/UVB защита", default=0)
    moisture = models.IntegerField(verbose_name="Влагосодержание", validators=[MaxValueValidator(100)])
    oxygen = models.IntegerField(verbose_name="Пропускание кислорода (Dk/t)")
    diameter = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Диаметр')
    class Meta:
        verbose_name = '    Линзы'
        verbose_name_plural = ' Линзы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')