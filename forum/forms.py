# forum/forms.py

# سیستم فرم‌های جنگو برای ساخت فرم‌های HTML و اعتبارسنجی داده‌ها
from django import forms

# مدل‌های اپلیکیشن forum
from .models import Post, Comment, Category


# ----------------------------------------
# فرم ایجاد و ویرایش پست
# ----------------------------------------
class PostForm(forms.ModelForm):
    """
    این فرم برای ایجاد و ویرایش پست‌های انجمن استفاده می‌شود.

    قابلیت‌ها:
    - ایجاد پست جدید
    - ویرایش پست موجود
    - انتخاب دسته‌بندی
    - اعتبارسنجی خودکار بر اساس مدل Post
    """

    class Meta:
        # اتصال فرم به مدل Post
        model = Post

        # فیلدهایی که در فرم نمایش داده می‌شوند
        fields = ['title', 'content', 'category']

        # تنظیم ظاهر HTML فیلدها (Bootstrap-friendly)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان موضوع را وارد کنید'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'متن خود را اینجا بنویسید...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        # برچسب‌های نمایشی در UI (فارسی‌سازی فرم)
        labels = {
            'title': 'عنوان موضوع',
            'content': 'متن پست',
            'category': 'دسته‌بندی',
        }


# ----------------------------------------
# فرم ارسال کامنت
# ----------------------------------------
class CommentForm(forms.ModelForm):
    """
    این فرم برای ثبت نظر (Comment) زیر پست‌ها استفاده می‌شود.

    ویژگی:
    - فقط شامل متن نظر است
    - به صورت خودکار به مدل Comment متصل است
    """

    class Meta:
        # اتصال به مدل Comment
        model = Comment

        # فقط فیلد محتوا در فرم نمایش داده می‌شود
        fields = ['content']

        # کنترل ظاهر textarea
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید...'
            }),
        }

        # برچسب نمایشی فیلد
        labels = {
            'content': 'متن نظر',
        }