from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
from .models import *


class LensesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='lenses'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Lenses, LensesAdmin)
admin.site.register(Lenses_type)
admin.site.register(Lenses_category)
admin.site.register(Lenses_material)
admin.site.register(Lenses_manufacturer)