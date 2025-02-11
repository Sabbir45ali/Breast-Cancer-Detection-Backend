import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n6(rql2@u)6)je3yw&m5c01a6x$f!=mdqx9s@wd8s$s&!!2aat'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
    # django's admin interface
    'django.contrib.admin',   
    # authentication framework
    'django.contrib.auth', 
    # Content type system     
    'django.contrib.contenttypes', 
    # Session framework
    'django.contrib.sessions',
    # Messaging framework      
    'django.contrib.messages',
    # Static files handling
    'django.contrib.staticfiles',
    # corsheader
    "corsheaders",
	# Django REST Framework for API development
    'rest_framework',
    # Token authentication for APIs
    'rest_framework.authtoken',
	# User authentication and registration
	'dj_rest_auth.registration',
    # REST-based authentication
    'dj_rest_auth',
	# Required by django-allauth
    'django.contrib.sites',
    # Authentication framework for Django
    'allauth',
    # Account management for django-allauth
    'allauth.account',
	# Social authentication support
    'allauth.socialaccount',
    # Google authentication provider
    'allauth.socialaccount.providers.google',
    #Simple JWT authentication
    'rest_framework_simplejwt',
    # Local app (django-admin startapp accounts)
    "accounts",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Middleware for handling CORS
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    # Cross-Site Request Forgery protection
    'django.middleware.csrf.CsrfViewMiddleware',
    # User authentication handling
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware for django-allauth
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'backend_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django's Allauth Configuration

SITE_ID = 1
# Disabling username field for authentication
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# No need for a username
ACCOUNT_USERNAME_REQUIRED = False
# Email is mandatory for authentication
ACCOUNT_EMAIL_REQUIRED = True
# Use email instead of username for login
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# Enforce email verification
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Django rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        # JWT authentication using cookies
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        
    ),
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        
        # Simple JWT authentication
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        
    ],
}

# JWT Authentication Settings
from datetime import timedelta
SIMPLE_JWT = {
    
    # Token expires after 5 minutes
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    # Refresh token expires after 2 hours
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=2),
}

# REST Auth settings
REST_AUTH = {
    
    'USE_JWT': True,
    # Name of the access token cookie
    'JWT_AUTH_COOKIE': 'access',
    # Name of the refresh token cookie
    'JWT_AUTH_REFRESH_COOKIE': 'refresh',
    #For getting the refresh token
    'JWT_AUTH_HTTPONLY': False,
    # Set to True when using HTTPS in production
    'JWT_AUTH_SECURE': False,  
    # Cookie SameSite policy
    'JWT_AUTH_SAMESITE': 'Lax',
    # Disable session-based login
    'SESSION_LOGIN': False,
    # Enable old password validation on password change
    'OLD_PASSWORD_FIELD_ENABLED': True,
}

# CORS headers settings (allow requests from frontend running on localhost:3000)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ronitbiswas8483@gmail.com'
EMAIL_HOST_PASSWORD = 'cybd nwfq ycgz glzi'

# Custom user model setting
# "Using a custom user model for authentication"
AUTH_USER_MODEL = "accounts.CustomUserModel"