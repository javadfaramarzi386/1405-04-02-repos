# accounts/forms.py

# فرم‌های جنگو برای ساخت فرم‌های HTML و مدیریت اعتبارسنجی داده‌ها
from django import forms

# مدل کاربر پیش‌فرض جنگو
from django.contrib.auth.models import User

# مدل پروفایل کاربر (مدل سفارشی پروژه شما)
from .models import Profile


# --------------------------------------------------
# فرم ثبت‌نام کاربر (با امکان آپلود عکس پروفایل)
# --------------------------------------------------
class UserRegistrationForm(forms.ModelForm):
    """
    فرم ثبت‌نام کاربران جدید

    ویژگی‌ها:
    - ایجاد کاربر جدید (User)
    - دریافت رمز عبور و تأیید آن
    - امکان آپلود عکس پروفایل در زمان ثبت‌نام
    """

    # فیلد رمز عبور (به صورت مخفی در UI نمایش داده می‌شود)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        label='رمز عبور',
        help_text='رمز عبور حداقل ۸ کاراکتر باشد.'
    )

    # فیلد تأیید رمز عبور برای جلوگیری از اشتباه کاربر
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور'
        }),
        label='تکرار رمز عبور'
    )

    # فیلد اختیاری برای آپلود تصویر پروفایل هنگام ثبت‌نام
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='عکس پروفایل (اختیاری)',
        help_text='حداکثر حجم ۲ مگابایت - فرمت‌های مجاز: jpg, png, jpeg'
    )

    class Meta:
        # این فرم مستقیماً به مدل User متصل است
        model = User

        # فیلدهایی که در فرم ثبت‌نام نمایش داده می‌شوند
        fields = ['username', 'email', 'first_name']

        # تنظیم ظاهر فیلدها در HTML (Bootstrap کلاس‌ها)
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
        }

        # توضیحات کمکی برای فیلدها (نمایش در UI)
        help_texts = {
            'username': 'فقط حروف انگلیسی، اعداد و @/./+/-/_ مجاز است.',
        }

    def clean_password2(self):
        """
        بررسی تطابق رمز عبور و تکرار آن

        این متد هنگام validate شدن فرم اجرا می‌شود.
        اگر دو رمز برابر نباشند، خطا برمی‌گرداند.
        """
        cd = self.cleaned_data  # داده‌های اعتبارسنجی‌شده

        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("رمزهای عبور مطابقت ندارند.")

        return cd['password2']

    def save(self, commit=True):
        """
        ذخیره کاربر در دیتابیس + ذخیره رمز به صورت امن + ذخیره عکس پروفایل

        نکات مهم:
        - رمز عبور با set_password هش می‌شود (امنیت)
        - پروفایل کاربر از طریق رابطه OneToOne ذخیره می‌شود
        """
        # ساخت کاربر بدون ذخیره نهایی در دیتابیس
        user = super().save(commit=False)

        # هش کردن رمز عبور (عدم ذخیره به صورت خام)
        user.set_password(self.cleaned_data['password'])

        if commit:
            # ذخیره کاربر در دیتابیس
            user.save()

            # دسترسی به پروفایل مرتبط با کاربر (OneToOneField)
            profile = user.profile

            # اگر عکس پروفایل ارسال شده باشد، ذخیره شود
            if self.cleaned_data.get('avatar'):
                profile.avatar = self.cleaned_data['avatar']
                profile.save()

        return user


# --------------------------------------------------
# فرم ویرایش پروفایل کاربر
# --------------------------------------------------
class ProfileForm(forms.ModelForm):
    """
    فرم ویرایش اطلاعات پروفایل کاربر

    این فرم برای بروزرسانی اطلاعات شخصی مثل:
    - عکس پروفایل
    - توضیحات
    - سن فرزند
    - نوع شرایط فرزند
    - تنظیمات نمایش اطلاعات
    """

    class Meta:
        model = Profile

        # همه فیلدهای قابل ویرایش در پروفایل
        fields = [
            'avatar',
            'nickname',
            'bio',
            'child_age',
            'condition_type',
            'location',
            'show_bio',
            'show_child_age',
            'show_condition_type',
            'show_location'
        ]

        # کنترل ظاهر فیلدها در HTML
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام مستعار (اختیاری)'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'درباره خودتان و فرزندتان بنویسید...'
            }),
            'child_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 18
            }),
            'condition_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: اوتیسم، فلج مغزی، سندرم داون و ...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شهر محل سکونت'
            }),
        }

        # برچسب‌های نمایشی در UI (فارسی‌سازی فرم)
        labels = {
            'avatar': 'عکس پروفایل',
            'nickname': 'نام مستعار',
            'bio': 'درباره من',
            'child_age': 'سن فرزند (سال)',
            'condition_type': 'نوع معلولیت / شرایط فرزند',
            'location': 'شهر',
            'show_bio': 'نمایش "درباره من" به دیگران',
            'show_child_age': 'نمایش سن فرزند',
            'show_condition_type': 'نمایش نوع شرایط',
            'show_location': 'نمایش شهر',
        }

    def clean_child_age(self):
        """
        اعتبارسنجی فیلد سن فرزند

        قوانین:
        - باید عدد صحیح باشد
        - مقدار منفی یا بیشتر از ۱۸ مجاز نیست
        - فیلد می‌تواند خالی باشد
        """
        age = self.cleaned_data.get('child_age')

        # اگر مقدار وارد نشده باشد، خطا نده (اختیاری است)
        if age is None:
            return None

        # بررسی نوع داده (ایمنی اولیه)
        if not isinstance(age, (int, str)):
            raise forms.ValidationError("سن فرزند باید عدد باشد.")

        # تبدیل مقدار به عدد صحیح
        try:
            age = int(age)
        except (ValueError, TypeError):
            raise forms.ValidationError("سن فرزند باید یک عدد صحیح باشد.")

        # بررسی محدوده مجاز سن
        if age < 0 or age > 18:
            raise forms.ValidationError("سن فرزند باید بین ۰ تا ۱۸ سال باشد.")

        return age