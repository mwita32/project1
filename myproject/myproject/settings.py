import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = True

# Allow all hosts (for development)
ALLOWED_HOSTS = ['*']

# Installed apps
INSTALLED_APPS = [
    'myapp',  # Your custom app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware configurations
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL Configuration
ROOT_URLCONF = 'myproject.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = 'myproject.wsgi.application'

# Database Configuration (MySQL on WAMP)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',  # Name of your database in MySQL
        'USER': 'root',  # Replace with your MySQL username
        'PASSWORD': '',  # Replace with your MySQL password
        'HOST': '127.0.0.1',  # Localhost (WAMP Server)
        'PORT': '3306',  # Default MySQL Port
        'OPTIONS': {
            'charset': 'utf8mb4',  # Fix encoding issues
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # Ensures data integrity
        }
    }
}

# Authentication Model
AUTH_USER_MODEL = 'myapp.CustomUser'

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Email Configuration (For sending account-related emails)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'josephmanga504@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'oaen rhzw vpmc xcfp'  # Replace with your email password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Static Files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'myapp', 'static')]  # Ensure static files are properly served

# Media Files (User Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging (Optional - Helps in Debugging)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

AUTH_PASSWORD_VALIDATORS = []
