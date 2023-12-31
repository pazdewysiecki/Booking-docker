"""
WSGI config for reservations project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from email.mime import application
from dj_static import Cling

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings.production')

#para local:

#application = get_wsgi_application()

#para producción:

application = Cling(get_wsgi_application())


