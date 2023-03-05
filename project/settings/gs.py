"""
Django settings for the project.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-djhfkwiruwe9324924nmxcn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'gps_simulator',
]

MIDDLEWARE = [
]
