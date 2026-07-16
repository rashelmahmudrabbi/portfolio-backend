import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
os.environ.setdefault('VERCEL', '1')

from django.core.wsgi import get_wsgi_application

# Vercel's Python runtime looks for a WSGI-callable named `app` in this file.
app = get_wsgi_application()
