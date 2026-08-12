"""
WSGI config for ebookstore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebookstore.settings')

# Ensure media directories exist and are writable before the first request
# is handled. This is critical when a persistent volume is mounted at
# MEDIA_ROOT (/app/media) because the mount point may be empty on first boot.
from django.core.management import call_command  # noqa: E402
try:
    call_command("ensure_media_dir", verbosity=0)
except Exception as exc:  # pragma: no cover
    import warnings
    warnings.warn(f"ensure_media_dir failed: {exc}", RuntimeWarning, stacklevel=1)

application = get_wsgi_application()
