"""
IMPORTANT: This file changed to support 'whitenoise' for testing purposes
"""
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
from django.conf import settings


application = get_wsgi_application()
application = WhiteNoise(application, root=settings.BASE_DIR + '/assets')
application.add_files(settings.BASE_DIR + '/assets', prefix='')

"""
### Ordinary wsgi file
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flytech.settings.dev')

application = get_wsgi_application()
"""
