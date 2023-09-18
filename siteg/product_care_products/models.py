from glasses.models import *

# Create your models here.
class Care_Products_manufacturer(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


    def __str__(self):
        return self.title


class Care_Products_type(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.title


class Care_Products(Product):
    manufacturer = models.ForeignKey('Care_Products_manufacturer', on_delete=models.CASCADE, verbose_name="Производитель")
    type = models.ForeignKey('Care_Products_type', on_delete=models.CASCADE, verbose_name="Тип")

    class Meta:
        verbose_name = 'Средство по уходу'
        verbose_name_plural = 'Средства по уходу'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')