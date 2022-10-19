from django.db import models


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


