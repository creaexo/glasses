from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
# Register your models here.
from .models import *

class GlassesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='glasses'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LensesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='lenses'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
#Общее
admin.site.register(Cart)
admin.site.register(CartProduct)

admin.site.register(Like)
admin.site.register(LikeProduct)
admin.site.register(Customer)
admin.site.register(Category)


#Очки
admin.site.register(Glasses, GlassesAdmin)
admin.site.register(Glasses_size)
admin.site.register(Glasses_gender)
admin.site.register(Glasses_frame_type)
admin.site.register(Glasses_frame_material)
admin.site.register(Glasses_manufacturer)
admin.site.register(Glasses_form)

admin.site.register(Glasses_linces_sph)
admin.site.register(Glasses_linces_cyl)
admin.site.register(Glasses_linces_ax)
admin.site.register(Glasses_linces_pd)

#Линзы
admin.site.register(Lenses, LensesAdmin)
admin.site.register(Lenses_type)
admin.site.register(Lenses_material)
admin.site.register(Lenses_manufacturer)


admin.site.register(Order)
