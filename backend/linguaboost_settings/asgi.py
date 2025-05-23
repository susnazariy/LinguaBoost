""" ASGI config for linguaboost project """

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguaboost_settings.settings')

application = get_asgi_application()
