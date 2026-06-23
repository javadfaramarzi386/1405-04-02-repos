# accounts/urls.py

# تابع path برای تعریف مسیرهای URL در جنگو
from django.urls import path

# ویوهای آماده جنگو برای سیستم احراز هویت (Login, Logout, Reset Password)
from django.contrib.auth import views as auth_views

# ویوهای اختصاصی اپلیکیشن accounts
from . import views

# نام‌گذاری فضای URL برای جلوگیری از تداخل با اپ‌های دیگر
app_name = 'accounts'


# ----------------------------------------
# لیست مسیرهای مربوط به حساب کاربری
# ----------------------------------------
urlpatterns = [

    # ------------------------------------
    # ثبت‌نام کاربر جدید (ویو اختصاصی)
    # ------------------------------------
    path('register/', views.register, name='register'),

    # ------------------------------------
    # ورود کاربر (Login)
    # استفاده از ویو آماده جنگو
    # ------------------------------------
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',  # قالب صفحه ورود
            redirect_authenticated_user=True,         # اگر کاربر لاگین باشد، ریدایرکت شود
            extra_context={'title': 'صفحه ورود'}      # ارسال داده اضافی به قالب
        ),
        name='login'
    ),

    # ------------------------------------
    # خروج کاربر (Logout)
    # ------------------------------------
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),  # بعد از خروج → صفحه home
        name='logout'
    ),

    # ------------------------------------
    # درخواست بازیابی رمز عبور (Step 1)
    # کاربر ایمیل وارد می‌کند
    # ------------------------------------
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
            subject_template_name='registration/password_reset_subject.txt',
            email_template_name='registration/password_reset_email.html',
            success_url='/accounts/password-reset/done/'
        ),
        name='password_reset'
    ),

    # ------------------------------------
    # نمایش پیام ارسال ایمیل موفق
    # ------------------------------------
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # ------------------------------------
    # مرحله تنظیم رمز جدید (لینک ایمیل)
    # uidb64 و token برای امنیت لینک هستند
    # ------------------------------------
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # ------------------------------------
    # تکمیل فرآیند تغییر رمز عبور
    # ------------------------------------
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # ------------------------------------
    # نمایش پروفایل کاربر فعلی
    # ------------------------------------
    path('profile/', views.profile_view, name='profile'),

    # ------------------------------------
    # ویرایش پروفایل کاربر فعلی
    # ------------------------------------
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # ------------------------------------
    # مشاهده پروفایل کاربران دیگر
    # با استفاده از username
    # ------------------------------------
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),

    # ------------------------------------
    # گزارش دادن به یک کاربر خاص
    # ------------------------------------
    path('profile/<str:username>/report/', views.report_user, name='report_user'),
]