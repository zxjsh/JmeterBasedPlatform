from django.urls import path
from . import views
from django.contrib.auth import views as authViews

app_name = 'Users'

urlpatterns = [
    path('SignIn/', views.userSignIn, name='SignIn'),
    path('SignOut/', views.userSignOut, name='SignOut'),
    path('SignUp/', views.userSignUp, name='SignUp'),
]
