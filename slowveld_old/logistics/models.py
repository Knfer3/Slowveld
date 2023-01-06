from django.db import models
from django_countries.fields import CountryField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class LogisticsCompany(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    email=models.EmailField()
    telephone=models.CharField(max_length=15)
    contact_name=models.CharField(max_length=100)
    website=models.CharField(max_length=200)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name



class Address(models.Model):

    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address

    class Meta:
        verbose_name_plural = 'Addresses'