from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use SQLite for local development by default, unless overridden by DATABASE_URL
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# Dummy email backend for console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
