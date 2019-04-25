# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from billing.models import BillingProfile
from django.db import models

ADDRESS_TYPES=(
('billing','Billing'),
('shipping','Shipping'),
)

# Create your models here.
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    address_type = models.CharField(max_length = 120,choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length = 120)
    address_line_2 = models.CharField(max_length = 120,null= True,blank=True)
    suburb = models.CharField(max_length = 120,default='Fourways')
    city = models.CharField(max_length = 120)
    state = models.CharField(max_length = 120)
    country = models.CharField(max_length = 120, default='South Africa')
    postal_code = models.CharField(max_length = 120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line1} \n {line2} \n {suburb} \n {city} \n {state} \n{postal} \n {country}" .format(
        line1 = self.address_line_1,
        line2 = self.address_line_2 or "",
        suburb = self.suburb,
        city = self.city,
        state = self.state,
        postal = self.postal_code,
        country = self.country,
        )
