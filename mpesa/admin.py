# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import PaymentTransaction, Wallet

# Register your models here.
admin.site.register(PaymentTransaction)
admin.site.register(Wallet)