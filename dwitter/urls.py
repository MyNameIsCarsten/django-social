from django.urls import path, include, reverse_lazy

# import a view functions called dashboard, profile_list and profile from your app’s views.py
from .views import dashboard, profile_list, profile, change_password

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from dwitter.views import ResetPasswordView, SignUpView, model_form_upload, profile_edit, DweetDetailView
#from dwitter.views import simple_upload
from .models import  Profile

app_name = "dwitter"


urlpatterns = [
    # access to all of the following URLs:
    #- accounts/login/ is used to log a user into your application. Refer to it by the name "login".
    #- accounts/logout/ is used to log a user out of your application. Refer to it by the name "logout".
    #- accounts/password_change/ is used to change a password. Refer to it by the name "password_change".
    #- accounts/password_change/done/ is used to show a confirmation that a password was changed. Refer to it by the name "password_change_done".
    #- accounts/password_reset/ is used to request an email with a password reset link. Refer to it by the name "password_reset".
    #- accounts/password_reset/done/ is used to show a confirmation that a password reset email was sent. Refer to it by the name "password_reset_done".
    #- accounts/reset/<uidb64>/<token>/ is used to set a new password using a password reset link. Refer to it by the name "password_reset_confirm".
    #- accounts/reset/done/ is used to show a confirmation that a password was reset. Refer to it by the name "password_reset_complete".
    path('accounts/', include('django.contrib.auth.urls')),


    path("", dashboard, {}, name="dashboard") ,
    
    # route requests that come to /profile_list to the view function called profile_list()
    path("profile_list/", profile_list, name="profile_list"),

    # angled-bracket syntax allows you to capture path components
    path("profile/<int:pk>", profile, name="profile"),    

    # login / logout urls
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # signup
    path("signup/", SignUpView.as_view(), name="signup"),

    # change password urls
    path('password/', change_password, name='change_password'),

    # password reset
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    # PasswordResetConfirmView is the view responsible for presenting this password reset form, and validating the token 
    # i.e. whether or not the token has ex ResetPasswordView.as_view()pired, or if it has been used already
    # uidb64: The user’s id encoded in base 64.
    # token: Password recovery token to check that the password is valid.
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='dwitter/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='dwitter/password_reset_complete.html'),
         name='password_reset_complete'),

    #url(r'^uploads/simple/$', simple_upload, name='simple_upload'),

    url(r'^uploads/model/$', model_form_upload, name='model_form_upload'),

    # change profile urls
    #path('profile_change/', ProfileView.as_view(), name='change_profile'),
    path("profile/<int:pk>/edit/", profile_edit, name="profile_edit"),   


    path("dweet/<int:pk>/", DweetDetailView.as_view(), name="dweet_detail"),   
]