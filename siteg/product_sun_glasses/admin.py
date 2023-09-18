from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
# Register your models here.
from .models import *

class Sun_GlassesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='sun_glasses'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Sun_glasses_size)
admin.site.register(Sun_Glasses, Sun_GlassesAdmin)
admin.site.register(Sun_glasses_gender)
admin.site.register(Sun_glasses_frame_type)
admin.site.register(Sun_glasses_frame_material)
admin.site.register(Sun_glasses_manufacturer)
admin.site.register(Sun_glasses_form)

admin.site.register(Sun_glasses_linces_sph)
admin.site.register(Sun_glasses_linces_cyl)
admin.site.register(Sun_glasses_linces_ax)
admin.site.register(Sun_glasses_linces_pd)