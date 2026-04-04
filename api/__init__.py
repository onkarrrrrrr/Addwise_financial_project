import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Get WSGI application
app = get_wsgi_application()
