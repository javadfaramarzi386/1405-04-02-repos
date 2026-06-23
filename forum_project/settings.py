"""
Django settings for forum_project project.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ========================================
# تنظیمات امنیتی و توسعه
# ========================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dzh0^t5i#)cvq^u-gb^1to@8bp+ygt8l(b1w^stti%(o&wded1')

# در Render و Railway این مقدار از محیط خوانده می‌شود
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ['*']


# ========================================
# اپلیکیشن‌ها
# ========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # اپ‌های پروژه
    'accounts',
    'forum',

    # برای static files در production
    'whitenoise.runserver_nostatic',
]


# ========================================
# Middleware
# ========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← مهم برای static
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ========================================
# دیگر تنظیمات پایه
# ========================================
ROOT_URLCONF = 'forum_project.urls'
WSGI_APPLICATION = 'forum_project.wsgi.application'


# ========================================
# Templates
# ========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ========================================
# دیتابیس (PostgreSQL)
# ========================================
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:Jzf13890422@localhost:5432/postgres',
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# ========================================
# اعتبارسنجی رمز عبور
# ========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ========================================
# تنظیمات بین‌المللی
# ========================================
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True


# ========================================
# احراز هویت
# ========================================
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# ========================================
# Static & Media Files
# ========================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ========================================
# تنظیمات اضافی
# ========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# امنیت بیشتر در production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True