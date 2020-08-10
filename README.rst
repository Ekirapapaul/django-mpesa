=====
mpesa
=====

Django-Mpesa is a generic python library that interfaces the safaricom
MPESA APIs to enable easy payments to your python application.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "mpesa" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mpesa',
    ]

2. Include the polls URLconf in your project urls.py like this::

    from django.urls import path, include
    from mpesa.urls import mpesa_urls

    path('mpesa/', include(mpesa_urls)),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/mpesa/ to checkout the library features.

API ENDPONTS
-----------

This module exposes some API endpoints that enable you work with MPESA API

1. mpesa/submit/
    This endpoint allows you to submit a post request to initiate an STK push

2. mpesa/confirm/
    This endpoint is used as the callback endpoint on which MPESA will return a transaction response/status
    
3. mpesa/checktransaction/
    This endpoint allows you to manually check for the status of an mpesa transaction
    
Check out the `test module <https://github.com/Ekirapapaul/django-mpesa/tree/master/tests>`__ for more elaborate examples
