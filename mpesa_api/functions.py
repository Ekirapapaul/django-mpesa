import os, socket, json, requests, datetime

from django.urls import reverse
import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from .models import PaymentTransaction


# import env settings
from decouple import config

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')
PASS_KEY = config('PASS_KEY')
shortcode = config('SHORT_CODE')
SAFARICOM_API = config('SAFARICOM_API')


#generate password by encoding the concatenated string that combines business short code, passkey and timestamp
def generate_pass_key(cipher):
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    s = shortcode + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

#function used to generate an access token. Requires consumer_key and consumer_secret
def get_token():
    api_URL = "{}/oauth/v1/generate?grant_type=client_credentials".format(SAFARICOM_API)

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    jsonresponse = json.loads(r.content)
    access_token = jsonresponse['access_token']
    print(access_token)
    return access_token





#LipaNaMpesa Online STK push 
def sendSTK(phone_number, amount, orderId=0, transaction_id=None):
    access_token = get_token()
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = shortcode + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpush/v1/processrequest".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    print("Phonenumber: {}, Amount: {}".format(phone_number, amount))
    request = {
        "BusinessShortCode": shortcode,
        "Password": encoded,
        "Timestamp": time_now,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(int(amount)),
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "{}/mpesa/confirm/".format(HOST_NAME),
        "AccountReference": phone_number,
        "TransactionDesc": "Payment for {}".format(phone_number)
    }

    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if json_response["ResponseCode"] == "0":
        checkoutId = json_response["CheckoutRequestID"]
        if transaction_id:
            transaction = PaymentTransaction.objects.filter(id=transaction_id)
            transaction.checkoutRequestID = checkoutId
            transaction.save()
            return transaction.id
        else:
            transaction = PaymentTransaction.objects.create(phone_number=phone_number, checkoutRequestID=checkoutId,
                                                            amount=amount, order_id=orderId)
            transaction.save()
            return transaction.id
    else:
        raise Exception("Error sending MPesa stk push", json_response)


def check_payment_status(checkout_request_id):
    access_token = get_token()
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = shortcode + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpushquery/v1/query".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": shortcode,
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