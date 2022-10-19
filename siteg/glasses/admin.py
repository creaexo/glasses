from django.contrib import admin

# Register your models here.
from .models import *


#Общее
admin.site.register(Cart)
admin.site.register(CartProduct)

admin.site.register(Like)
admin.site.register(LikeProduct)
admin.site.register(Customer)
admin.site.register(Category)


#Очки
admin.site.register(Glasses)
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
admin.site.register(Lenses)
admin.site.register(Lenses_type)
admin.site.register(Lenses_material)
admin.site.register(Lenses_manufacturer)
