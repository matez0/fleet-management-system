import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'project.wsgi.application'

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Messaging:
FMS_RMQ_EXCHANGE = os.getenv('FMS_RMQ_EXCHANGE', 'fms')
FMS_RMQ_URL = os.getenv('FMS_RMQ_URL', 'amqp://guest:guest@localhost:5672')
