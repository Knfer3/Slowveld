from django.contrib import admin
from .models import *


# class LogisticsCompanyAdmin(admin.ModelAdmin):
#     list_display=['type_of_sale','sell_price']

# class AddressAdmin(admin.ModelAdmin):
#     list_display=['status']



admin.site.register(LogisticsCompany)
admin.site.register(Address)
