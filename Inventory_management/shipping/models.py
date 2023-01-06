from django.db import models
from apps.utils.models import Timestamps
from django_countries.fields import CountryField


class ShippingType(models.Model):
    '''
    The type of shipping transaction
    ['Purchase Delivery', 'Sales Delivery']
    '''
    shipping_type = models.CharField(max_length=100)

    def __str__(self):
        return self.shipping_type

class Shipping(Timestamps,models.Model):
    '''
    Shipping company details
    Every shipping transaction and the cost associated
    '''
    company = models.CharField(max_length=100)
    shipping_type = models.ForeignKey(ShippingType, on_delete=models.CASCADE)
    cost =  models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    cost_incurred = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}-{self.company}-{self.cost}'

class Supplier(models.Model):
    '''
    Details of of Supplier, where purchases are made
    '''
    supplier_name = models.CharField(max_length=100)
    supplier_type = models.CharField(max_length=100)
    shipping_id = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    website = models.CharField(max_length=100)
    account_username = models.CharField(max_length=100)
    account_password = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_mobile_number = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.supplier_name}-{self.shipping_id}"

class Customer(models.Model):
    '''
    Detail of Customers, who make sales orders
    '''
    customer_full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email_address = models.EmailField(max_length=100)
    shipping_id = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    shipping_address_1 = models.CharField(max_length=100)
    shipping_address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    province = models.CharField(max_length=100)
    country = CountryField(multiple=False)

    def __str__(self):
        return self.customer_full_name
