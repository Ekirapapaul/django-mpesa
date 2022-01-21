# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True


class PaymentTransaction(models.Model):
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_finished = models.BooleanField(default=False)
    is_successful = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=30)
    order_id = models.CharField(max_length=200)
    checkout_request_id = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{} {}".format(self.phone_number, self.amount)


class Wallet(BaseModel):
    phone_number = models.CharField(max_length=30)
    available_balance = models.DecimalField(('available_balance'), max_digits=6, decimal_places=2, default=0)
    actual_balance = models.DecimalField(('actual_balance'), max_digits=6, decimal_places=2, default=0)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return self.phone_number
