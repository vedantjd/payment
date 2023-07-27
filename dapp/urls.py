from os import name
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path,include
from .views import *
urlpatterns = [
    # login_register urls
   
    path('',login_attempt,name='login_attempt'),
    path('register',register_attempt,name='register_attempt'),
    path('token',token_send,name='token_send'),
    path('login_success',login_success,name='login_success'),
    path('verify/<auth_token>',verify,name='verify'),
    path('error',error_page,name="error"),
    path('logout_user',logout_user,name="logout"),

    # # forget password urls template_name="passwordReset.html"
    # path('reset_password/',auth_views.PasswordResetView.as_view(), name="reset_password"),
    
    # # template_name="send_reset_password.html"
    # path('sent_reset_password/',auth_views.PasswordResetDoneView.as_view(),
    # name="password_reset_done"),
    
    # # template_name="password_reset_form.html"
    # path('reset_password/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    
    # # template_name="password_reset_complete.html"),name="password_reset_complete"
    # path('success_reset_password/',auth_views.PasswordResetCompleteView.as_view()),
    





    path('reset_password/', auth_views.PasswordResetView.as_view(),name="reset_password"),

    path('sent_reset_password/', 
        auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset_password/<uidb64>/<token>',
     auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('success_reset_password/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),







    # main project urls
    path('home', home,name="home"),
    path('success',success,name="success"),
    path('about',about,name="about"),
    path('members',members,name="members"),
    path('ratings',ratings,name="ratings"),
  
]