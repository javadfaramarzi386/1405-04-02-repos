"""
WSGI config for forum_project project.

WSGI (Web Server Gateway Interface) نقطه ورود استاندارد جنگو برای اجرای پروژه
در حالت synchronous است.

این فایل توسط وب‌سرورهایی مثل Gunicorn یا uWSGI استفاده می‌شود.

It exposes the WSGI callable as a module-level variable named ``application``.

برای اطلاعات بیشتر:
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

# ماژول سیستم‌عامل برای مدیریت متغیرهای محیطی
import os

# تابع ساخت WSGI application از جنگو
from django.core.wsgi import get_wsgi_application

# تعیین مسیر تنظیمات پروژه
# این خط مشخص می‌کند جنگو از کدام settings استفاده کند
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_project.settings')

# ساخت WSGI application برای استفاده توسط سرور
application = get_wsgi_application()