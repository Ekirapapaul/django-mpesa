import os, socket, json, requests, datetime

from django.urls import reverse
import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from .models import PaymentTransaction
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

# import env settings
import importlib

try:
    dotenv = importlib.import_module('dotenv')
    dotenv.load_dotenv(dotenv.find_dotenv())
except ModuleNotFoundError:
    pass

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
api_URL = os.environ.get('API_URL')
INITIATOR_PASS = os.environ.get('INITIATOR_PASS')
CERTIFICATE_FILE = os.environ.get('CERTIFICATE_FILE')
HOST_NAME = os.environ.get('HOST_NAME')
PASS_KEY = os.environ.get('PASS_KEY')
shortcode = os.environ.get('SHORT_CODE')


def encryptInitiatorPassword():
    PASS = "foobar1234"
    cert_file_path = os.path.join(os.path.dirname(__file__), CERTIFICATE_FILE)
    cert_file = open(cert_file_path, 'rb')
    cert_data = cert_file.read()
    cert_file.close()

    cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    PASS = str.encode(PASS)  # If you are using python 3
    pub_key = cert.public_key()
    cipher = pub_key.encrypt(PASS, padding=PKCS1v15())
    return b64encode(cipher)


def generate_pass_key(cipher):
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
    s = shortcode + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')


def get_token():
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    jonresponse = json.loads(r.content)
    access_token = jonresponse['access_token']
    print(access_token)
    return access_token


def register_url(access_token):
    api_url = "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "ShortCode": "601754",
        "ResponseType": "Cancelled",
        "ConfirmationURL": HOST_NAME + reverse('mpesa-c2b-confirm'),
        "ValidationURL": HOST_NAME + reverse('mpesa-c2b-validate')
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


def sendSTK(phone_number, amount, orderId=0, transaction_id=None):
    access_token = get_token()
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = shortcode + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
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

    print(json.dumps(request))
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    print(json_response)
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
