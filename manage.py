#!/usr/bin/env python

"""
اسکریپت مدیریت اصلی جنگو (Django Management Script)

این فایل نقطه ورود اجرای دستورات مدیریتی جنگو است،
مثل:
- اجرای سرور توسعه (runserver)
- ساخت مایگریشن‌ها (makemigrations)
- اعمال تغییرات دیتابیس (migrate)
- ایجاد ادمین (createsuperuser)
"""

import os
import sys


def main():
    """
    تابع اصلی اجرای دستورات جنگو از طریق خط فرمان
    """

    # تعیین فایل تنظیمات اصلی پروژه جنگو
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_project.settings')

    try:
        # ایمپورت هسته اجرای دستورات مدیریتی جنگو
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        # خطا در صورت نصب نبودن جنگو یا مشکل محیط مجازی
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc

    # اجرای دستوراتی که در ترمینال وارد شده‌اند
    execute_from_command_line(sys.argv)


# اگر این فایل مستقیماً اجرا شود (نه import)
if __name__ == '__main__':
    main()