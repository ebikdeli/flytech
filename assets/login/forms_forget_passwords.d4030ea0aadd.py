from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _


class PasswordResetF(PasswordResetForm):
    email = forms.EmailField(label='ایمیل',
                             max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email'})
                             )


class SetPasswordF(SetPasswordForm):
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        # help_text='طول رمز عبور نباید از 6 کاراکتر کمتر باشد'
    )
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if len(password2) > 20:
                raise forms.ValidationError(_('طول رمز عبور از حد مجاز فراتر است'))
            if len(password2) < 6:
                raise forms.ValidationError(_('طول رمز عبور از 6 کاراکتر کوتاه تر است'))
        return password2
