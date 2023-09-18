from glasses.models import *

class Sun_glasses_manufacturer(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.title


class Sun_glasses_frame_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип оправы'
        verbose_name_plural = 'Типы оправ'

    def __str__(self):
        return self.title


class Sun_glasses_frame_material(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал оправы'
        verbose_name_plural = 'Материалы оправ'

    def __str__(self):
        return self.title


class Sun_glasses_size(models.Model):
    size = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Размер очков'
        verbose_name_plural = 'Размеры очков'

    def __str__(self):
        return self.size


class Sun_glasses_gender(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.title


class Sun_glasses_form(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Форма оправы'
        verbose_name_plural = 'Форма оправ'

    def __str__(self):
        return self.title


class Sun_glasses_linces_sph(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Сфера (Sph)')

    class Meta:
        verbose_name = 'Сфера (Sph)'
        verbose_name_plural = 'Сфера (Sph)'

    def __str__(self):
        return self.value


class Sun_glasses_linces_cyl(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Цилиндр (Cyl)')

    class Meta:
        verbose_name = 'Цилиндр (Cyl)'
        verbose_name_plural = 'Цилиндр (Cyl)'

    def __str__(self):
        return self.value


class Sun_glasses_linces_ax(models.Model):
    value = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ось (Ax)')

    class Meta:
        verbose_name = 'Ось (Ax)'
        verbose_name_plural = 'Ось (Ax)'

    def __str__(self):
        return self.value


class Sun_glasses_linces_pd(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='РМЦ (PD)')

    class Meta:
        verbose_name = 'РМЦ (PD)'
        verbose_name_plural = 'РМЦ (PD)'

    def __str__(self):
        return self.value
# Create your models here.
class Sun_Glasses(Product):
    glasses_size = models.ForeignKey('Sun_glasses_size', on_delete=models.CASCADE, verbose_name="Размер очков")
    glasses_gender = models.ForeignKey('Sun_glasses_gender', on_delete=models.CASCADE, verbose_name="Пол")
    manufacturer = models.ForeignKey('Sun_glasses_manufacturer', on_delete=models.CASCADE, verbose_name="Производитель")
    frame_material = models.ForeignKey('Sun_glasses_frame_material', on_delete=models.CASCADE, verbose_name="Материал оправы")
    frame_type = models.ForeignKey('Sun_glasses_frame_type', on_delete=models.CASCADE, verbose_name="Тип оправы")
    glasses_form = models.ForeignKey('Sun_glasses_form', on_delete=models.CASCADE, verbose_name="Форма очков")
    Lenses_height = models.IntegerField(verbose_name="Высота линзы")
    Lenses_width = models.IntegerField(verbose_name="Ширина линзы")
    Lenses_length = models.IntegerField(verbose_name="Длина линзы")
    Lenses_bridge = models.IntegerField(verbose_name="Высота линзы")

    class Meta:
        verbose_name = '        Солнцезащитные очки'
        verbose_name_plural = '     Солнцезащитные очки'

    def __str__(self):
        return "{} : {}".format(self.category, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')