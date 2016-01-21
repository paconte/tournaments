"""
WSGI config for restdjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append(project)
sys.path.append('/home/django')
sys.path.append('/home/django/django-tournament.git/restdjango')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restdjango.apache.settings_apache")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
