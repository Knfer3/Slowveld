from django.db import models
from apps.utils.models import Timestamps
from django.shortcuts import reverse
from apps.utils.models import Pricing
from django.utils import formats


# from slowveld.transactions.views import round_up

class Supplier(models.Model):
    '''The details of the supplier for raw material inputs'''
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.ForeignKey('logistics.Address',on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Customer(Timestamps, models.Model):
    '''The details of the supplier for raw material inputs'''
    Recipient_name = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    description = models.TextField()
    address = models.ForeignKey('logistics.Address',on_delete=models.CASCADE)

    def __str__(self):
        return self.Recipient_name

class Item(models.Model):
    '''Item as seen on shelf/website store.'''

    item = models.CharField(max_length=200)
    description = models.TextField(null=True, blank = True)
    category = models.ForeignKey("utils.Category", on_delete=models.CASCADE, null=True,blank=True)
    uom_quantity_purchased = models.IntegerField(default=0)
    uom_quantity = models.IntegerField(default=0)
    uom = models.ForeignKey('utils.UOM', on_delete=models.CASCADE, null=True,blank=True)
    cost_price = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    order_cost = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    sold_in_packs = models.BooleanField(default=False)

    class meta:
        unique_together = [['category'],['supplier'],['uom'],['item'],]


    def get_absolute_url(self):
        return reverse("transactions:slowveld-forms")




    def __str__(self):

        return f'{self.item}'
    


class ItemPurchased(Timestamps,models.Model):
    '''Purchased item as seen on shelf/website store.'''

    class Meta:
        verbose_name = "Items purchased"
        verbose_name_plural = "Items purchased"

    item = models.CharField(max_length=200)
    description = models.TextField(null=True, blank = True)
    category = models.ForeignKey("utils.Category", on_delete=models.CASCADE, null=True,blank=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE, null=True,blank=True)
    uom_quantity_purchased = models.IntegerField(default=0)
    uom_quantity = models.IntegerField(default=0)
    uom = models.ForeignKey('utils.UOM', on_delete=models.CASCADE, null=True,blank=True)
    cost_price = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    counted_as_stock = models.BooleanField(default=False)
    sold_in_packs = models.BooleanField(default=False)


    def cost_per_item(self):
        return  self.cost_price / self.uom_quantity_purchased
        



    def __str__(self):

        return f'{self.item}'



class PurchaseOrder(Timestamps,models.Model):
    '''Order from Supplier of all purchase items'''

    purchase_order_reference = models.CharField(max_length=200)
    item = models.ManyToManyField(ItemPurchased, blank=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE, null=True,blank=True)
    delivery_price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.ForeignKey('utils.Status',on_delete=models.CASCADE, default=1)
    order_cost = models.DecimalField(max_digits=10,decimal_places=2) #incl Delivery
    received = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-id']


 
    def __str__(self):
        return f"{self.purchase_order_reference}"






class Stock(Timestamps,models.Model):
    '''intems/inputs that are in the system (on-hand)'''

    item = models.CharField(max_length=200)
    description = models.TextField(null=True, blank = True)
    category = models.ForeignKey("utils.Category", on_delete=models.CASCADE, null=True,blank=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE, null=True,blank=True)
    quantity_on_hand = models.IntegerField(default=0)
    uom = models.ForeignKey('utils.UOM', on_delete=models.CASCADE, null=True,blank=True)
    cost_price_on_hand = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    order_reference = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    reserve_quantity = models.IntegerField(default=0)

    def get_item_price(self):
        return  self.cost_price_on_hand / self.quantity_on_hand
        
    def __str__(self):
        return f'{self.item}'
  



class NewProduct(models.Model):
    '''Provides all the input details & quantities for a new product'''
    product_name = models.ForeignKey("Product",on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    input_item = models.ForeignKey(Stock, verbose_name=("input_item_in_product"), on_delete=models.CASCADE, blank=True,null=True)
    input_quantity = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    product_type = models.ForeignKey("utils.Type", on_delete=models.CASCADE)
    
    def new_product_input_cost(self):
        # Stock valued at average cost
        return self.input_item.get_item_price() * self.input_quantity


    def __str__(self):
        return f'{self.input_item}'



class Product(Timestamps,models.Model):
    '''Finished Products in inventory'''

    name = models.CharField(max_length=200)
    description = models.TextField()
    stock_on_hand = models.IntegerField(default=0)
    product_type = models.ForeignKey("utils.Type", on_delete=models.CASCADE)
    inputs = models.ManyToManyField(NewProduct, blank=True)
    slug = models.SlugField()
    image = models.ImageField(blank=True,null=True)


    def product_cost_per_item(self):
        total_cost = 0
        for i in self.inputs.all():
            total_cost += i.new_product_input_cost()
        return round(total_cost,2)

    def product_total_cost(self):
        total_cost = 0
        for i in self.inputs.all():
            total_cost += i.new_product_input_cost()
        return round(total_cost * self.stock_on_hand,2)

    def __str__(self):
        return self.name




class SaleOrderItem(Timestamps,models.Model):
    '''Add Products to a cart'''
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True,null=True)
    ordered = models.BooleanField(default=False)
    sale_order_reference = models.CharField(max_length=255, blank=True, null=True)
    pricing = models.ForeignKey('utils.Pricing',on_delete=models.CASCADE, null=True,blank=True)
    product_type = models.ForeignKey("utils.Type", on_delete=models.CASCADE)
    


    def __str__(self):
        return f'{self.item}'




    def get_pricing(self, type, moq):
        ''' sets the quantity for Mininum Order Quantity (moq) and uses the type to get the object'''
        if  moq <10:
            sQuantity =  1
        elif moq >= 10 and moq <30:
            sQuantity = 10
        elif moq >= 30 and moq < 50:
            sQuantity = 30
        else:
            sQuantity = 50

        price = Pricing.objects.get(type=type,moq=sQuantity)
        return price.id



    def sufficient_stock_on_hand(self,order_amount: int):
        if  self.item.stock_on_hand > order_amount:
            result = True
        else:
            result = False
        return result

    def get_total_item_price(self):
        return self.quantity * self.pricing.sell_price

    



class SaleOrder(Timestamps, models.Model):
    '''Order refers to clients placing a candle order'''

    class Meta:
        ordering = ['-id']

    reference = models.CharField(max_length=255)
    
    product = models.ManyToManyField(SaleOrderItem,related_name='order_item')
    quantity = models.IntegerField
    status = models.ForeignKey('utils.Status',on_delete=models.CASCADE, null=True,blank=True)
    logistics_company = models.ForeignKey('logistics.LogisticsCompany',on_delete=models.CASCADE, blank=True,null=True)
    proof_of_payment = models.BooleanField(default=False)
    delivery_price = models.IntegerField()
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    delivered = models.BooleanField(default=False)
    counted = models.BooleanField(default=False)


    def create_reference_number(self):
        count = SaleOrder.objects.all().count()
        logistics = f'{self.logistics_company.code}'
        created = f'{formats.date_format(self.created_at, "y-m-d")}'


        inv = "INV"
        return f'{inv}-{count}-{logistics}-{created}'



    def get_total(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_total_item_price()

        return total + self.delivery_price


    def __str__(self):
        if self.reference:
            return self.reference
        else:
            return str(self.id)


