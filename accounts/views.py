from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login

from .forms import ProfileForm, UserRegistrationForm
from .models import Profile, Report


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserRegistrationForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
            return redirect('home')
        else:
            messages.error(request, "خطا در ثبت‌نام. لطفاً اطلاعات را بررسی کنید.")

    return render(request, 'accounts/register.html', {
        'form': form,
        'title': 'ثبت‌نام'
    })


@login_required
def profile_view(request):
    return redirect('accounts:profile_detail', username=request.user.username)


def profile_detail(request, username):
    target_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=target_user)

    return render(request, 'accounts/profile_detail.html', {
        'target_profile': profile,
        'target_user': target_user,
        'is_own_profile': request.user == target_user
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل بروزرسانی شد")
            return redirect('accounts:profile_detail', username=request.user.username)

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })


@login_required
def report_user(request, username):
    reported_user = get_object_or_404(User, username=username)

    if reported_user == request.user:
        messages.error(request, "نمی‌توانید خودتان را گزارش دهید.")
        return redirect('accounts:profile_detail', username=username)

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()

        if len(reason) < 10:
            messages.error(request, "دلیل گزارش باید حداقل ۱۰ کاراکتر باشد.")
            return redirect('accounts:profile_detail', username=username)

        if not Report.objects.filter(
            reporter=request.user,
            reported_user=reported_user,
            reason=reason
        ).exists():

            Report.objects.create(
                reporter=request.user,
                reported_user=reported_user,
                reason=reason
            )

            messages.success(request, "گزارش ثبت شد.")

        return redirect('accounts:profile_detail', username=username)

    return render(request, 'accounts/report_user.html', {
        'reported_user': reported_user
    })


def home_page(request):
    return render(request, 'accounts/home.html')