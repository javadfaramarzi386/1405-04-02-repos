# forum/admin.py

# سیستم مدیریت جنگو (Django Admin)
from django.contrib import admin

# وارد کردن مدل‌های اپلیکیشن forum
from .models import Category, Post, Comment


# ----------------------------------------
# تنظیمات نمایش مدل Category در پنل ادمین
# ----------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    تنظیمات مربوط به نمایش دسته‌بندی‌ها در Django Admin

    هدف:
    - نمایش ساده و خوانا از دسته‌بندی‌ها
    - کمک به مدیریت بهتر محتوا
    """

    # ستون‌هایی که در لیست نمایش داده می‌شوند
    list_display = ['name', 'slug']


# ----------------------------------------
# تنظیمات نمایش مدل Post در پنل ادمین
# ----------------------------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    مدیریت پست‌ها در پنل ادمین

    امکانات:
    - نمایش اطلاعات مهم هر پست
    - فیلتر بر اساس وضعیت تایید و دسته‌بندی
    - جستجو در عنوان و محتوا
    """

    # ستون‌های قابل نمایش در لیست پست‌ها
    list_display = ['title', 'author', 'category', 'created_at', 'is_approved']

    # فیلترهای کناری (Sidebar filters)
    list_filter = ['is_approved', 'category']

    # قابلیت جستجو در پنل ادمین
    search_fields = ['title', 'content']


# ----------------------------------------
# تنظیمات نمایش مدل Comment در پنل ادمین
# ----------------------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    مدیریت کامنت‌ها در پنل ادمین

    هدف:
    - مشاهده نظرات کاربران
    - مدیریت وضعیت تایید کامنت‌ها
    """

    # اطلاعاتی که در لیست کامنت‌ها نمایش داده می‌شود
    list_display = ['post', 'author', 'created_at', 'is_approved']

    # فیلتر بر اساس وضعیت تایید کامنت
    list_filter = ['is_approved']