import os
import sys
from pathlib import Path

# Add project root directory to python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Ensure settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from config.wsgi import application
from django.core.management import call_command

# Auto-initialize database schema and seed catalog on Vercel cold start
try:
    call_command('migrate', interactive=False)
    
    from apps.products.models import Product
    if Product.objects.count() == 0:
        call_command('seed_data')
except Exception as e:
    print(f"Auto DB initialization info: {e}")

# Export app for Vercel serverless deployment
app = application
