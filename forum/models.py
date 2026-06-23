# forum/models.py

# هسته اصلی مدل‌های پایگاه داده در جنگو
from django.db import models

# مدل پیش‌فرض کاربر در سیستم احراز هویت جنگو
from django.contrib.auth.models import User

# ابزارهای زمانی جنگو (در این کد فعلاً استفاده نشده)
from django.utils import timezone


# ----------------------------------------
# مدل دسته‌بندی (Category)
# ----------------------------------------
class Category(models.Model):
    """
    این مدل برای دسته‌بندی پست‌های انجمن استفاده می‌شود.

    هر پست می‌تواند متعلق به یک دسته‌بندی باشد.
    """

    # نام دسته‌بندی (نمایشی برای کاربر)
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")

    # شناسه یکتا برای URLها (مثلاً /category/python)
    # null=True و blank=True یعنی موقتاً اختیاری است
    slug = models.SlugField(unique=True, null=True, blank=True)

    # توضیحات بیشتر درباره دسته‌بندی
    description = models.TextField(blank=True, verbose_name="توضیحات")

    def __str__(self):
        """
        نمایش شیء در پنل ادمین و محیط‌های مختلف
        """
        return self.name

    class Meta:
        """
        تنظیمات متا برای مدل Category
        """

        # نام‌های نمایشی در پنل ادمین
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


# ----------------------------------------
# مدل پست (Post)
# ----------------------------------------
class Post(models.Model):
    """
    این مدل نماینده یک موضوع یا پست در فروم است.

    ویژگی‌ها:
    - عنوان و متن پست
    - نویسنده
    - دسته‌بندی
    - وضعیت تأیید
    - سیستم لایک
    - زمان ایجاد و ویرایش
    """

    # عنوان پست
    title = models.CharField(max_length=200, verbose_name="عنوان موضوع")

    # محتوای اصلی پست
    content = models.TextField(verbose_name="متن پست")

    # نویسنده پست (ارتباط با User)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    # دسته‌بندی پست (در صورت حذف دسته‌بندی، مقدار NULL می‌شود)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )

    # زمان ایجاد پست (خودکار)
    created_at = models.DateTimeField(auto_now_add=True)

    # زمان آخرین ویرایش پست (خودکار)
    updated_at = models.DateTimeField(auto_now=True)

    # وضعیت تأیید توسط مدیریت
    is_approved = models.BooleanField(
        default=True,
        verbose_name="تایید شده توسط مدیریت"
    )

    # سیستم لایک (رابطه Many-to-Many بین کاربران و پست‌ها)
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )

    def __str__(self):
        """
        نمایش پست در پنل ادمین
        """
        return self.title

    class Meta:
        """
        تنظیمات کلی مدل Post
        """

        # مرتب‌سازی پیش‌فرض: جدیدترین پست‌ها اول
        ordering = ['-created_at']

        # نام‌های نمایشی در پنل ادمین
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"


# ----------------------------------------
# مدل کامنت (Comment)
# ----------------------------------------
class Comment(models.Model):
    """
    این مدل برای ذخیره نظرات کاربران زیر پست‌ها استفاده می‌شود.

    هر کامنت:
    - به یک پست مرتبط است
    - توسط یک کاربر نوشته می‌شود
    """

    # پستی که کامنت زیر آن ثبت شده است
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # نویسنده کامنت
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # متن کامنت
    content = models.TextField(verbose_name="متن نظر")

    # زمان ثبت کامنت
    created_at = models.DateTimeField(auto_now_add=True)

    # وضعیت تأیید کامنت (برای moderation)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        """
        نمایش کامنت در پنل ادمین

        نمایش کوتاه شده از متن پست برای خوانایی بهتر
        """
        return f"نظر {self.author} در {self.post.title[:30]}"

    class Meta:
        """
        تنظیمات مدل Comment
        """

        # نمایش کامنت‌ها از قدیمی به جدید (برای بحث‌ها منطقی‌تر است)
        ordering = ['created_at']

        # نام‌های نمایشی در پنل ادمین
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"