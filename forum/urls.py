# forum/urls.py

# تابع اصلی برای تعریف مسیرهای URL در جنگو
from django.urls import path

# ایمپورت ویوهای اپلیکیشن forum
from . import views

# namespace برای جلوگیری از تداخل نام URLها بین اپ‌ها
app_name = 'forum'  # ← بسیار مهم برای استفاده در reverse و template‌ها


# ----------------------------------------
# لیست مسیرهای مربوط به فروم
# ----------------------------------------
urlpatterns = [

    # ------------------------------------
    # نمایش لیست همه پست‌ها (صفحه اصلی فروم)
    # ------------------------------------
    path('', views.post_list, name='post_list'),

    # ------------------------------------
    # نمایش پست‌های یک دسته‌بندی خاص
    # slug برای SEO-friendly URL
    # ------------------------------------
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),

    # ------------------------------------
    # جزئیات یک پست خاص
    # pk = شناسه عددی پست
    # ------------------------------------
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # ------------------------------------
    # ایجاد پست جدید
    # ------------------------------------
    path('post/create/', views.create_post, name='create_post'),

    # ------------------------------------
    # ویرایش پست موجود
    # ------------------------------------
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),

    # ------------------------------------
    # حذف پست
    # ------------------------------------
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

    # ------------------------------------
    # لایک کردن پست (toggle like system)
    # ------------------------------------
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
]