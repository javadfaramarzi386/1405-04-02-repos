# accounts/models.py

# هسته اصلی مدل‌های پایگاه داده در جنگو
from django.db import models

# مدل پیش‌فرض کاربر در جنگو (Authentication system)
from django.contrib.auth.models import User

# برای ایجاد خطاهای استاندارد در validation فیلدها
from django.core.exceptions import ValidationError

# کتابخانه Pillow برای پردازش و تغییر اندازه تصاویر
from PIL import Image


# ----------------------------------------
# اعتبارسنجی حجم تصویر پروفایل
# ----------------------------------------
def validate_image_size(image):
    """
    این تابع یک Validator سفارشی برای فیلد ImageField است.

    کاربرد:
    - قبل از ذخیره تصویر اجرا می‌شود
    - بررسی می‌کند حجم فایل از حد مجاز بیشتر نباشد

    اگر فایل بزرگ‌تر از حد تعیین‌شده باشد:
    - ذخیره در دیتابیس متوقف می‌شود
    - خطای ValidationError برگردانده می‌شود
    """

    # گرفتن حجم فایل آپلود شده (بر حسب بایت)
    file_size = image.file.size

    # تعیین سقف مجاز حجم فایل (مگابایت)
    limit_mb = 2.0

    # تبدیل مگابایت به بایت و مقایسه
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(
            f"حداکثر حجم عکس باید {limit_mb} مگابایت باشد."
        )


# ----------------------------------------
# مدل پروفایل کاربر
# ----------------------------------------
class Profile(models.Model):
    """
    این مدل اطلاعات تکمیلی کاربران را نگهداری می‌کند.

    دلیل وجود این مدل:
    - مدل User جنگو فقط اطلاعات پایه دارد
    - برای اطلاعات اضافی (مثل عکس، بیو، سن فرزند و ...)
      از یک مدل جدا (Profile) استفاده می‌کنیم

    ارتباط:
    - رابطه OneToOne با User
    - هر کاربر فقط یک پروفایل دارد
    """

    # ارتباط یک‌به‌یک با مدل User
    # اگر کاربر حذف شود، پروفایل هم حذف می‌شود
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # تصویر پروفایل کاربر
    avatar = models.ImageField(
        upload_to='avatars/',                 # مسیر ذخیره فایل‌ها در MEDIA_ROOT
        validators=[validate_image_size],     # اعتبارسنجی حجم فایل
        blank=True,                           # در فرم اجباری نیست
        null=True,                            # در دیتابیس می‌تواند NULL باشد
        verbose_name="عکس پروفایل"
    )

    # نام نمایشی یا مستعار کاربر
    nickname = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="نام مستعار (اختیاری)"
    )

    # توضیحات کاربر (معرفی خود یا فرزند)
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="درباره من"
    )

    # سن فرزند کاربر
    child_age = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="سن فرزند"
    )

    # نوع بیماری / شرایط خاص فرزند
    condition_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نوع معلولیت/شرایط فرزند"
    )

    # محل زندگی کاربر
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="شهر محل سکونت"
    )

    # ----------------------------------------
    # تنظیمات حریم خصوصی (Privacy Settings)
    # ----------------------------------------
    # این فیلدها تعیین می‌کنند چه اطلاعاتی
    # برای سایر کاربران قابل مشاهده باشد

    show_bio = models.BooleanField(
        default=True,
        verbose_name="نمایش درباره من"
    )

    show_child_age = models.BooleanField(
        default=True,
        verbose_name="نمایش سن فرزند"
    )

    show_condition_type = models.BooleanField(
        default=True,
        verbose_name="نمایش نوع شرایط"
    )

    show_location = models.BooleanField(
        default=True,
        verbose_name="نمایش شهر"
    )

    def __str__(self):
        """
        نمایش شیء در پنل ادمین جنگو

        اولویت نمایش:
        1. اگر nickname وجود داشته باشد → نمایش nickname
        2. در غیر این صورت → username کاربر
        """
        return self.nickname if self.nickname else self.user.username

    def save(self, *args, **kwargs):
        """
        بازنویسی متد save برای پردازش تصویر پروفایل

        فرآیند:
        1. ذخیره اولیه در دیتابیس انجام می‌شود
        2. اگر تصویر وجود داشته باشد:
           - باز می‌شود
           - بررسی ابعاد انجام می‌شود
           - در صورت بزرگ بودن، resize می‌شود
           - دوباره ذخیره می‌شود

        هدف:
        - کاهش حجم تصاویر
        - افزایش سرعت بارگذاری سایت
        - بهینه‌سازی فضای ذخیره‌سازی
        """

        # ذخیره اولیه مدل در دیتابیس
        super().save(*args, **kwargs)

        # اگر کاربر تصویر پروفایل داشته باشد
        if self.avatar:

            # باز کردن تصویر با Pillow
            img = Image.open(self.avatar.path)

            # بررسی ابعاد تصویر
            if img.height > 300 or img.width > 300:

                # تغییر اندازه تصویر با حفظ نسبت طول و عرض
                img.thumbnail((300, 300))

                # ذخیره مجدد تصویر فشرده شده
                img.save(self.avatar.path)


# ----------------------------------------
# مدل گزارش کاربران (Report System)
# ----------------------------------------
class Report(models.Model):
    """
    این مدل برای سیستم گزارش‌دهی کاربران استفاده می‌شود.

    کاربرد:
    - کاربران می‌توانند سایر کاربران را گزارش دهند
    - دلیل گزارش ذخیره می‌شود
    - برای مدیریت تخلفات در سیستم استفاده می‌شود
    """

    # کاربری که گزارش را ثبت کرده
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports_made',
        verbose_name="گزارش دهنده"
    )

    # کاربری که مورد گزارش قرار گرفته
    reported_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports_received',
        verbose_name="کاربر گزارش شده"
    )

    # دلیل یا توضیح گزارش
    reason = models.TextField(
        max_length=500,
        verbose_name="علت گزارش"
    )

    # زمان ثبت گزارش (به صورت خودکار)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        """
        نمایش گزارش در پنل مدیریت

        فرمت:
        گزارش علیه X توسط Y
        """
        return (
            f"گزارش علیه {self.reported_user.username} "
            f"توسط {self.reporter.username}"
        )

    class Meta:
        """
        تنظیمات متا (رفتار کلی مدل در دیتابیس و admin)
        """

        # مرتب‌سازی پیش‌فرض: جدیدترین گزارش‌ها اول
        ordering = ['-created_at']