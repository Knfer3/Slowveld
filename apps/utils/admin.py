from django.contrib import admin
from .models import *


class PricingAdmin(admin.ModelAdmin):
    list_display=['type_of_sale','sell_price']

class StatusAdmin(admin.ModelAdmin):
    list_display=['status']

class UOMAdmin(admin.ModelAdmin):
    list_display=['name','code']


class TypeAdmin(admin.ModelAdmin):
    list_display= ['type']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']


admin.site.register(Pricing,PricingAdmin)
admin.site.register(Status,StatusAdmin)
# admin.site.register(UOM,UOMAdmin)
admin.site.register(Type,TypeAdmin)
admin.site.register(Category,CategoryAdmin)

