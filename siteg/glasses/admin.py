from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
# Register your models here.
from .models import *

class StocksAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='stock'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
#Общее
admin.site.register(Cart)
admin.site.register(CartProduct)

admin.site.register(Like)
admin.site.register(LikeProduct)
admin.site.register(Customer)
admin.site.register(Category)

admin.site.register(Order)

#Остальное
# admin.site.register(Stocks, StocksAdmin)
