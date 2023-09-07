# Python
import os

# Django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'settings.env.local'
)

application = get_wsgi_application()
