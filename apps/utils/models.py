from django.db import models

# Create your models here.

STATUS_CHOICES = (
                 ("New",'New Order'),
                 ("In Progress",'In Progress'),
                 ("Finished Goods",'Finished Good'),
                 ("Delivered",'Delivered'),
                 ("Returns",'Returns')
              )



class Timestamps(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True



class UOM(models.Model):
    '''
    Unit of measurement
    '''
    name=models.CharField(max_length=100, unique=True)
    code=models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Pricing(models.Model):
    type_of_sale = models.CharField(max_length=200, unique=True)
    sell_price = models.DecimalField(max_digits=10,decimal_places=2)
    moq = models.IntegerField()
    type = models.ForeignKey("utils.Type",on_delete=models.CASCADE)
    code = models.CharField(max_length=5)

    def __str__(self):
        return f"self.sell_price"




class Status(models.Model):
    status = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.status






class Type(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)


    def __str__(self):
        return self.name