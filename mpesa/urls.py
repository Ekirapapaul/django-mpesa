from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import SubmitView, CheckTransaction

mpesa_urls = [
    url(r'^submit/', SubmitView.as_view(), name='submit'),
    url(r'^checktransaction/', CheckTransaction.as_view(), name='check_transaction'),
]
