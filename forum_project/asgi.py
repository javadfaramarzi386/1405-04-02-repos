"""
ASGI config for forum_project project.

ASGI (Asynchronous Server Gateway Interface) نقطه ورود پروژه جنگو برای
اجرای اپلیکیشن در حالت asynchronous است.

این فایل توسط سرورهای ASGI (مثل Uvicorn یا Daphne) استفاده می‌شود.

It exposes the ASGI callable as a module-level variable named ``application``.

برای اطلاعات بیشتر:
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# ماژول سیستم‌عامل برای مدیریت متغیرهای محیطی
import os

# تابع اصلی جنگو برای ساخت ASGI application
from django.core.asgi import get_asgi_application

# تنظیم متغیر محیطی پیش‌فرض برای معرفی فایل تنظیمات پروژه
# این خط به جنگو می‌گوید از کدام settings استفاده کند
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_project.settings')

# ساخت و معرفی ASGI application
# این متغیر توسط سرور ASGI استفاده می‌شود
application = get_asgi_application()