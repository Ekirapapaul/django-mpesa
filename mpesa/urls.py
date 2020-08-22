from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import SubmitView, CheckTransaction, ConfirmView, CheckTransactionOnline

mpesa_urls = [
    url(r'^submit/', SubmitView.as_view(), name='submit'),
    url(r'^confirm/', ConfirmView.as_view(), name='confirm'),
    url(r'^check-online/', CheckTransactionOnline.as_view(), name='confirm-online'),
    url(r'^check-transaction/', CheckTransaction.as_view(), name='check_transaction'),
]
