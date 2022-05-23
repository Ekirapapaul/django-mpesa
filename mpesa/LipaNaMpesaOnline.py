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
TILL_NUMBER = api_settings.TILL_NUMBER
SAFARICOM_API = api_settings.SAFARICOM_API
TRANSACTION_TYPE = api_settings.TRANSACTION_TYPE
AUTH_URL = api_settings.AUTH_URL


# Applies for LipaNaMpesaOnline Payment method
def generate_pass_key():
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
    s = SHORT_CODE + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')


def get_token():
    api_url = "{}{}".format(SAFARICOM_API, AUTH_URL)

    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if r.status_code == 200:
        jonresponse = json.loads(r.content)
        access_token = jonresponse['access_token']
        return access_token
    elif r.status_code == 400:
        print('Invalid credentials.')
        return False


def sendSTK(phone_number, amount, orderId=0, transaction_id=None, shortcode=None, account_number=None):
    code = shortcode or SHORT_CODE
    party_b = TILL_NUMBER or code
    access_token = get_token()
    if access_token is False:
        raise Exception("Invalid Consumer key or secret or both")

    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = code + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpush/v1/processrequest".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }

    transaction_type = TRANSACTION_TYPE or "CustomerBuyGoodsOnline"
    # If account number is set, change transaction type to paybill
    if account_number:
        transaction_type = "CustomerPayBillOnline"
    elif transaction_type == "CustomerPayBillOnline" and account_number == None:
        account_number = phone_number

    request = {
        "BusinessShortCode": int(code),
        "Password": encoded,
        "Timestamp": time_now,
        "TransactionType": transaction_type,
        "Amount": str(int(amount)),
        "PartyA": phone_number,
        "PartyB": party_b,
        "PhoneNumber": phone_number,
        "CallBackURL": "{}/mpesa/confirm/".format(HOST_NAME),
        "AccountReference": account_number or code,
        "TransactionDesc": "{}".format(phone_number)
    }

    print(request)
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if json_response.get('ResponseCode'):
        if json_response["ResponseCode"] == "0":
            checkout_id = json_response["CheckoutRequestID"]
            if transaction_id:
                transaction = PaymentTransaction.objects.filter(id=transaction_id)
                transaction.checkout_request_id = checkout_id
                transaction.save()
                return transaction.id
            else:
                transaction = PaymentTransaction.objects.create(phone_number=phone_number,
                                                                checkout_request_id=checkout_id,
                                                                amount=amount, order_id=orderId)
                transaction.save()
                return transaction.id
    else:
        raise Exception("Error sending MPesa stk push", json_response)


def check_payment_status(checkout_request_id, shortcode=None):
    code = shortcode or SHORT_CODE
    access_token = get_token()
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = code + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpushquery/v1/query".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": code,
        "Password": encoded,
        "Timestamp": time_now,
        "CheckoutRequestID": checkout_request_id
    }
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if 'ResponseCode' in json_response and json_response["ResponseCode"] == "0":
        requestId = json_response.get('CheckoutRequestID')
        transaction = PaymentTransaction.objects.get(
            checkout_request_id=requestId)
        if transaction:
            transaction.is_finished = True
            transaction.is_successful = True
            transaction.save()

        result_code = json_response['ResultCode']
        response_message = json_response['ResultDesc']
        return {
            "result_code": result_code,
            "status": result_code == "0",
            "finished": transaction.is_finished,
            "successful": transaction.is_successful,
            "message": response_message
        }
    else:
        raise Exception("Error checking transaction status", json_response)
