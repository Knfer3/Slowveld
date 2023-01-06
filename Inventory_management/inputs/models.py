from django.db import models

class UOM(models.Model):
    '''
    Unit of measurement
    '''
    name=models.CharField(max_length=100, unique=True)
    code=models.CharField(max_length=10)

    def __str__(self):
        return self.name


class InputCategory( models.Model):
    '''
    The category the input item falls under
    ['Jar','Wick','Wax','Essential Oil','Fragrance Oil','Labels','Packaging','Misc.']
    '''
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category





class Item(models.Model):
    '''
    Input Items as they appear from the supplier. 
    Before purchased, this is making the input known to the system.
    '''
    item = models.CharField(max_length=100)
    category_id = models.ForeignKey(InputCategory, on_delete=models.CASCADE)
    item_cost = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    UOM = models.ForeignKey(UOM, on_delete=models.CASCADE)
    sold_as_pack = models.BooleanField(default=False)
    quantity_per_pack = models.IntegerField(default=1)
    cost_per_pack_excl_VAT = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    cost_per_pack_Incl_VAT = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)

    def __str__(self):
        return f'{self.item}'



