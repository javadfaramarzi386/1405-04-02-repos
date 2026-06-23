# accounts/signals.py

# سیگنال‌های جنگو برای اجرای خودکار کدها در زمان رخ دادن رویدادها
from django.db.models.signals import post_save

# دکوراتور receiver برای اتصال تابع به سیگنال‌ها
from django.dispatch import receiver

# مدل پیش‌فرض کاربر در جنگو
from django.contrib.auth.models import User

# مدل پروفایل سفارشی پروژه
from .models import Profile


# ----------------------------------------
# ایجاد خودکار پروفایل بعد از ساخت کاربر
# ----------------------------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    این سیگنال بعد از ذخیره شدن User اجرا می‌شود.

    هدف:
    - اگر کاربر تازه ایجاد شده باشد (created=True)
      برای او یک Profile ساخته شود

    این کار باعث می‌شود:
    - نیازی به ساخت دستی Profile نباشد
    - ساختار داده همیشه کامل و یکپارچه باشد
    """

    if created:
        # ایجاد خودکار پروفایل برای کاربر جدید
        Profile.objects.create(user=instance)


# ----------------------------------------
# ذخیره خودکار پروفایل هنگام ذخیره کاربر
# ----------------------------------------
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    این سیگنال هر بار که کاربر ذخیره (save) می‌شود اجرا می‌شود.

    هدف:
    - اطمینان از اینکه تغییرات مرتبط با پروفایل نیز ذخیره شوند

    نکته:
    - اگر پروفایل وجود داشته باشد، آن را نیز ذخیره می‌کند
    """

    # بررسی اینکه کاربر واقعاً پروفایل دارد
    # (جلوگیری از خطای AttributeError)
    if hasattr(instance, 'profile'):
        instance.profile.save()