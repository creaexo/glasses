from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
# Register your models here.
from .models import *

class Care_ProductsAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='care_products'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Care_Products, Care_ProductsAdmin)
admin.site.register(Care_Products_type)
admin.site.register(Care_Products_manufacturer)