# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import PaymentTransaction, Wallet


# Register your models here.

class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "amount", "is_finished",
                    "is_successful", "trans_id", 'date_created', 'date_modified')


admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(Wallet)
