import django
import os
import sys


def execute_in_django(operation):
    if operation and callable(operation):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.abspath(BASE_DIR))
        sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))
        os.environ['DJANGO_SETTINGS_MODULE'] = 'Inventarisation.settings'

        django.setup()
        operation()
