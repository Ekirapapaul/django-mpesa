# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class PaymentTransaction(models.Model):
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(('amount'), max_digits=6, decimal_places=2, default=0)
    isFinished = models.BooleanField(default=False)
    isSuccessFull = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=30)
    checkoutRequestID = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.phone_number, self.amount)