from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


def validate_password(request, password):
    """Django has problem with custom User password validation so we have to make password validation in main view"""
    if len(password) < 6:
        messages.error(request, _('طول رمز عبور کمتر از 6 کاراکتر است'))
        return False
    if len(password) > 20:
        messages.error(request, _('طول رمز عبور از حد مجاز بیشتر است'))
        return False

    return True


class UserLogin(forms.Form):
    username_login = forms.CharField()
    password_login = forms.CharField(widget=forms.PasswordInput)


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               help_text=_('رمز عبور باید بیش از 6 کاراکتر باشد'))

    class Meta:
        model = get_user_model()
        fields = ['username', 'phone', 'email', 'password']
        widgets = {
            'email': forms.EmailInput,
            'password': forms.PasswordInput(attrs={'required': False}),  # <==> This is wrong. 'required is a option
            'phone': forms.TextInput(attrs={'type': 'phone'})            # by itself
        }
        error_messages = {
            'username': {'unique': 'این نام کاربری قبلا استفاده شده'},
            'phone': {'unique': 'این شماره تماس قبلا استفاده شده'},
            'email': {'unique': 'این ایمبل قبلا استفاده شده'},
            'password': {'required': 'لطفا رمز عبور را وارد کنید'}
        }


class UserChangeForm(forms.Form):
    username = forms.CharField(required=False)
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False, max_length=12, widget=forms.TextInput(attrs={'type': 'tel'}),
                            validators=[MaxLengthValidator(12, _('شماره تلفن صحیح نیست')),
                                        MinLengthValidator(11, _('شماره تلفن اشتباه است'))])
    address = forms.CharField(required=False, widget=forms.Textarea)
    background = forms.ImageField(required=False)


class UserPasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('رمز عبور')}),)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('رمز عبور جدید')}),
                                   help_text=_('رمز عبور جدید باید حداقل 6 کاراکتر داشته باشد'))
    new_password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('تکرار رمز عبور جدید')}))

    def clean_new_password_2(self):
        data = self.cleaned_data
        if data['new_password'] != data['new_password_2']:
            raise forms.ValidationError(_('تکرار رمز عبور جدید را به درستی وارد کنید'))
        return data
