from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import SubmitView, CheckTransaction, ConfirmView

mpesa_urls = [
    url(r'^submit/', SubmitView.as_view(), name='submit'),
    url(r'^confirm/', ConfirmView.as_view(), name='confirm'),
    url(r'^checktransaction/', CheckTransaction.as_view(), name='check_transaction'),
]
