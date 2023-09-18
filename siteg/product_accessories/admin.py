from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
# Register your models here.
from .models import *


class AccessoriesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='accessories'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Accessories, AccessoriesAdmin)

admin.site.register(Accessories_type)
admin.site.register(Accessories_manufacturer)
