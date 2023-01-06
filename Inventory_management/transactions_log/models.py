from django.db import models
from apps.utils.models import Timestamps
from Inventory_management.shipping.models import Supplier

# Transactions log serves as a running commentary of the
# purchase and sales orders
# ideally should assist with accounting records


class Transactions(Timestamps, models.Model):
    '''
    A table that captures a running log of events.
    Purchases & and Sales. 
    Production.
    Should be able to match business actions (effort) with rows.
    '''
    item = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    transaction_detail = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    debit = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    credit = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)

    def __str__(self):
        return f'{self.item}-{self.created_at}-{self.quantity}-{self.amount}'


class PurchaseOrder(models.Model):
    pass
    # item_id
    # purchase_quantity
    # purchase_cost

class PurchaseStatus(models.Model):
    status = models.CharField(max_length=100)

class Purchase(Timestamps, models.Model):
    reference_number = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    purchase_status = models.ForeignKey(PurchaseStatus,on_delete=models.CASCADE)
    delivery_date = models.DateField()

# class ProductPricing(models.Model):
    # name
    # quantity
    # price


# class SalesOrder(models.Model):
    # product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    # product_pricing

    

# class Sale(Timestamps,models.Model):
    # invoice_number
    # sales_order_id
    # customer_id
    # total_amount
    # sale_status



class Production(Timestamps, models.Model):
    pass 