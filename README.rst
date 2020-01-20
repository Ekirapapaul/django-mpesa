=====
mpesa
=====

Django-Mpesa is a generic python library that interfaces the safaricom
MPESA APIs to enable easy payments to your python application.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-mpesa',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('mpesa/', include(mpesa_urls)),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/mpesa/ to checkout the library features.