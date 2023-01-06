from django.contrib import admin
from .models import *

class NewProductAdmin(admin.ModelAdmin):

    list_display=['input_item','product_name' , 'input_quantity', 'new_product_input_cost' ] #'new_product_input_cost', 'get_uom']
  
    def get_uom(self, obj):
        return obj.input_item.uom
    get_uom.short_description = 'Uom'
    get_uom.admin_order_field = 'input_item__uom'


class ItemAdmin(admin.ModelAdmin):

    list_display=['item' , 'category', 'cost_price','uom_quantity' ] #'new_product_input_cost', 'get_uom']

class ItemPurchasedAdmin(admin.ModelAdmin):

    list_display=['item' , 'cost_price', 'uom_quantity', 'sold_in_packs' ] #'new_product_input_cost', 'get_uom']

class ProductAdmin(admin.ModelAdmin):

    list_display=['name' , 'stock_on_hand', ] #'new_product_input_cost', 'get_uom']
  
    
class SaleOrderItemAdmin(admin.ModelAdmin):

    list_display=['item' , 'sale_order_reference' , 'quantity', 'ordered']
  

class StockAdmin(admin.ModelAdmin):

    list_display=['item' , 'category', 'cost_price_on_hand','quantity_on_hand' ] #'new_product_input_cost', 'get_uom']



admin.site.register(Supplier)
admin.site.register(Customer)

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemPurchased, ItemPurchasedAdmin)
admin.site.register(PurchaseOrder)
admin.site.register(Stock, StockAdmin)
# admin.site.register(ProductCreate)
admin.site.register(Product, ProductAdmin)
admin.site.register(SaleOrderItem,SaleOrderItemAdmin)
admin.site.register(SaleOrder)
admin.site.register(NewProduct, NewProductAdmin)

