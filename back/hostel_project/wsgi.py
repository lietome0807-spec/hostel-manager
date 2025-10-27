"""
WSGI config for hostel_project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_project.settings')

application = get_wsgi_application()
