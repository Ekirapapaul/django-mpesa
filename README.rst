=====
mpesa
=====

Django-Mpesa is a generic python library that interfaces the safaricom
MPESA APIs to enable easy payments to your python application.

Detailed documentation is in the "docs" directory.

View the module from the  `official pypi site <https://pypi.org/project/django-mpesa/>`__

Quick start
-----------
1. Install the package with pip like this::

    pip install django-mpesa
    
2. Add "mpesa" to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'mpesa',
    ]

3. Add Mpesa Config variables to your project's settings.py file 

.. code-block:: python

    MPESA_CONFIG = {
        'CONSUMER_KEY': '<Your consumer key from daraja>',
        'CONSUMER_SECRET': '<Your consumer secret from daraja>',
        'HOST_NAME': '<Your hostname e.g https://myhostname>',
        'PASS_KEY': '<Your pass key from daraja>',
        'SAFARICOM_API': 'https://sandbox.safaricom.co.ke',
        'SHORT_CODE': '174379'

    }
    # Check below for full setting variables description

4. Include the polls URLconf in your project urls.py like this::

.. code-block:: python

    from django.urls import path, include
    from mpesa.urls import mpesa_urls

    path('mpesa/', include(mpesa_urls)),

5. Run `python manage.py migrate` to create the mpesa models.

6. Start the development server and visit http://127.0.0.1:8000/admin/

7. Visit http://127.0.0.1:8000/mpesa/ to checkout the library features.

API ENDPONTS
------------

This module exposes some API endpoints that enable you work with MPESA API

1. mpesa/submit/
    This endpoint allows you to submit a post request to initiate an STK push

2. mpesa/confirm/
    This endpoint is used as the callback endpoint on which MPESA will return a transaction response/status
    
3. mpesa/check-transaction/
    This endpoint allows you to manually check for the status of an mpesa transaction
    
Check out the `test module <https://github.com/Ekirapapaul/django-mpesa/tree/master/tests>`__ for more elaborate examples
