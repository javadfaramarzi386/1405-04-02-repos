# accounts/views.py

# توابع کمکی برای رندر صفحات، ریدایرکت و گرفتن آبجکت یا 404
from django.shortcuts import render, redirect, get_object_or_404

# دکوراتور برای محدود کردن دسترسی به کاربران لاگین‌شده
from django.contrib.auth.decorators import login_required

# مدل پیش‌فرض کاربر جنگو
from django.contrib.auth.models import User

# سیستم پیام‌رسانی جنگو (نمایش پیام موفقیت / خطا به کاربر)
from django.contrib import messages

# تابع login برای لاگین کردن کاربر بعد از ثبت‌نام
from django.contrib.auth import login

# فرم‌های پروژه (ثبت‌نام و ویرایش پروفایل)
from .forms import ProfileForm, UserRegistrationForm

# مدل‌های پروژه (پروفایل و گزارش کاربران)
from .models import Profile, Report


# --------------------------------------------------
# ثبت نام کاربران جدید
# --------------------------------------------------
def register(request):
    """
    ثبت‌نام کاربر جدید در سیستم

    مراحل:
    1. بررسی لاگین بودن کاربر (اگر لاگین باشد → هدایت به خانه)
    2. دریافت اطلاعات از فرم
    3. اعتبارسنجی و ذخیره کاربر
    4. ایجاد پروفایل (در صورت نبود سیگنال)
    5. لاگین خودکار کاربر
    """

    # اگر کاربر قبلاً لاگین کرده باشد، نیازی به ثبت‌نام ندارد
    if request.user.is_authenticated:
        return redirect('home')

    # اگر فرم ارسال شده باشد
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        # بررسی اعتبار داده‌ها
        if form.is_valid():
            user = form.save()

            # ایجاد پروفایل (اگر به هر دلیل توسط signal ساخته نشده باشد)
            Profile.objects.get_or_create(user=user)

            # لاگین خودکار بعد از ثبت‌نام
            login(request, user)

            # پیام موفقیت برای UI
            messages.success(request, "ثبت‌نام با موفقیت انجام شد. خوش آمدید!")

            return redirect('home')

    else:
        # نمایش فرم خالی برای GET request
        form = UserRegistrationForm()

    # رندر صفحه ثبت‌نام
    return render(request, 'accounts/register.html', {
        'form': form,
        'title': 'ثبت‌نام در سایت'
    })


# --------------------------------------------------
# نمایش پروفایل کاربر فعلی
# --------------------------------------------------
@login_required
def profile_view(request):
    """
    این ویو فقط کاربر لاگین‌شده را به صفحه پروفایل خودش هدایت می‌کند.
    """
    return redirect('accounts:profile_detail', username=request.user.username)


# --------------------------------------------------
# نمایش پروفایل کاربران دیگر
# --------------------------------------------------
def profile_detail(request, username):
    """
    نمایش پروفایل هر کاربر بر اساس username

    نکته:
    - اگر پروفایل وجود نداشته باشد، به صورت خودکار ساخته می‌شود
    - این کار برای کاربران قدیمی یا ناقص بودن داده‌هاست
    """

    # پیدا کردن کاربر بر اساس نام کاربری
    target_user = get_object_or_404(User, username=username)

    # گرفتن پروفایل یا ساخت آن در صورت نبود
    profile, created = Profile.objects.get_or_create(user=target_user)

    # بررسی اینکه آیا کاربر در حال مشاهده پروفایل خودش است یا نه
    is_own_profile = request.user == target_user

    # ارسال داده‌ها به قالب
    return render(request, 'accounts/profile_detail.html', {
        'target_profile': profile,
        'target_user': target_user,
        'is_own_profile': is_own_profile,
        'title': f"پروفایل {target_user.get_full_name() or target_user.username}"
    })


# --------------------------------------------------
# ویرایش پروفایل کاربر لاگین‌شده
# --------------------------------------------------
@login_required
def edit_profile(request):
    """
    ویرایش اطلاعات پروفایل کاربر فعلی
    """

    # گرفتن پروفایل یا ساخت آن در صورت نبود
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # فرم همراه با داده‌های POST و فایل‌ها (مثل عکس)
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            messages.success(request, "پروفایل شما با موفقیت بروزرسانی شد.")

            return redirect('accounts:profile_detail', username=request.user.username)

    else:
        # نمایش فرم با اطلاعات فعلی پروفایل
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'title': 'ویرایش پروفایل'
    })


# --------------------------------------------------
# گزارش دادن به کاربران دیگر
# --------------------------------------------------
@login_required
def report_user(request, username):
    """
    ثبت گزارش تخلف علیه یک کاربر

    ویژگی‌ها:
    - جلوگیری از گزارش خود کاربر
    - اعتبارسنجی دلیل گزارش
    - جلوگیری از گزارش تکراری
    """

    # کاربری که قرار است گزارش شود
    reported_user = get_object_or_404(User, username=username)

    # جلوگیری از گزارش دادن به خود
    if reported_user == request.user:
        messages.error(request, "نمی‌توانید خودتان را گزارش دهید.")
        return redirect('profile_detail', username=username)

    if request.method == 'POST':
        # دریافت دلیل گزارش از فرم HTML
        reason = request.POST.get('reason', '').strip()

        # بررسی خالی نبودن دلیل
        if not reason:
            messages.error(request, "لطفاً دلیل گزارش را وارد کنید.")
            return redirect('profile_detail', username=username)

        # بررسی حداقل طول توضیح
        if len(reason) < 10:
            messages.error(request, "لطفاً دلیل گزارش را با جزئیات بنویسید (حداقل ۱۰ کاراکتر).")
            return redirect('profile_detail', username=username)

        # جلوگیری از ثبت گزارش تکراری
        if Report.objects.filter(
                reporter=request.user,
                reported_user=reported_user,
                reason=reason
        ).exists():
            messages.warning(request, "شما قبلاً این گزارش را ثبت کرده‌اید.")
            return redirect('profile_detail', username=username)

        # ثبت گزارش جدید در دیتابیس
        Report.objects.create(
            reporter=request.user,
            reported_user=reported_user,
            reason=reason
        )

        messages.success(request, "گزارش شما با موفقیت ثبت شد و توسط مدیریت بررسی خواهد شد.")
        return redirect('profile_detail', username=username)

    # نمایش فرم گزارش (GET request)
    return render(request, 'accounts/report_user.html', {
        'reported_user': reported_user,
        'title': f'گزارش کاربر {reported_user.username}'
    })


# --------------------------------------------------
# صفحه اصلی سایت
# --------------------------------------------------
def home_page(request):
    """
    صفحه اصلی سایت
    """
    return render(request, 'accounts/home.html', {
        'title': 'خانه'
    })