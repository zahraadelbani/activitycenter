import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Use environment variables for secrets
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")

# Disable DEBUG in production
DEBUG = True  # Set False only in production

# Allowed Hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',  # Required for Django AllAuth
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    # Django AllAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Your apps
    'users',
    'clubs',
    #'events',
    'messaging',
    'polls',
    'feedback',
    #'announcements',
    'analytics',
    'activity_center_admin',
    'club_leader',
    'rector',
    'club_member',
    #'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
#email integration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your SMTP provider if different
EMAIL_PORT = 587
EMAIL_USE_TLS = True 

import environ

env = environ.Env()
environ.Env.read_env()

EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


# Set your custom user model
AUTH_USER_MODEL = "users.User"

# Tell Django-Allauth to STOP using username
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_AUTO_LOGIN = False  # Prevents auto-login after signup
SOCIALACCOUNT_ENABLED = True


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = int(os.getenv("SITE_ID", 6))  

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login/'  
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False 




SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}



ACCOUNT_EMAIL_VERIFICATION = "none" 
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/dashboard/"
SOCIALACCOUNT_ADAPTER = "users.adapters.MySocialAccountAdapter"

ACCOUNT_ADAPTER = "users.account_adapter.CustomAccountAdapter"

# Default session expiration (24 hours)
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds

# Ensure session persists for 24 hours unless "Remember Me" is checked
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keeps session active until expiration

# Do not reset expiration time on every request
SESSION_SAVE_EVERY_REQUEST = False  # Ensures session expires exactly after 24 hours


# Remove SSL/HTTPS configurations
# These were causing the "only supports HTTP" issue
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_HSTS_SECONDS = 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_HSTS_PRELOAD = False
# X_FRAME_OPTIONS = "DENY"

# Fix how AllAuth displays users
ACCOUNT_USER_DISPLAY = lambda user: user.name

# Force Django-Allauth to use our CustomSignupForm
ACCOUNT_FORMS = {"signup": "users.forms.CustomSignupForm"}

# Root URL configuration
ROOT_URLCONF = 'club_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Corrected path
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


# Directory where Django will search for additional static files
#STATICFILES_DIRS = [
 #   os.path.join(BASE_DIR, 'static'),
#] 

# Directory where Django collects all static files (useful in production)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WSGI_APPLICATION = 'club_management.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# MEDIA & STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # ✅ Corrected
MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR / "media"  # ✅ Corrected
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}