from django.contrib.auth import login, authenticate
from django.contrib import messages
# from users.models import User   <==> We better use below line to decouple apps in the project
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .froms import validate_password


def user_signup_login(request, user):
    """
    This function login user with session mode. Note that because we use more than one(default) login backend,
    we must set backend the one we want. If we don't this we receive errors.
    """
    try:
        user.set_password(user.password)
        try:
            user.social_login = False
        except:
            print('social login no vojood!')
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, _('به وبسایت بیگتک خوش آمدید'))
        return True
    except:
        return False


def user_change_check(request, form):
    """This function checks if there are errors in user change profile form"""
    errors = 0
    for field in form.changed_data:
        if field == 'username' and get_user_model().objects.filter(email=form.cleaned_data[field]):
            messages.error(request, _('این نام کاربری قبلا ثبت شده'))
            errors += 1
        if field == 'email' and get_user_model().objects.filter(email=form.cleaned_data[field]):
            messages.error(request, _('این نام ایمیل قبلا ثبت شده'))
            errors += 1
        if field == 'phone' and get_user_model().objects.filter(phone=form.cleaned_data[field]):
            messages.error(request, _('این نام کاربری قبلا ثبت شده'))
            errors += 1
    return errors


def change_user_data(request, user, form):
    """Change user profile based on user change form"""
    try:
        if not user.social_login:
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
        user.last_name = form.cleaned_data['name']
        user.address = form.cleaned_data['address']
        user.phone = form.cleaned_data['phone']
        user.picture = form.cleaned_data['picture']
        user.save()
        messages.success(request, _('تغییرات با موفقیت اعمال شد'))
        return True
    except:
        messages.error(request, _('مشکل پیش آمده. تغییرات اعمال نشد'))
        return None


def user_password_change(request, form):
    """Handle user password change form"""
    if form.is_valid():
        user = request.user
        if authenticate(request, username=user.phone, password=form.cleaned_data['password']):
            if validate_password(request, form.cleaned_data['new_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, _('رمز عبور شما با موفقیت تغییر کرد'))
                return True
            return None
        else:
            messages.error(request, _('رمز عبور اشتباه است'))
            return None
    messages.error(request, _('عملیات تغییر رمز عبور مفقیت آمیز نبود. بار دیگر تلاش کنید'))
    return None
