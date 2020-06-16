import django
from os import environ
from sys import path

path.append('..')

environ['DJANGO_SETTINGS_MODULE'] = 'vhs_store.settings'
print(environ['DJANGO_SETTINGS_MODULE'])

django.setup()
