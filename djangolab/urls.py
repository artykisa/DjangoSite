"""djangolab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from firstapp import views
from django.views.generic import TemplateView
from firstapp.views import MemberList, GuideList, activate, activation_sent_view
from firstapp import forms
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path(r'^fivexfive/', TemplateView.as_view(template_name="firstapp/fivexfive.html")),
    path('contact/', TemplateView.as_view(template_name="firstapp/contact.html")),
    path('admin/', admin.site.urls),
    path('products/<int:productid>/', views.products),
    path('logins/', views.index),
    re_path(r'^guides/cur_guide/', views.guide),
    path('addguide/', forms.GuideAddForm.as_view(), name='guide_new'),
    path('guides/<pk>/updateguide/', forms.GuideUpdateForm.as_view(), name='guide_update'),
    path('guides/<pk>/deleteguide/', forms.GuideDeleteForm.as_view(), name='delete'),
    re_path(r'^guides/', GuideList.as_view()),
    re_path(r'^heroes/', MemberList.as_view()),
    re_path(r'^articles/', TemplateView.as_view(template_name="firstapp/articles.html")),
    re_path(r'^register/', views.register, name='register'),
    re_path(r'^accounts/profile/', views.account, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='firstapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='firstapp/logout.html'), name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('sent/', activation_sent_view, name="activation_sent"),
    re_path(r'^', TemplateView.as_view(template_name="firstapp/main.html"))
]
