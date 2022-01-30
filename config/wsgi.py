"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

config_name = os.environ.get('CONFIG_NAME')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{config_name}')


application = get_wsgi_application()
