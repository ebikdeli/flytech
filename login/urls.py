from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from . import forms_forget_passwords


app_name = 'login'

urlpatterns = [
    path('', views.login_signup, name='login_signup'),
    path('login/', views.classic_login, name='classic_login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/', views.profile, name='profile'),
]

urlpatterns += [
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='login/templates/forget_password/password_reset.html',
                                              form_class=forms_forget_passwords.PasswordResetF,
                                              from_email='ebikdeli@gmail.com',
                                              email_template_name='login/templates/forget_password/subject_email_template.txt',
                                              success_url=reverse_lazy('login:password_reset_done')),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='login/templates/forget_password/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='login/templates/forget_password/password_reset_confirm.html',
                                                     form_class=forms_forget_passwords.SetPasswordF,
                                                     success_url=reverse_lazy('login:password_reset_complete'),
                                                     ),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='login/templates/forget_password/password_reset_complete.html'),
         name='password_reset_complete')
]
