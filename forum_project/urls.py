"""
URL configuration for forum_project project.

این فایل نقطه مرکزی مدیریت تمام URLهای پروژه است.
تمام درخواست‌های کاربران از اینجا به اپ‌های مربوطه هدایت می‌شوند.

The `urlpatterns` list routes URLs to views.

برای اطلاعات بیشتر:
https://docs.djangoproject.com/en/6.0/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf
    1. Import include: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# پنل مدیریت جنگو
from django.contrib import admin

# ابزار تعریف مسیرها و اتصال اپ‌ها
from django.urls import path, include

# تنظیمات پروژه (برای MEDIA و STATIC)
from django.conf import settings

# برای سرو فایل‌های media در حالت توسعه
from django.conf.urls.static import static

# ویو صفحه اصلی سایت
from accounts.views import home_page


# ----------------------------------------
# تعریف مسیرهای اصلی پروژه
# ----------------------------------------
urlpatterns = [
    # صفحه اصلی سایت (Home Page)
    path('', home_page, name='home'),

    # پنل مدیریت جنگو
    path('admin/', admin.site.urls),

    # مسیرهای مربوط به اپ accounts
    path('accounts/', include('accounts.urls')),

    # مسیرهای مربوط به اپ forum
    path('forum/', include('forum.urls')),
]

# ----------------------------------------
# سرو فایل‌های media در حالت development
# ----------------------------------------
# فقط در حالت DEBUG فعال است (برای production مناسب نیست)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)