from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
path('login_user',views.login_users,name="login"),
path('logout_user',views.logout_user,name="logout"),
path('register_user',views.register_users,name="register")
]