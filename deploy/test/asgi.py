# Python
import os

# Django
from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'settings.env.local'
)

application = get_asgi_application()
