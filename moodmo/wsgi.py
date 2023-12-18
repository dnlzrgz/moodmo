"""
WSGI config for moodmo project.
"""

import os
from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moodmo.settings")

application = get_wsgi_application()
application = WhiteNoise(application)
application.add_files(
    "/app/staticfiles",
    prefix="staticfiles/",
)
