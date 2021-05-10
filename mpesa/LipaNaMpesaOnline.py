import os, socket, json, requests, datetime

import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from .models import PaymentTransaction
from .settings import api_settings

# Read variables from settings file

consumer_key = api_settings.CONSUMER_KEY
consumer_secret = api_settings.CONSUMER_SECRET

HOST_NAME = api_settings.HOST_NAME
PASS_KEY = api_settings.PASS_KEY
SHORT_CODE = api_settings.SHORT_CODE
SAFARICOM_API = api_settings.SAFARICOM_API


# Applies for LipaNaMpesaOnline Payment method
def generate_pass_key():
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
    s = SHORT_CODE + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')


def get_token():
    api_URL = "{}/oauth/v1/generate?grant_type=client_credentials".format(SAFARICOM_API)

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    jonresponse = json.loads(r.content)
    access_token = jonresponse['access_token']
    return access_token


def sendSTK(phone_number, amount, orderId=0, transaction_id=None, shortcode=None):
    SHORT_CODE = shortcode or SHORT_CODE
    access_token = get_token()
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = SHORT_CODE + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpush/v1/processrequest".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": SHORT_CODE,
        "Password": encoded,
        "Timestamp": time_now,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(int(amount)),
        "PartyA": phone_number,
        "PartyB": SHORT_CODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "{}/mpesa/confirm/".format(HOST_NAME),
        "AccountReference": phone_number,
        "TransactionDesc": "Payment for {}".format(phone_number)
    }

    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if json_response.get('ResponseCode'):
        if json_response["ResponseCode"] == "0":
            checkout_id = json_response["CheckoutRequestID"]
            if transaction_id:
                transaction = PaymentTransaction.objects.filter(id=transaction_id)
                transaction.checkoutRequestID = checkout_id
                transaction.save()
                return transaction.id
            else:
                transaction = PaymentTransaction.objects.create(phone_number=phone_number, checkoutRequestID=checkout_id,
                                                            amount=amount, order_id=orderId)
                transaction.save()
                return transaction.id
    else:
        raise Exception("Error sending MPesa stk push", json_response)


def check_payment_status(checkout_request_id, shortcode=None):
    SHORT_CODE = shortcode or SHORT_CODE
    access_token = get_token()
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = SHORT_CODE + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpushquery/v1/query".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": SHORT_CODE,
        "Password": encoded,
        "Timestamp": time_now,
        "CheckoutRequestID": checkout_request_id
    }
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if 'ResponseCode' in json_response and json_response["ResponseCode"] == "0":
        result_code = json_response['ResultCode']
        response_message = json_response['ResultDesc']
        return {
            "result_code": result_code,
            "status": result_code == "0",
            "message": response_message
        }
    else:
        raise Exception("Error sending MPesa stk push", json_response)
