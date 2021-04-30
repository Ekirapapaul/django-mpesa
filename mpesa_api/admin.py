from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import PaymentTransaction, Wallet



class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "amount", "isFinished",
                    "isSuccessFull", "trans_id", 'date_created','date_modified')

admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(Wallet)