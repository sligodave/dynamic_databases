
from django.conf import settings


PREFIX = getattr(settings, 'DYNAMIC_DATABASES_PREFIX', 'DYNAMIC_DATABASES')
SEPARATOR = getattr(settings, 'DYNAMIC_DATABASES_SEPARATOR', '_')
