from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import cache_page, never_cache

from .froms import UserLogin, UserSignUpForm, UserChangeForm, \
    UserPasswordChangeForm
from .froms import validate_password
from login.login import user_signup_login, user_change_check, change_user_data,\
    user_password_change


# @cache_page(60 * 10)
def login_signup(request):
    """Render forms and templates for user to login or signup to the site"""
    if request.method == 'GET':
        login_form = UserLogin()
        signup_form = UserSignUpForm()
        context = {'login_form': login_form, 'signup_form': signup_form}
        return render(request, 'login/templates/login_signup.html', context)
    else:
        return redirect('login:login_signup')


# @cache_page(60 * 15)
def classic_login(request):
    """This handles the classic or ordinary user login procedure"""
    if request.method == 'POST':
        login_form = UserLogin(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=request.POST['phone_login'],
                                password=login_form.cleaned_data['password_login'])
            if user:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('با موفقیت وارد حساب کاربری خود شدید'))
                return redirect(reverse('core:index'))
            else:
                messages.warning(request, _('نام کاربری یا رمز عبور اشتباه است'))
                return redirect('login:login_signup')
    else:
        return redirect('login:login_signup')


def logout_view(request):
    """Logout user from website"""
    logout(request)
    messages.success(request, _('شما از حساب کاربری خود خارج شده اید'))
    return redirect('core:index')


# @cache_page(60 * 15)
def signup(request):
    """SignUp user after user proceeds with signup form in 'user_signup_view"""
    if request.method == 'POST':
        signup_form = UserSignUpForm(data=request.POST, files=request.FILES)
        if signup_form.is_valid():
            new_user = signup_form.save(commit=False)
            # Validate password manually (Django has odd behaviors to validate passwords)
            if validate_password(request, new_user.password):
                if user_signup_login(request, new_user):
                    return redirect('login:profile')
                return redirect('core:index')
    return redirect('login:login_signup')


# @login_required
def change_password(request):
    """Handle changing user password"""
    if request.method == 'POST':
        password_change_form = UserPasswordChangeForm(request.POST)
        if user_password_change(request, password_change_form):
            return redirect('core:index')
        redirect('login:change_password')
    else:
        password_change_form = UserPasswordChangeForm()
    return render(request, 'password_change.html', {'password_change_form': password_change_form})


# @cache_page(60 * 10)
@login_required
def profile(request):
    """This view set-change user profile identifications"""
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'phone': user.phone,
        'address': user.address,
        'picture': user.picture
    }
    if request.method == 'POST':
        change_form = UserChangeForm(data=request.POST, files=request.FILES, initial=data)
        if change_form.is_valid():
            if change_form.has_changed():
                errors = user_change_check(request, change_form)
                if errors > 0:
                    return redirect('login:profile')
                if change_user_data(request, user, change_form):
                    return redirect('login:profile')
                return redirect('login:profile')
    else:
        change_form = UserChangeForm(initial=data)
    return render(request, 'login/templates/profile.html', {'change_form': change_form})
