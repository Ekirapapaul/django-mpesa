from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'MPESA_CONFIG', None)

DEFAULTS = {
    'CONSUMER_KEY': None,
    'CONSUMER_SECRET': None,
    'CERTIFICATE_FILE': None,
    'HOST_NAME': None,
    'PASS_KEY': None,
    'SAFARICOM_API': 'https://sandbox.safaricom.co.ke',
    'SHORT_CODE': None,
}

api_settings = APISettings(USER_SETTINGS, DEFAULTS, None)
