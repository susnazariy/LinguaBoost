""" WSGI config for linguaboost project """

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguaboost_settings.settings')

application = get_wsgi_application()
