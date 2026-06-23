# forum/views.py

# توابع اصلی برای رندر صفحات، ریدایرکت و مدیریت 404
from django.shortcuts import render, redirect, get_object_or_404

# دکوراتور برای محدود کردن دسترسی به کاربران لاگین‌شده
from django.contrib.auth.decorators import login_required

# سیستم پیام‌های کاربری (success / error / warning)
from django.contrib import messages

# برای انجام aggregation مثل شمارش تعداد پست‌ها
from django.db.models import Count

# مدل‌های اپلیکیشن forum
from .models import Post, Category, Comment

# فرم‌های مربوط به پست و کامنت
from .forms import PostForm, CommentForm


# ----------------------------------------
# نمایش لیست پست‌ها (صفحه اصلی فروم)
# ----------------------------------------
def post_list(request):
    """
    این ویو صفحه اصلی فروم را نمایش می‌دهد.

    شامل:
    - لیست پست‌های تأیید شده
    - لیست دسته‌بندی‌ها همراه با تعداد پست‌ها
    """

    # گرفتن پست‌های تأیید شده (moderation system)
    posts = Post.objects.filter(
        is_approved=True
    ).select_related(
        'author', 'category'  # کاهش تعداد queryها (optimization)
    ).order_by('-created_at')

    # گرفتن دسته‌بندی‌ها + تعداد پست‌های هر دسته (aggregation)
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).order_by('name')

    return render(request, 'forum/post_list.html', {
        'posts': posts,
        'categories': categories,
        'title': 'فروم تبادل نظر'
    })


# ----------------------------------------
# نمایش پست‌های یک دسته‌بندی خاص
# ----------------------------------------
def category_posts(request, slug):
    """
    نمایش پست‌های مربوط به یک دسته‌بندی خاص بر اساس slug
    """

    # پیدا کردن دسته‌بندی یا بازگشت 404
    category = get_object_or_404(Category, slug=slug)

    # فیلتر پست‌ها بر اساس دسته‌بندی
    posts = Post.objects.filter(
        category=category,
        is_approved=True
    ).select_related('author').order_by('-created_at')

    # لیست دسته‌بندی‌ها برای sidebar
    categories = Category.objects.annotate(post_count=Count('posts'))

    return render(request, 'forum/post_list.html', {
        'posts': posts,
        'category': category,
        'categories': categories,
        'title': f'دسته‌بندی: {category.name}'
    })


# ----------------------------------------
# نمایش جزئیات یک پست + ارسال کامنت
# ----------------------------------------
def post_detail(request, pk):
    """
    این ویو هم نمایش پست را انجام می‌دهد
    و هم ارسال کامنت را مدیریت می‌کند.
    """

    # گرفتن پست تأیید شده یا 404
    post = get_object_or_404(Post, pk=pk, is_approved=True)

    # گرفتن کامنت‌های تأیید شده مربوط به پست
    comments = post.comments.filter(
        is_approved=True
    ).select_related('author').order_by('created_at')

    # ------------------------------------
    # ارسال کامنت (POST request)
    # ------------------------------------
    if request.method == 'POST':

        # بررسی لاگین بودن کاربر
        if not request.user.is_authenticated:
            messages.error(request, "برای ارسال نظر باید وارد حساب کاربری شوید.")
            return redirect('accounts:login')

        # ساخت فرم با داده‌های ارسال‌شده
        form = CommentForm(request.POST)

        if form.is_valid():
            # ساخت کامنت بدون ذخیره اولیه
            comment = form.save(commit=False)

            # اتصال کامنت به پست و کاربر
            comment.post = post
            comment.author = request.user

            # ذخیره نهایی در دیتابیس
            comment.save()

            messages.success(request, "نظر شما با موفقیت ثبت شد.")

            return redirect('forum:post_detail', pk=post.pk)

    else:
        # فرم خالی برای GET request
        form = CommentForm()

    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': form,  # نام مورد استفاده در template
        'title': post.title
    })


# ----------------------------------------
# ایجاد پست جدید
# ----------------------------------------
@login_required
def create_post(request):
    """
    ایجاد یک پست جدید توسط کاربر لاگین‌شده
    """

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            # ساخت پست بدون ذخیره نهایی
            post = form.save(commit=False)

            # اتصال نویسنده به پست
            post.author = request.user

            # ذخیره در دیتابیس
            post.save()

            messages.success(request, "موضوع شما با موفقیت ایجاد و منتشر شد.")

            return redirect('forum:post_detail', pk=post.pk)

    else:
        form = PostForm()

    return render(request, 'forum/create_post.html', {
        'form': form,
        'title': 'ایجاد موضوع جدید'
    })


# ----------------------------------------
# ویرایش پست (فقط نویسنده مجاز است)
# ----------------------------------------
@login_required
def edit_post(request, pk):
    """
    فقط نویسنده پست اجازه ویرایش دارد
    """

    # گرفتن پست متعلق به کاربر فعلی یا 404
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()

            messages.success(request, "پست با موفقیت ویرایش شد.")

            return redirect('forum:post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)

    return render(request, 'forum/create_post.html', {
        'form': form,
        'title': 'ویرایش پست'
    })


# ----------------------------------------
# حذف پست (فقط نویسنده)
# ----------------------------------------
@login_required
def delete_post(request, pk):
    """
    حذف پست توسط نویسنده آن
    """

    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "پست با موفقیت حذف شد.")
        return redirect('forum:post_list')

    # در GET معمولاً صفحه تأیید حذف نمایش داده می‌شود
    return redirect('forum:post_detail', pk=pk)


# ----------------------------------------
# سیستم لایک / آنلایک
# ----------------------------------------
@login_required
def like_post(request, pk):
    """
    اگر کاربر قبلاً لایک کرده باشد → آنلایک
    در غیر این صورت → لایک
    """

    post = get_object_or_404(Post, pk=pk)

    # بررسی وضعیت لایک کاربر
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('forum:post_detail', pk=pk)