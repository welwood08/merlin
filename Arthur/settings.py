# Django settings for Arthur project.

from Core.config import Config
import re

hostre = re.compile("https?://([^/:]+).*")

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'Arthur.errors.exceptions',
    'Arthur.errors.db',
    'Arthur.views.graphs.graphs',
)

APPEND_SLASH = True

ROOT_URLCONF = 'Arthur'

INSTALLED_APPS = (
    'Arthur',
)

SECRET_KEY = Config.get("Arthur", "secretkey", raw=True)

ALLOWED_HOSTS = (
    hostre.match(Config.get("URL", "arthur")).group(1),
)
# Get all alturls
for url in Config.items("alturls"):
    ALLOWED_HOSTS += ( hostre.match(url[1]).group(1), )

