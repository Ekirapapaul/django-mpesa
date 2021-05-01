from django.contrib import admin
from django.urls import path
from .views import SubmitView, CheckTransaction, ConfirmView, CheckTransactionOnline

mpesa_urls = [
    path('submit/', SubmitView.as_view(), name='submit'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('check-online/', CheckTransactionOnline.as_view(), name='confirm-online'),
    path('check-transaction/', CheckTransaction.as_view(), name='check_transaction'),
]
